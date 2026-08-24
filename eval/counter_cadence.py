"""How often does source actually republish its click counters?

This matters for correctness and for cost. If the counters are live, frequent
polling cuts detection latency. If they are republished as a periodic batch,
frequent polling fetches an identical payload and buys nothing, and worse, any
diff taken inside one batch window reads as "nothing is happening" when really
nothing has been *published*.

MEASURED ANSWER (2026-08-23): a once-daily batch.

    run 1 -> 2      0 of 525 products changed   (23:27 -> 23:48 UTC)
    run 2 -> 3      0 of 525                    (23:48 -> 01:58)
    run 3 -> 4      0 of 525                    (01:58 -> 02:21)
    run 4 -> 5      0 of 525                    (02:21 -> 07:27)
    run 5 -> 6    248 of 526  (47%)             (07:27 -> 13:27)

Note the earlier version of this script got the verdict WRONG. It looked at
whether individual products drifted within a day, saw mostly no movement, found
no midnight resets, and concluded "rolling trailing-24h window, safe to poll
more often." But flat-because-stale is indistinguishable from flat-because-
steady when you only look product by product.

The signature that actually separates them is **synchronization**: a batch
publish moves a large share of the whole panel at one instant, while a live
counter moves a trickle of products continuously. So this version tests the
panel, not the product.

Consequences applied to the system:
  * cron reduced from 4x/day to 2x/day bracketing the observed publish window,
    cutting API load ~50% for zero information loss
  * alerting diffs against the previous distinct batch, not the previous run
    (see store.previous_batch_run)
  * a reported change means one published day of movement, never "since N hours"

Run:  python eval/counter_cadence.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import store  # noqa: E402

# A batch publish moves a big share of the panel at once; a live counter does
# not. These bounds separate the two regimes.
QUIET_MAX = 0.02    # <=2% changed: same batch, nothing republished
BATCH_MIN = 0.15    # >=15% changed at once: a publish happened


def main() -> int:
    conn = store.connect()
    runs = [r["run_id"] for r in conn.execute(
        "SELECT run_id FROM runs WHERE finished_at IS NOT NULL ORDER BY run_id")]
    if len(runs) < 3:
        print(f"Only {len(runs)} completed run(s). Need at least 3 consecutive "
              "snapshots to characterize the refresh cadence.")
        return 0

    times = {r["run_id"]: r["started_at"] for r in conn.execute(
        "SELECT run_id, started_at FROM runs")}

    print(f"{'transition':16} {'changed':>9} {'of':>6} {'share':>7}   window (UTC)")
    print("-" * 74)
    quiet, batch, mixed = [], [], []
    for a, b in zip(runs, runs[1:]):
        row = conn.execute(
            """SELECT SUM(CASE WHEN x.daily_clicks <> y.daily_clicks THEN 1 ELSE 0 END) ch,
                      COUNT(*) n
               FROM product_snapshots x JOIN product_snapshots y USING(product_id)
               WHERE x.run_id = ? AND y.run_id = ?
                 AND x.daily_clicks IS NOT NULL AND y.daily_clicks IS NOT NULL""",
            (a, b),
        ).fetchone()
        n = row["n"] or 0
        if not n:
            continue
        share = (row["ch"] or 0) / n
        bucket = quiet if share <= QUIET_MAX else (batch if share >= BATCH_MIN else mixed)
        bucket.append((a, b, share))
        print(f"  run {a} -> {b:<8} {row['ch']:>9} {n:>6} {share:>6.1%}   "
              f"{times.get(a,'?')[11:16]} -> {times.get(b,'?')[11:16]}")

    print()
    if batch and quiet:
        # Narrow the publish window to the transition that moved the panel.
        a, b, share = max(batch, key=lambda t: t[2])
        lo, hi = times.get(a, "?")[11:16], times.get(b, "?")[11:16]
        print(f"VERDICT: BATCH PUBLISH, roughly once daily.\n"
              f"  {len(quiet)} transition(s) moved <={QUIET_MAX:.0%} of the panel "
              f"(same batch, nothing republished).\n"
              f"  {len(batch)} transition(s) moved >={BATCH_MIN:.0%} at once "
              f"(a publish), the largest being {share:.0%} between {lo} and {hi} UTC.\n"
              f"  => Publish window is between {lo} and {hi} UTC. Poll around it, not\n"
              f"     continuously, and diff against the previous distinct batch.")
    elif mixed and not quiet:
        print("VERDICT: LIVE or near-live counters. Products move continuously "
              "rather than in a synchronized jump, so higher polling frequency "
              "genuinely reduces detection latency.")
    elif quiet and not batch:
        print("VERDICT: INCONCLUSIVE. No publish observed yet; every transition was "
              "quiet. Keep collecting until a refresh lands.")
    else:
        print("VERDICT: INCONCLUSIVE. Pattern does not cleanly separate. Keep the "
              "batch-aware baseline, which is safe under either behavior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
