# TRACE Demand Radar

Run `126`, compared against run 124 (previous upstream batch, skipped 1 same-batch run(s)).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
711 dress products from 9 creators across 108 collections. 71 cleared the volume floor, 60 are in play (rising, peaking or sustained).

## Alerts

- **accelerating** - Visions Lace Maxi Dress (Third Form) acceleration rose +0.697 to 1.873 since the last run
- **trajectory_change** - Visions Lace Maxi Dress (Third Form) peaking -> rising
- **new_entrant** - Salter Mini Dress (Hunter Bell) entered the top 10 at #5 (gap 0.3992, rising)
- **accelerating** - Salter Mini Dress (Hunter Bell) acceleration rose +2.673 to 3.192 since the last run
- **trajectory_change** - Salter Mini Dress (Hunter Bell) insufficient_volume -> rising
- **suppressed** -  23 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ano Layered Raffia Dress | Kilentar | 750.0 | 1.0 | occasion | sustained | 0.365 | 1 | 59 | 8 (manual) | 0.4633 | 0.4633 |
| 2 | Visions Lace Maxi Dress | Third Form | 420.0 | 1.0 | occasion | rising | 1.873 | 1 | 38 | unmeasured | 0.3569 | 0.3569 |
| 3 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | sustained | 0.587 | 1 | 189 | unmeasured | 0.3568 | 0.3568 |
| 4 | Exclusive Devlyn Satin Gown | Significant Other | 495.0 | 1.0 | unknown | rising | 2.632 | 1 | 138 | unmeasured | 0.4084 | 0.3267 |
| 5 | Salter Mini Dress | Hunter Bell | 495.0 | 1.0 | unknown | rising | 3.192 | 1 | 57 | unmeasured | 0.3992 | 0.3194 |
| 6 | Izel Cape Gown                  | SIMKHAI | 747.0 | 1.0 | unknown | rising | 2.878 | 2 | 37 | unmeasured | 0.3864 | 0.3091 |
| 7 | Gaspard Mini Dress | REVOLVE LOS ANGELES | 450.0 | 1.0 | going_out | rising | 5.563 | 1 | 120 | unmeasured | 0.4269 | 0.2988 |
| 8 | Marsla Gown  | Cult Gaia | 1198.0 | 0.868 | occasion | peaking | 1.148 | 1 | 51 | unmeasured | 0.3279 | 0.2846 |
| 9 | Daniela Silk Dress | Reformation | 398.0 | 0.992 | occasion | peaking | 0.895 | 1 | 17 | unmeasured | 0.2814 | 0.2791 |
| 10 | Nellcote Anniversary Dress  | DÔEN | 698.0 | 1.0 | occasion | peaking | 1.016 | 1 | 9 | unmeasured | 0.2691 | 0.2691 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Cali Knit Dress | Reformation | 11913 | 5092 | 260 | 0.219 |
| Tiffany Fringe Maxi Dress | MESHKI | 11649 | 3447 | 201 | 0.25 |
| Side Pleated Midi Dress  | LOFT | 1768 | 1534 | 103 | 0.288 |
| Rune Dress | Reformation | 848 | 627 | 41 | 0.28 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._