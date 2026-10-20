# TRACE Demand Radar

Run `117`, compared against run 116 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
711 dress products from 9 creators across 108 collections. 62 cleared the volume floor, 51 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Mini Dress Sleeveless (Hemant & Nandita) entered the top 10 at #2 (gap 0.4243, rising)
- **trajectory_change** - Mini Dress Sleeveless (Hemant & Nandita) insufficient_volume -> rising
- **new_entrant** - Dahlia Strapless Maxi Dress (Bronx and Banco) entered the top 10 at #3 (gap 0.4155, rising)
- **new_entrant** - Madalena Dress (Arcina Ori) entered the top 10 at #4 (gap 0.4099, rising)
- **accelerating** - Madalena Dress (Arcina Ori) acceleration rose +2.567 to 3.234 since the last run
- **suppressed** -  23 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ano Layered Raffia Dress | Kilentar | 750.0 | 1.0 | occasion | rising | 1.806 | 1 | 256 | 8 (manual) | 0.5614 | 0.5614 |
| 2 | Mini Dress Sleeveless | Hemant & Nandita | 398.0 | 0.992 | occasion | rising | 6.983 | 1 | 423 | unmeasured | 0.4243 | 0.4209 |
| 3 | Dahlia Strapless Maxi Dress | Bronx and Banco | 826.0 | 1.0 | occasion | rising | 3.761 | 1 | 72 | unmeasured | 0.4155 | 0.4155 |
| 4 | Madalena Dress | Arcina Ori | 560.0 | 1.0 | occasion | rising | 3.234 | 1 | 79 | unmeasured | 0.4099 | 0.4099 |
| 5 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | rising | 1.506 | 1 | 341 | unmeasured | 0.3818 | 0.3818 |
| 6 | Mock Neck Long Sleeve Lace Gown | Mac Duggal | 498.0 | 1.0 | occasion | peaking | 0.802 | 1 | 30 | unmeasured | 0.3441 | 0.3441 |
| 7 | Visions Lace Maxi Dress | Third Form | 420.0 | 1.0 | occasion | peaking | 1.131 | 1 | 21 | unmeasured | 0.3115 | 0.3115 |
| 8 | Kira Draped Silk Maxi Dress | STAUD | 795.0 | 1.0 | going_out | rising | 1.906 | 1 | 1210 | unmeasured | 0.4434 | 0.3104 |
| 9 | Reformation Frankie Dress | Reformation | 348.0 | 0.792 | occasion | rising | 1.429 | 2 | 110 | unmeasured | 0.377 | 0.2986 |
| 10 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | sustained | 0.753 | 1 | 24 | unmeasured | 0.2937 | 0.2937 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Satin Silk Dress | DÔEN | 38301 | 16563 | 203 | 0.053 |
| Cali Knit Dress | Reformation | 11764 | 6306 | 430 | 0.292 |
| Tiffany Fringe Maxi Dress | MESHKI | 11520 | 4259 | 262 | 0.264 |
| Side Pleated Midi Dress  | LOFT | 1727 | 1727 | 111 | 0.275 |
| Clash Sail Silk Maxi Dress | ZIMMERMANN | 713 | 711 | 47 | 0.283 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._