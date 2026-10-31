# TRACE Demand Radar

Run `139`, compared against run 138 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
564 dress products from 9 creators across 108 collections. 53 cleared the volume floor, 42 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Fringed Satin Maxi Dress (Fleur du Mal) entered the top 10 at #1 (gap 0.3821, rising)
- **accelerating** - Fringed Satin Maxi Dress (Fleur du Mal) acceleration rose +3.835 to 4.571 since the last run
- **trajectory_change** - Fringed Satin Maxi Dress (Fleur du Mal) insufficient_volume -> rising
- **new_entrant** - Belted Houndstooth Turtleneck Midi Dress (Norma Kamali) entered the top 10 at #4 (gap 0.4068, rising)
- **trajectory_change** - Belted Houndstooth Turtleneck Midi Dress (Norma Kamali) insufficient_volume -> rising
- **suppressed** -  16 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fringed Satin Maxi Dress | Fleur du Mal | 573.0 | 1.0 | occasion | rising | 4.571 | 1 | 32 | unmeasured | 0.3821 | 0.3821 |
| 2 | Thalia Dress | Retrofete | 598.0 | 1.0 | occasion | peaking | 1.089 | 1 | 63 | unmeasured | 0.3735 | 0.3735 |
| 3 | Avielle Dress | HUTCH | 374.0 | 0.896 | occasion | rising | 3.171 | 1 | 188 | unmeasured | 0.3801 | 0.3406 |
| 4 | Belted Houndstooth Turtleneck Midi | Norma Kamali | 445.0 | 1.0 | unknown | rising | 6.234 | 1 | 122 | unmeasured | 0.4068 | 0.3254 |
| 5 | Visions Lace Maxi Dress | Third Form | 420.0 | 1.0 | occasion | peaking | 0.818 | 1 | 9 | unmeasured | 0.2677 | 0.2677 |
| 6 | Kasai Mini Dress | De La Vali | 715.0 | 1.0 | going_out | rising | 1.75 | 1 | 11 | unmeasured | 0.3377 | 0.2364 |
| 7 | Josie Bodice Midi Dress | ALÉMAIS | 690.0 | 1.0 | unknown | peaking | 0.911 | 1 | 44 | unmeasured | 0.2927 | 0.2342 |
| 8 | Viviana Dress | STAUD | 695.0 | 1.0 | unknown | peaking | 1.227 | 1 | 17 | unmeasured | 0.2697 | 0.2158 |
| 9 | Rosa Dress | Arcina Ori | 340.0 | 0.76 | going_out | rising | 3.056 | 1 | 31 | unmeasured | 0.3932 | 0.2092 |
| 10 | Sana Dress | Diane von Furstenberg | 398.0 | 0.992 | unknown | peaking | 1.008 | 1 | 17 | unmeasured | 0.2535 | 0.2012 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| The Deep Plunge Mini Dress | Heiress Beverly Hills | 10766 | 6753 | 162 | 0.103 |
| Puff Sleeve Valentina Mini Dress | Hyacinth House | 4507 | 4017 | 272 | 0.29 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._