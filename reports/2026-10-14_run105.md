# TRACE Demand Radar

Run `105`, compared against run 104 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
628 dress products from 9 creators across 108 collections. 60 cleared the volume floor, 49 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Ambrosia Dress (Retrofete) entered the top 10 at #1 (gap 0.4303, rising)
- **accelerating** - Portia Silk Dress (STAUD) acceleration rose +0.954 to 2.004 since the last run
- **trajectory_change** - Portia Silk Dress (STAUD) peaking -> rising
- **new_entrant** - Charlotte Gown (ALÉMAIS) entered the top 10 at #5 (gap 0.3409, rising)
- **accelerating** - Charlotte Gown (ALÉMAIS) acceleration rose +1.748 to 3.588 since the last run
- **suppressed** -  13 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ambrosia Dress | Retrofete | 798.0 | 1.0 | occasion | rising | 4.242 | 1 | 143 | unmeasured | 0.4303 | 0.4303 |
| 2 | Ano Layered Raffia Dress | Kilentar | 1082.0 | 0.945 | occasion | peaking | 1.202 | 1 | 45 | 8 (manual) | 0.4023 | 0.3803 |
| 3 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | sustained | 0.651 | 1 | 222 | unmeasured | 0.3726 | 0.3726 |
| 4 | Portia Silk Dress | STAUD | 695.0 | 1.0 | occasion | rising | 2.004 | 1 | 77 | unmeasured | 0.3515 | 0.3515 |
| 5 | Charlotte Gown | ALÉMAIS | 790.0 | 1.0 | occasion | rising | 3.588 | 1 | 326 | 47 (poshmark) | 0.3409 | 0.3409 |
| 6 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | sustained | 0.72 | 1 | 39 | unmeasured | 0.3301 | 0.3301 |
| 7 | Zara Ruched Long Dress | HEMANT AND NANDITA | 598.0 | 1.0 | occasion | peaking | 0.801 | 1 | 35 | unmeasured | 0.3264 | 0.3264 |
| 8 | Avery Dress  | Arcina Ori | 420.0 | 1.0 | occasion | peaking | 1.291 | 1 | 19 | unmeasured | 0.3125 | 0.3125 |
| 9 | Strapless Mikado Ball Gown | Mac Duggal | 498.0 | 1.0 | unknown | rising | 4.491 | 1 | 34 | unmeasured | 0.3709 | 0.2967 |
| 10 | Kira Draped Silk Maxi Dress | STAUD | 795.0 | 1.0 | going_out | rising | 1.357 | 1 | 415 | unmeasured | 0.4192 | 0.2934 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Satin Silk Dress | DÔEN | 38135 | 16964 | 524 | 0.132 |
| Marta Gown | Sachin & Babi | 30665 | 20224 | 148 | 0.031 |
| The Plunge Drape Gown | Heiress Beverly Hills | 22098 | 4920 | 89 | 0.078 |
| Cali Knit Dress | Reformation | 11476 | 7954 | 426 | 0.23 |
| Chantelle Maxi Dress | Show Me Your Mumu | 5572 | 4025 | 77 | 0.082 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._