"""Alerting: what changed since the last run.

An alert is by definition a comparison against prior state, which is why the
store is append-only. A single-snapshot script can rank products; it cannot tell
you a product *started* accelerating, or entered the top of the board for the
first time. Those are the two things TRACE actually needs to act on.

Output is a short markdown digest, because the reader is a COO deciding where to
point content, creator outreach or seeding, not someone reading a database.
"""

from pathlib import Path

import yaml

import score as sc

TOP_N = 10
ACCEL_JUMP = 0.35   # rise in accel_short between runs worth flagging

# Trajectories TRACE can act on. The brief asks for products "beginning to gain
# momentum, experiencing peak current interest, or demonstrating both", so a
# cooling product must not be able to head the board on gap alone.
ACTIONABLE = ("rising", "peaking")


def _index(rows) -> dict:
    return {r["product_id"]: dict(r) for r in rows}


def load_run(conn, run_id: int) -> dict:
    rows = conn.execute(
        "SELECT * FROM product_snapshots WHERE run_id = ?", (run_id,)
    ).fetchall()
    return _index(rows)


def supply_for(conn, run_id: int) -> dict:
    """Brand-level supply, but only where it was genuinely observed.

    Rows tagged `floor_saturated` are discarded: page one of a Poshmark brand
    page saturates at 48 for every brand, so the number carries no information.
    Discarding it means those products fall through to `unmeasured` instead of
    being scored against a meaningless count.
    """
    rows = conn.execute(
        """SELECT brand, listing_count FROM supply_snapshots
           WHERE run_id = ? AND confidence = 'observed'""",
        (run_id,),
    ).fetchall()
    return {r["brand"]: r["listing_count"] for r in rows if r["brand"]}


def manual_supply() -> dict:
    """Per-product supply measured by hand, keyed by ShopMy product id.

    Poshmark and Pickle counts are summed into one secondary-supply figure. A
    null on both sides stays None, which the scorer treats as neutral rather
    than as thin supply.
    """
    path = Path(__file__).parent / "manual_supply.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text()) or {}
    out = {}
    for obs in (data.get("observations") or []):
        pid = str(obs.get("product_id") or "")
        if not pid:
            continue
        parts = [obs.get("poshmark_listings"), obs.get("pickle_listings")]
        vals = [v for v in parts if isinstance(v, int)]
        out[pid] = sum(vals) if vals else None
    return out


def creator_counts(conn, run_id: int) -> dict:
    rows = conn.execute(
        """SELECT product_id, COUNT(DISTINCT creator) AS n
           FROM creator_pins WHERE run_id = ? GROUP BY product_id""",
        (run_id,),
    ).fetchall()
    return {r["product_id"]: r["n"] for r in rows}


def build_board(conn, run_id: int) -> list[dict]:
    """Score and rank every product in a run."""
    prods = load_run(conn, run_id)
    supply = supply_for(conn, run_id)
    manual = manual_supply()
    creators = creator_counts(conn, run_id)

    board = []
    for pid, p in prods.items():
        label, a_short, a_mid = sc.classify(p)
        n_creators = creators.get(pid, 1)
        demand = sc.demand_score(p, distinct_creators=n_creators)
        # A hand-checked product-level count beats a brand-level proxy.
        listings = manual[pid] if pid in manual else supply.get(p.get("brand"))
        board.append({
            **p,
            "label": label,
            "accel_short": round(a_short, 3) if a_short else None,
            "accel_mid": round(a_mid, 3) if a_mid else None,
            "distinct_creators": n_creators,
            "demand": demand,
            "supply_listings": listings,
            "supply_observed": listings is not None,
            "supply_source": ("manual" if pid in manual
                              else "poshmark" if listings is not None else None),
            "gap": sc.gap_score(demand, listings),
        })
    # Actionable trajectories first, then by gap. Without this a fading product
    # with thin supply outranks one that is actually accelerating, which is the
    # opposite of what TRACE needs to see.
    board.sort(key=lambda r: (r["label"] not in ACTIONABLE, -r["gap"]))
    return board


