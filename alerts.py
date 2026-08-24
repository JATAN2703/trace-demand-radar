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

# Trajectories TRACE can act on. Per Ella: "an item beginning to gain momentum,
# one currently peaking, or one that has been especially popular over the past
# two weeks." `sustained` covers that third case. A cooling or faded product must
# not be able to head the board on gap alone.
ACTIONABLE = ("rising", "peaking", "sustained")

# Precision gates. An alert triggers content, creator outreach, comment
# engagement, lister identification and possibly a seeded listing, so a false
# positive costs a small team real coordinated effort. Better to surface three
# items worth acting on than twenty worth triaging.
MIN_PRICE_FIT_TO_ALERT = 0.5   # ignore items well outside the $400-1,000 band
MAX_ALERTS = 5                 # a digest, not a queue


def load_config() -> dict:
    path = Path(__file__).parent / "watchlist.yaml"
    return yaml.safe_load(path.read_text()) or {}


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


def occasion_for(conn, run_id: int) -> dict:
    """Dominant occasion per product, from the collections it was filed under.

    A dress can appear in several creators' collections with different framings;
    we take the most frequent, preferring a named occasion over 'unknown'.
    """
    rows = conn.execute(
        """SELECT product_id, occasion, COUNT(*) AS n
           FROM creator_pins WHERE run_id = ? AND occasion IS NOT NULL
           GROUP BY product_id, occasion""",
        (run_id,),
    ).fetchall()
    best: dict[str, tuple[int, bool, str]] = {}
    for r in rows:
        pid, occ, n = r["product_id"], r["occasion"], r["n"]
        # Rank by count, then prefer a named occasion over 'unknown'.
        cand = (n, occ != "unknown", occ)
        if pid not in best or cand > best[pid]:
            best[pid] = cand
    return {pid: occ for pid, (_, _, occ) in best.items()}


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
    occasions = occasion_for(conn, run_id)

    cfg = load_config()
    band = cfg.get("price_band", {})
    occ_weights = cfg.get("occasion_weights", {})

    board = []
    for pid, p in prods.items():
        label, a_short, a_mid = sc.classify(p)
        n_creators = creators.get(pid, 1)
        demand = sc.demand_score(p, distinct_creators=n_creators)
        # A hand-checked product-level count beats a brand-level proxy.
        listings = manual[pid] if pid in manual else supply.get(p.get("brand"))
        occ = occasions.get(pid, "unknown")
        pfit = sc.price_fit(p.get("price"), band)
        gap = sc.gap_score(demand, listings)
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
            "gap": gap,
            "occasion": occ,
            "price_fit": round(pfit, 3),
            "priority": sc.priority(gap, pfit, occ_weights.get(occ, 0.8)),
        })
    # Actionable trajectories first, then by priority. Priority rather than raw
    # gap, so TRACE's stated targeting (the $400-1,000 occasionwear focus) drives
    # the order a human reads, while `gap` stays the untargeted measurement.
    board.sort(key=lambda r: (r["label"] not in ACTIONABLE, -r["priority"]))
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

        # Precision gates, in order of how cheaply they reject.
        if r["label"] not in ACTIONABLE:
            continue
        if r["price_fit"] < MIN_PRICE_FIT_TO_ALERT:
            continue  # outside TRACE's band, so not worth a human's time

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

    # Cap the digest. If everything is an alert, nothing is: a small team can
    # only run content plus outreach plus seeding on a handful of items at once.
    # Ordering follows the board, which is already priority-sorted, so the cap
    # keeps the highest-priority signals rather than an arbitrary slice.
    if len(out) > MAX_ALERTS:
        out = out[:MAX_ALERTS] + [{
            "kind": "suppressed", "product": None,
            "message": f"{len(out) - MAX_ALERTS} further threshold crossings not "
                       f"shown; raise MAX_ALERTS to see them.",
        }]
    return out


def digest(conn, curr_run: int, prev_run: int | None, meta: dict) -> str:
    board = build_board(conn, curr_run)
    alerts = diff(conn, curr_run, prev_run)
    scored = [r for r in board if r["label"] != "insufficient_volume"]
    actionable = [r for r in scored if r["label"] in ACTIONABLE]
    faded = sorted([r for r in scored if r["label"] == "faded"],
                   key=lambda r: -(r.get("total_clicks") or 0))

    L = ["# TRACE Demand Radar", ""]
    note = meta.get("baseline_note", "")
    if prev_run is None:
        L.append(f"Run `{curr_run}`, with _no prior run to compare against (baseline)_.")
    else:
        L.append(f"Run `{curr_run}`, compared against {note}.")
        L.append("")
        L.append("> The source republishes its click counters as a once-daily batch "
                 "(measured: zero of 525 products changed across five snapshots "
                 "spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). "
                 "Deltas below are therefore one publish apart, so a change means one "
                 "day of movement, not the elapsed wall-clock time between runs.")
    L.append(f"{len(board)} dress products from {len(meta.get('creators_ok', []))} creators "
             f"across {meta.get('collections_scanned', 0)} collections. "
             f"{len(scored)} cleared the volume floor, {len(actionable)} are in play "
             f"(rising, peaking or sustained).")
    L += ["", "## Alerts", ""]
    if alerts:
        L += [f"- **{a['kind']}** - {a['product'] or ''} {a['message']}".strip() for a in alerts]
    else:
        L.append("- No threshold crossings this run.")

    L += ["", "## In play, ranked by priority", "",
          "Rising, peaking, or sustained (especially popular recently), ordered by "
          "priority = gap x price fit x occasion weight. Targeting is TRACE's stated "
          "focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.", "",
          "| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(actionable[:TOP_N], 1):
        sup = f"{r['supply_listings']} ({r['supply_source']})" if r["supply_observed"] else "unmeasured"
        L.append(f"| {i} | {str(r.get('title'))[:34]} | {r.get('brand')} | "
                 f"{r.get('price')} | {r['price_fit']} | {r['occasion']} | "
                 f"{r['label']} | {r['accel_short']} | "
                 f"{r['distinct_creators']} | {r.get('daily_clicks')} | {sup} | "
                 f"{r['gap']} | {r['priority']} |")

    if faded:
        L += ["", "## Past peak (what a retrospective report would wrongly surface)", "",
              "High all-time volume, thin recent activity. Listed so the contrast is "
              "explicit: these are the products a 'most popular dresses' report would "
              "lead with, and they are exactly the ones TRACE should not organize "
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
