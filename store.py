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
    run_id        INTEGER NOT NULL,
    observed_at   TEXT NOT NULL,
    creator       TEXT NOT NULL,
    collection_id TEXT,
    product_id    TEXT NOT NULL,
    pinned_at     TEXT,
    confidence    TEXT NOT NULL
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


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
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
         str(r.get("product_id") or ""), r.get("pinned_at"), confidence)
        for r in rows if r.get("product_id")
    ]
    conn.executemany(
        """INSERT INTO creator_pins
           (run_id, observed_at, creator, collection_id, product_id, pinned_at, confidence)
           VALUES (?,?,?,?,?,?,?)""",
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
