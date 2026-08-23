"""Is `dailyClicks` a rolling 24h window, or a same-day accumulator?

This matters for correctness, not curiosity. If the counter accumulates through
the UTC day and resets at midnight, then any intraday comparison shows the
counter filling up and reads as acceleration that never happened. If it is a
rolling trailing-24h window, intraday comparisons are meaningful and we get
faster detection.

We do not assume either. With four snapshots a day the data answers it:

  * ACCUMULATOR  -> within a single UTC day, dailyClicks rises monotonically
                    across snapshots, then drops sharply at the day boundary.
  * ROLLING      -> values fluctuate up and down within a day with no
                    systematic climb and no reset at midnight.

Run:  python eval/counter_cadence.py
"""

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import store  # noqa: E402

MIN_PRODUCTS = 20   # need a decent panel before claiming anything


def main() -> int:
    conn = store.connect()
    rows = conn.execute(
        """SELECT run_id, observed_at, product_id, daily_clicks
           FROM product_snapshots
           WHERE daily_clicks IS NOT NULL
           ORDER BY observed_at"""
    ).fetchall()

    if not rows:
        print("No snapshots yet.")
        return 0

    # (utc_date, hour) buckets per product
    by_product: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
    for r in rows:
        day, _, rest = r["observed_at"].partition("T")
        hour = int(rest[:2]) if rest[:2].isdigit() else 0
        by_product[r["product_id"]].append((day, hour, r["daily_clicks"]))

    days = sorted({d for obs in by_product.values() for d, _, _ in obs})
    hours = sorted({h for obs in by_product.values() for _, h, _ in obs})
    print(f"{len(rows)} snapshots | {len(by_product)} products | "
          f"{len(days)} UTC day(s) {days} | hours seen {hours}")

    if len(hours) < 2:
        print("\nVERDICT: insufficient data. Need at least two snapshots at "
              "different hours of the same UTC day. Wait for the 6-hourly cron.")
        return 0

    rising = flat = falling = 0
    resets = 0
    panel = 0

    for pid, obs in by_product.items():
        per_day = defaultdict(list)
        for day, hour, val in obs:
            per_day[day].append((hour, val))

        # Intraday direction: compare first and last snapshot within each day.
        for day, seq in per_day.items():
            if len(seq) < 2:
                continue
            seq.sort()
            panel += 1
            first, last = seq[0][1], seq[-1][1]
            if last > first:
                rising += 1
            elif last < first:
                falling += 1
            else:
                flat += 1

        # Day boundary: does the first value of a day drop below the last value
        # of the previous day? That is the signature of a reset.
        ds = sorted(per_day)
        for a, b in zip(ds, ds[1:]):
            prev_last = sorted(per_day[a])[-1][1]
            next_first = sorted(per_day[b])[0][1]
            if prev_last > 0 and next_first < prev_last * 0.6:
                resets += 1

    if panel < MIN_PRODUCTS:
        print(f"\nVERDICT: only {panel} product-days with multiple snapshots. "
              f"Need >= {MIN_PRODUCTS} before drawing a conclusion.")
        return 0

    print(f"\nIntraday direction across {panel} product-days: "
          f"rising {rising}, flat {flat}, falling {falling}")
    print(f"Day-boundary drops consistent with a reset: {resets}")

    share_rising = rising / panel
    if share_rising > 0.7 and resets > 0:
        verdict = ("ACCUMULATOR. dailyClicks climbs through the UTC day and "
                   "resets at the boundary, so intraday comparisons are NOT "
                   "valid. The ~24h baseline anchoring in store.baseline_run is "
                   "required, not optional.")
    elif share_rising < 0.55 and resets == 0:
        verdict = ("ROLLING trailing-24h window. Intraday comparisons are "
                   "meaningful, so polling frequency can be raised to cut "
                   "detection latency.")
    else:
        verdict = ("INCONCLUSIVE. The pattern is mixed. Keep the ~24h baseline "
                   "anchoring, which is safe under either behaviour, and collect "
                   "more days.")
    print(f"\nVERDICT: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
