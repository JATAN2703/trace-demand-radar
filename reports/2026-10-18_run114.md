# TRACE Demand Radar

Run `114`, compared against run 113 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
765 dress products from 9 creators across 108 collections. 66 cleared the volume floor, 58 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Aura Halter Neck Maxi Dress (Hemant & Nandita) entered the top 10 at #1 (gap 0.4232, rising)
- **accelerating** - Aura Halter Neck Maxi Dress (Hemant & Nandita) acceleration rose +4.397 to 6.306 since the last run
- **trajectory_change** - Aura Halter Neck Maxi Dress (Hemant & Nandita) insufficient_volume -> rising
- **new_entrant** - Visions Lace Maxi Dress (Third Form) entered the top 10 at #5 (gap 0.3139, peaking)
- **trajectory_change** - Visions Lace Maxi Dress (Third Form) cooling -> peaking
- **suppressed** -  35 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Aura Halter Neck Maxi Dress | Hemant & Nandita | 403.0 | 1.0 | occasion | rising | 6.306 | 1 | 100 | unmeasured | 0.4232 | 0.4232 |
| 2 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | peaking | 0.975 | 1 | 226 | unmeasured | 0.364 | 0.364 |
| 3 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | sustained | 0.588 | 1 | 35 | unmeasured | 0.328 | 0.328 |
| 4 | Ano Layered Raffia Dress | Kilentar | 1088.0 | 0.941 | occasion | sustained | 0.433 | 1 | 13 | 8 (manual) | 0.3336 | 0.314 |
| 5 | Visions Lace Maxi Dress | Third Form | 420.0 | 1.0 | occasion | peaking | 1.077 | 1 | 22 | unmeasured | 0.3139 | 0.3139 |
| 6 | Mock Neck Long Sleeve Lace Gown | Mac Duggal | 498.0 | 1.0 | occasion | sustained | 0.33 | 1 | 11 | unmeasured | 0.3029 | 0.3029 |
| 7 | Kira Draped Silk Maxi Dress | STAUD | 795.0 | 1.0 | going_out | rising | 1.558 | 1 | 596 | unmeasured | 0.4169 | 0.2918 |
| 8 | Thalia Dress | Retrofete | 648.0 | 1.0 | occasion | peaking | 1.141 | 1 | 15 | unmeasured | 0.2843 | 0.2843 |
| 9 | Madalena Dress | Arcina Ori | 560.0 | 1.0 | occasion | peaking | 1.017 | 1 | 17 | unmeasured | 0.2797 | 0.2797 |
| 10 |  Katya Off-Shoulders Stretch-Woven | Deme by Gabriella | 410.0 | 1.0 | occasion | rising | 1.4 | 1 | 9 | unmeasured | 0.2735 | 0.2735 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Satin Silk Dress | DÔEN | 38252 | 16553 | 283 | 0.073 |
| The Plunge Drape Gown | Heiress Beverly Hills | 22139 | 4739 | 65 | 0.059 |
| Cali Knit Dress | Reformation | 11689 | 6401 | 446 | 0.299 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._