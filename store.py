"""Append-only snapshot store.

History is the product here: momentum is a derivative, so we never overwrite a
row. Every collector run inserts a new dated snapshot and old rows stay put.
That is what makes day-over-day deltas and alerting possible at all.
"""

import sqlite3
import datetime as dt
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "radar.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at  TEXT NOT NULL,
    finished_at TEXT,
    notes       TEXT
);

-- One row per (run, product). The click counters are cumulative windows as
-- reported by the source, not deltas we computed.
CREATE TABLE IF NOT EXISTS product_snapshots (
    run_id         INTEGER NOT NULL,
    observed_at    TEXT NOT NULL,
    source         TEXT NOT NULL,
    product_id     TEXT NOT NULL,
    title          TEXT,
    brand          TEXT,
    category       TEXT,
    price          REAL,
    num_promoters  INTEGER,
    daily_clicks   INTEGER,
    weekly_clicks  INTEGER,
    monthly_clicks INTEGER,
    total_clicks   INTEGER,
    domain         TEXT,
    confidence     TEXT NOT NULL,
    PRIMARY KEY (run_id, source, product_id)
);

-- Which creator surfaced which product, and when they pinned it. Lets us say
-- "N distinct creators are currently linking this" and spot fresh adoption.
CREATE TABLE IF NOT EXISTS creator_pins (
    run_id          INTEGER NOT NULL,
    observed_at     TEXT NOT NULL,
    creator         TEXT NOT NULL,
    collection_id   TEXT,
    collection_name TEXT,
    occasion        TEXT,
    product_id      TEXT NOT NULL,
    pinned_at       TEXT,
    confidence      TEXT NOT NULL
);

-- Secondary-market supply. Deliberately source-agnostic: Poshmark is automated,
-- Pickle is manual (blocked by bot protection), and both land in the same table
-- distinguished by `confidence`.
CREATE TABLE IF NOT EXISTS supply_snapshots (
    run_id        INTEGER NOT NULL,
    observed_at   TEXT NOT NULL,
    source        TEXT NOT NULL,
    query         TEXT NOT NULL,
    brand         TEXT,
    listing_count INTEGER,
    confidence    TEXT NOT NULL,
    note          TEXT
);

