# TRACE Demand Radar

Run `134`, compared against run 132 (previous upstream batch, skipped 1 same-batch run(s)).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
599 dress products from 9 creators across 108 collections. 67 cleared the volume floor, 55 are in play (rising, peaking or sustained).

## Alerts

- **trajectory_change** - Vinicia Dress (Retrofete) rising -> peaking
- **new_entrant** - Valencia Mini Dress (STAUD) entered the top 10 at #2 (gap 0.3957, rising)
- **accelerating** - Valencia Mini Dress (STAUD) acceleration rose +4.958 to 5.833 since the last run
- **trajectory_change** - Valencia Mini Dress (STAUD) insufficient_volume -> rising
- **trajectory_change** - Ano Layered Raffia Dress (Kilentar) sustained -> peaking
- **suppressed** -  22 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Vinicia Dress | Retrofete | 598.0 | 1.0 | occasion | peaking | 1.177 | 1 | 55 | unmeasured | 0.4042 | 0.4042 |
| 2 | Valencia Mini Dress | STAUD | 595.0 | 1.0 | occasion | rising | 5.833 | 1 | 40 | unmeasured | 0.3957 | 0.3957 |
| 3 | Pandorea Layered Maxi Dress | Aje | 695.0 | 1.0 | occasion | rising | 1.595 | 1 | 77 | unmeasured | 0.3884 | 0.3884 |
| 4 | Ano Layered Raffia Dress | Kilentar | 750.0 | 1.0 | occasion | peaking | 0.9 | 1 | 41 | 8 (manual) | 0.3835 | 0.3835 |
| 5 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | peaking | 1.314 | 1 | 379 | unmeasured | 0.3777 | 0.3777 |
| 6 | Thalia Dress | Retrofete | 648.0 | 1.0 | occasion | peaking | 1.158 | 1 | 43 | unmeasured | 0.3447 | 0.3447 |
| 7 | Rayna Embroidered Maxi Dress | Leo Lin | 1095.0 | 0.937 | occasion | rising | 2.397 | 1 | 25 | unmeasured | 0.3601 | 0.3373 |
| 8 | Petites Jillian Silk Dress | Reformation | 378.0 | 0.912 | occasion | sustained | 0.229 | 1 | 86 | unmeasured | 0.3611 | 0.3293 |
| 9 | Feather-Trim Sheer Kaftan | HUTCH | 398.0 | 0.992 | occasion | peaking | 0.868 | 1 | 59 | unmeasured | 0.3313 | 0.3286 |
| 10 | Kira Strapless Printed Satin A-Lin | BHLDN | 348.0 | 0.792 | occasion | rising | 3.909 | 1 | 43 | unmeasured | 0.3964 | 0.3139 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Bita Gown | Katie May | 18180 | 17567 | 101 | 0.025 |
| Cali Knit Dress | Reformation | 12119 | 4916 | 328 | 0.286 |
| Felicity Satin Asymmetric-Neck Maxi Dr | Club L London | 4917 | 1558 | 83 | 0.228 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._