def diff(conn, curr_run: int, prev_run: int | None) -> list[dict]:
    """Alerts worth a human's attention. Empty list is a valid, honest answer."""
    curr = build_board(conn, curr_run)
    if prev_run is None:
        return [{"kind": "baseline", "product": None,
                 "message": f"Baseline run recorded ({len(curr)} products). "
                            "Deltas and alerts begin from the next run."}]

    prev = load_run(conn, prev_run)
    prev_rank = [r["product_id"] for r in build_board(conn, prev_run)[:TOP_N]]
    out = []

    for i, r in enumerate(curr):
        pid = r["product_id"]
        p_old = prev.get(pid)
        name = f"{r.get('title')} ({r.get('brand')})"

        if r["label"] == "insufficient_volume":
            continue

        if i < TOP_N and pid not in prev_rank:
            out.append({"kind": "new_entrant", "product": name,
                        "message": f"entered the top {TOP_N} at #{i+1} "
                                   f"(gap {r['gap']}, {r['label']})"})

        d = sc.day_over_day(r, p_old)
        if d and d.get("d_accel_short", 0) >= ACCEL_JUMP:
            out.append({"kind": "accelerating", "product": name,
                        "message": f"acceleration rose {d['d_accel_short']:+} "
                                   f"to {r['accel_short']} since the last run"})

        if p_old is not None:
            old_label, _, _ = sc.classify(dict(p_old))
            if old_label != r["label"] and r["label"] in ("rising", "peaking"):
                out.append({"kind": "trajectory_change", "product": name,
                            "message": f"{old_label} -> {r['label']}"})

        if d and d.get("d_num_promoters", 0) >= 10:
            out.append({"kind": "creator_pickup", "product": name,
                        "message": f"+{d['d_num_promoters']} creators promoting since last run"})

    return out


def digest(conn, curr_run: int, prev_run: int | None, meta: dict) -> str:
    board = build_board(conn, curr_run)
    alerts = diff(conn, curr_run, prev_run)
    scored = [r for r in board if r["label"] != "insufficient_volume"]
    actionable = [r for r in scored if r["label"] in ACTIONABLE]
    faded = sorted([r for r in scored if r["label"] == "faded"],
                   key=lambda r: -(r.get("total_clicks") or 0))

    L = ["# TRACE Demand Radar", ""]
    age = meta.get("baseline_age_hours")
    if prev_run is None:
        L.append(f"Run `{curr_run}`, with _no prior run to compare against (baseline)_.")
    else:
        L.append(f"Run `{curr_run}`, compared against run `{prev_run}` "
                 f"({age}h earlier).")
        if age is not None and age < 20:
            L.append("")
            L.append(f"> Baseline is only {age}h old. The upstream click counters are "
                     "reported at daily granularity, so a sub-daily comparison may "
                     "reflect the counter's own refresh cycle rather than real demand "
                     "movement. Deltas below are indicative, not conclusive, until a "
                     "full-day baseline exists.")
    L.append(f"{len(board)} dress products from {len(meta.get('creators_ok', []))} creators "
             f"across {meta.get('collections_scanned', 0)} collections. "
             f"{len(scored)} cleared the volume floor, {len(actionable)} are rising or peaking.")
    L += ["", "## Alerts", ""]
    if alerts:
        L += [f"- **{a['kind']}** - {a['product'] or ''} {a['message']}".strip() for a in alerts]
    else:
        L.append("- No threshold crossings this run.")

    L += ["", "## Rising or peaking, ranked by demand-supply gap", "",
          "| # | Product | Brand | $ | State | Accel | Creators | Daily | Supply | Gap |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(actionable[:TOP_N], 1):
        sup = f"{r['supply_listings']} ({r['supply_source']})" if r["supply_observed"] else "unmeasured"
        L.append(f"| {i} | {str(r.get('title'))[:38]} | {r.get('brand')} | "
                 f"{r.get('price')} | {r['label']} | {r['accel_short']} | "
                 f"{r['distinct_creators']} | {r.get('daily_clicks')} | {sup} | {r['gap']} |")

    if faded:
        L += ["", "## Past peak (what a retrospective report would wrongly surface)", "",
              "High all-time volume, thin recent activity. Listed so the contrast is "
              "explicit: these are the products a 'most popular dresses' report would "
              "lead with, and they are exactly the ones TRACE should not organise "
              "demand around now.", "",
              "| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |",
              "|---|---|---|---|---|---|"]
        for r in faded[:5]:
            L.append(f"| {str(r.get('title'))[:38]} | {r.get('brand')} | "
                     f"{r.get('total_clicks')} | {r.get('monthly_clicks')} | "
                     f"{r.get('weekly_clicks')} | {r['accel_mid']} |")

    if meta.get("errors"):
        L += ["", "## Sources unavailable this run", ""]
        L += [f"- {e}" for e in meta["errors"][:8]]
    L += ["", "_Supply shown as `unmeasured` is not the same as zero; those rows are "
          "scored at neutral supply so an unchecked item cannot masquerade as a "
          "confirmed gap._"]
    return "\n".join(L)