-- Independent demand cross-check, so we can tell genuine consumer pull apart
-- from creator-side promotion.
CREATE TABLE IF NOT EXISTS trend_snapshots (
    run_id      INTEGER NOT NULL,
    observed_at TEXT NOT NULL,
    term        TEXT NOT NULL,
    window      TEXT NOT NULL,
    mean_recent REAL,
    mean_prior  REAL,
    ratio       REAL,
    confidence  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_prod_pid  ON product_snapshots(product_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_pins_pid  ON creator_pins(product_id);
CREATE INDEX IF NOT EXISTS idx_supply_q  ON supply_snapshots(query, observed_at);
"""

# Only these fields are ever persisted from an upstream payload. The ShopMy user
# endpoint incidentally returns unrelated internal fields (a referring brand's
# Stripe customer id, a support phone number, admin flags). We do not want them,
# so the collectors map explicitly into the columns above and everything else is
# dropped on the floor rather than stored "just in case".
PRODUCT_FIELDS = (
    "product_id", "title", "brand", "category", "price", "num_promoters",
    "daily_clicks", "weekly_clicks", "monthly_clicks", "total_clicks", "domain",
)


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _migrate(conn: sqlite3.Connection) -> None:
    """Add columns introduced after the first snapshots were already recorded.

    History is the asset here, so schema changes have to be additive rather than
    a rebuild. SQLite has no ADD COLUMN IF NOT EXISTS, hence the probe.
    """
    have = {r["name"] for r in conn.execute("PRAGMA table_info(creator_pins)")}
    for col in ("collection_name", "occasion"):
        if col not in have:
            conn.execute(f"ALTER TABLE creator_pins ADD COLUMN {col} TEXT")
    conn.commit()


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


def start_run(conn: sqlite3.Connection, notes: str = "") -> int:
    cur = conn.execute(
        "INSERT INTO runs (started_at, notes) VALUES (?, ?)", (utcnow(), notes)
    )
    conn.commit()
    return cur.lastrowid


def finish_run(conn: sqlite3.Connection, run_id: int) -> None:
    conn.execute("UPDATE runs SET finished_at = ? WHERE run_id = ?", (utcnow(), run_id))
    conn.commit()


def insert_products(conn, run_id: int, source: str, rows: list[dict], confidence: str) -> int:
    """Insert product snapshots, whitelisting fields. Returns rows written."""
    seen, payload = set(), []
    ts = utcnow()
    for r in rows:
        pid = str(r.get("product_id") or "")
        if not pid or pid in seen:
            continue  # same product can appear in several collections
        seen.add(pid)
        payload.append((
            run_id, ts, source, pid, r.get("title"), r.get("brand"),
            r.get("category"), r.get("price"), r.get("num_promoters"),
            r.get("daily_clicks"), r.get("weekly_clicks"), r.get("monthly_clicks"),
            r.get("total_clicks"), r.get("domain"), confidence,
        ))
    conn.executemany(
        """INSERT OR REPLACE INTO product_snapshots
           (run_id, observed_at, source, product_id, title, brand, category, price,
            num_promoters, daily_clicks, weekly_clicks, monthly_clicks, total_clicks,
            domain, confidence)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        payload,
    )
    conn.commit()
    return len(payload)


def insert_pins(conn, run_id: int, rows: list[dict], confidence: str) -> int:
    ts = utcnow()
    payload = [
        (run_id, ts, r.get("creator"), str(r.get("collection_id") or ""),
         r.get("collection_name"), r.get("occasion"),
         str(r.get("product_id") or ""), r.get("pinned_at"), confidence)
        for r in rows if r.get("product_id")
    ]
    conn.executemany(
        """INSERT INTO creator_pins
           (run_id, observed_at, creator, collection_id, collection_name, occasion,
            product_id, pinned_at, confidence)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        payload,
    )
    conn.commit()
    return len(payload)


def insert_supply(conn, run_id: int, source: str, query: str, brand: str | None,
                  listing_count: int | None, confidence: str, note: str = "") -> None:
    conn.execute(
        """INSERT INTO supply_snapshots
           (run_id, observed_at, source, query, brand, listing_count, confidence, note)
           VALUES (?,?,?,?,?,?,?,?)""",
        (run_id, utcnow(), source, query, brand, listing_count, confidence, note),
    )
    conn.commit()


def insert_trend(conn, run_id: int, term: str, window: str, mean_recent: float | None,
                 mean_prior: float | None, ratio: float | None, confidence: str) -> None:
    conn.execute(
        """INSERT INTO trend_snapshots
           (run_id, observed_at, term, window, mean_recent, mean_prior, ratio, confidence)
           VALUES (?,?,?,?,?,?,?,?)""",
        (run_id, utcnow(), term, window, mean_recent, mean_prior, ratio, confidence),
    )
    conn.commit()


def latest_two_runs(conn) -> list[int]:
    """Run ids for the two most recent completed runs, newest first.

    Alerting is a comparison against prior state, so this is the hinge that a
    single-shot script cannot provide.
    """
    rows = conn.execute(
        "SELECT run_id FROM runs WHERE finished_at IS NOT NULL ORDER BY run_id DESC LIMIT 2"
    ).fetchall()
    return [r["run_id"] for r in rows]


def previous_batch_run(conn, current_run: int) -> tuple[int | None, str]:
    """The most recent run whose data is from a DIFFERENT upstream batch.

    Measured behaviour of the source (see eval/counter_cadence.py): ShopMy's
    click counters are republished as a once-daily batch. Across five
    consecutive snapshots spanning 23:27 to 07:27 UTC, zero of 525 products
    changed; at the 13:27 snapshot, 248 of 526 changed at once. So the counters
    are not live, they are a daily publish.

    That makes wall-clock a poor baseline. Two runs inside the same batch window
    yield an empty diff that looks like "nothing is happening" when really
    nothing has been *published*. Conversely a baseline two batches back
    understates a single day's move.

    So we walk backwards to the first run whose `daily_clicks` panel actually
    differs, and diff against that. The comparison is then always exactly one
    upstream publish apart, whatever the cron does.

    Returns (run_id, note). note explains what was chosen, for the digest.
    """
    rows = conn.execute(
        "SELECT run_id FROM runs WHERE finished_at IS NOT NULL AND run_id < ? "
        "ORDER BY run_id DESC",
        (current_run,),
    ).fetchall()
    skipped = 0
    for r in rows:
        rid = r["run_id"]
        changed = conn.execute(
            """SELECT COUNT(*) AS n
               FROM product_snapshots x JOIN product_snapshots y USING(product_id)
               WHERE x.run_id = ? AND y.run_id = ?
                 AND x.daily_clicks IS NOT NULL AND y.daily_clicks IS NOT NULL
                 AND x.daily_clicks <> y.daily_clicks""",
            (current_run, rid),
        ).fetchone()["n"]
        if changed > 0:
            note = (f"run {rid} (previous upstream batch"
                    + (f", skipped {skipped} same-batch run(s)" if skipped else "")
                    + ")")
            return rid, note
        skipped += 1
    if rows:
        return rows[0]["run_id"], (f"run {rows[0]['run_id']} (no distinct batch found; "
                                   "all prior runs share this batch)")
    return None, "no prior run"


MIN_BASELINE_HOURS = 20


def baseline_run(conn, min_hours: float = MIN_BASELINE_HOURS) -> tuple[int | None, float | None]:
    """Pick the run to diff against: the newest one at least `min_hours` old.

    Why not simply the previous run. The upstream click counters are reported at
    daily granularity, and we have not yet established whether `dailyClicks` is a
    rolling trailing-24h window or a same-day accumulator that resets. If it
    accumulates, then comparing a 3pm snapshot against a 9am snapshot shows the
    counter filling up and reads as acceleration that never happened.

    Anchoring to a roughly 24-hour-old baseline keeps every comparison
    like-for-like no matter how often we poll, so polling frequency becomes a
    detection-latency choice rather than a correctness risk.

    Returns (run_id, age_in_hours). Falls back to the oldest completed run when
    nothing is old enough yet, so early runs still produce a usable comparison,
    and the caller can say so honestly in the digest.
    """
    now = dt.datetime.now(dt.timezone.utc)
    rows = conn.execute(
        "SELECT run_id, started_at FROM runs WHERE finished_at IS NOT NULL "
        "ORDER BY run_id DESC"
    ).fetchall()
    if not rows:
        return None, None

    def age(row) -> float:
        started = dt.datetime.fromisoformat(row["started_at"])
        if started.tzinfo is None:
            started = started.replace(tzinfo=dt.timezone.utc)
        return (now - started).total_seconds() / 3600.0

    for r in rows:
        a = age(r)
        if a >= min_hours:
            return r["run_id"], round(a, 1)
    oldest = rows[-1]
    return oldest["run_id"], round(age(oldest), 1)
