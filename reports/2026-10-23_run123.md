# TRACE Demand Radar

Run `123`, compared against run 122 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
714 dress products from 9 creators across 108 collections. 67 cleared the volume floor, 62 are in play (rising, peaking or sustained).

## Alerts

- **trajectory_change** - Charli Silk Dress (STAUD) rising -> peaking
- **new_entrant** - Leilani Tiered Lace Midi Dress (Retrofete) entered the top 10 at #3 (gap 0.3841, rising)
- **accelerating** - Leilani Tiered Lace Midi Dress (Retrofete) acceleration rose +3.478 to 5.811 since the last run
- **trajectory_change** - Leilani Tiered Lace Midi Dress (Retrofete) insufficient_volume -> rising
- **new_entrant** - Exclusive Devlyn Satin Gown (Significant Other) entered the top 10 at #4 (gap 0.4309, rising)
- **suppressed** -  43 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ano Layered Raffia Dress | Kilentar | 750.0 | 1.0 | occasion | sustained | 0.256 | 1 | 40 | 8 (manual) | 0.4442 | 0.4442 |
| 2 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | peaking | 1.316 | 1 | 431 | unmeasured | 0.3869 | 0.3869 |
| 3 | Leilani Tiered Lace Midi Dress | Retrofete | 858.0 | 1.0 | occasion | rising | 5.811 | 1 | 44 | unmeasured | 0.3841 | 0.3841 |
| 4 | Exclusive Devlyn Satin Gown | Significant Other | 495.0 | 1.0 | unknown | rising | 4.008 | 1 | 138 | unmeasured | 0.4309 | 0.3447 |
| 5 | Patrizia Dress | Cult Gaia | 698.0 | 1.0 | occasion | rising | 2.333 | 1 | 31 | unmeasured | 0.3394 | 0.3394 |
| 6 | Liela Sequin Dress | Retrofete | 698.0 | 1.0 | occasion | rising | 2.932 | 1 | 31 | unmeasured | 0.3392 | 0.3392 |
| 7 | Viviana Dress | STAUD | 695.0 | 1.0 | unknown | rising | 3.829 | 1 | 99 | unmeasured | 0.4155 | 0.3324 |
| 8 | Visions Lace Maxi Dress | Third Form | 420.0 | 1.0 | occasion | peaking | 1.176 | 1 | 20 | unmeasured | 0.3103 | 0.3103 |
| 9 | Reformation Frankie Dress | Reformation | 348.0 | 0.792 | occasion | rising | 1.703 | 1 | 137 | unmeasured | 0.3857 | 0.3055 |
| 10 | Tie Gown | L'IDÉE | 549.0 | 1.0 | occasion | peaking | 1.235 | 1 | 15 | unmeasured | 0.2995 | 0.2995 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Cali Knit Dress | Reformation | 11861 | 5175 | 232 | 0.192 |
| Tiffany Fringe Maxi Dress | MESHKI | 11626 | 3956 | 210 | 0.228 |
| Side Pleated Midi Dress  | LOFT | 1758 | 1758 | 100 | 0.244 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._