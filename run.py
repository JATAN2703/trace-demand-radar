"""Daily entry point. Collect -> store -> score -> alert -> write digest.

Designed to be run by cron (see .github/workflows/daily.yml). Each invocation
appends one snapshot, so momentum and alerting are computed against real stored
history rather than assumed.
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

import yaml

import store
import alerts
from collectors.base import Fetcher
from collectors import shopmy, poshmark, trends

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"


def load_config() -> dict:
    with open(ROOT / "watchlist.yaml") as f:
        return yaml.safe_load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-trends", action="store_true",
                    help="skip Google Trends (unofficial endpoint, rate-limits)")
    ap.add_argument("--no-supply", action="store_true", help="skip Poshmark supply")
    ap.add_argument("--creators", type=int, default=None, help="limit creators (smoke test)")
    args = ap.parse_args()

    cfg = load_config()
    creators = cfg["creators"][: args.creators] if args.creators else cfg["creators"]
    fetcher = Fetcher(delay=cfg.get("request_delay", 0.7))

    conn = store.connect()
    # Diff against a roughly 24h-old run rather than simply the previous one, so
    # the comparison stays like-for-like however often the cron fires. See
    # store.baseline_run for why this matters.
    prev_run, baseline_age = store.baseline_run(conn)
    run_id = store.start_run(conn, notes=f"creators={len(creators)}")
    print(f"run {run_id} started (baseline run: {prev_run}, "
          f"{baseline_age}h old)" if prev_run else f"run {run_id} started (no baseline yet)")

    # --- demand -------------------------------------------------------------
    products, pins, meta = shopmy.collect(
        fetcher, creators,
        category_filter=cfg.get("category_filter", "Dresses"),
        max_collections=cfg.get("max_collections_per_creator", 12),
        staleness_days=cfg.get("collection_staleness_days", 400),
    )
    n_prod = store.insert_products(conn, run_id, "shopmy", products, confidence="observed")
    n_pins = store.insert_pins(conn, run_id, pins, confidence="observed")
    print(f"  shopmy: {n_prod} products, {n_pins} pins, "
          f"{len(meta['creators_ok'])}/{len(creators)} creators ok")

    # --- supply -------------------------------------------------------------
    # Check the brands we care about plus whatever the demand side actually
    # surfaced, so supply follows demand instead of a stale hand-written list.
    if not args.no_supply:
        top_brands = []
        for p in sorted(products, key=lambda x: -(x.get("daily_clicks") or 0)):
            b = p.get("brand")
            if b and b not in top_brands:
                top_brands.append(b)
            if len(top_brands) >= 8:
                break
        brands = list(dict.fromkeys(cfg.get("supply_brands", []) + top_brands))
        for row in poshmark.collect(fetcher, brands):
            store.insert_supply(conn, run_id, row["source"], row["query"], row["brand"],
                                row["listing_count"], row["confidence"], row["note"])
        print(f"  poshmark: checked {len(brands)} brands")

    # --- independent demand cross-check ------------------------------------
    if not args.no_trends:
        for row in trends.collect(cfg.get("trend_terms", [])):
            store.insert_trend(conn, run_id, row["term"], row["window"],
                               row["mean_recent"], row["mean_prior"], row["ratio"],
                               row["confidence"])
        print(f"  trends: {len(cfg.get('trend_terms', []))} terms")

    store.finish_run(conn, run_id)

    # --- report -------------------------------------------------------------
    meta["errors"] = fetcher.errors
    meta["baseline_age_hours"] = baseline_age
    text = alerts.digest(conn, run_id, prev_run, meta)
    REPORTS.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    (REPORTS / f"{stamp}_run{run_id}.md").write_text(text)
    (REPORTS / "latest.md").write_text(text)
    print("\n" + text)
    if fetcher.errors:
        print(f"\n[{len(fetcher.errors)} source errors, run completed on partial data]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
