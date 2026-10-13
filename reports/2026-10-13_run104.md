# TRACE Demand Radar

Run `104`, compared against run 103 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
616 dress products from 9 creators across 108 collections. 59 cleared the volume floor, 50 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Zara Ruched Long Dress (HEMANT AND NANDITA) entered the top 10 at #2 (gap 0.4174, rising)
- **accelerating** - Zara Ruched Long Dress (HEMANT AND NANDITA) acceleration rose +4.809 to 5.949 since the last run
- **trajectory_change** - Zara Ruched Long Dress (HEMANT AND NANDITA) insufficient_volume -> rising
- **new_entrant** - Avery Dress  (Arcina Ori) entered the top 10 at #3 (gap 0.4013, rising)
- **accelerating** - Avery Dress  (Arcina Ori) acceleration rose +2.617 to 3.354 since the last run
- **suppressed** -  27 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | rising | 2.644 | 1 | 139 | unmeasured | 0.43 | 0.43 |
| 2 | Zara Ruched Long Dress | HEMANT AND NANDITA | 598.0 | 1.0 | occasion | rising | 5.949 | 1 | 232 | unmeasured | 0.4174 | 0.4174 |
| 3 | Avery Dress  | Arcina Ori | 420.0 | 1.0 | occasion | rising | 3.354 | 1 | 46 | unmeasured | 0.4013 | 0.4013 |
| 4 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | sustained | 0.762 | 1 | 258 | unmeasured | 0.3727 | 0.3727 |
| 5 | Ano Layered Raffia Dress | Kilentar | 1079.0 | 0.947 | occasion | peaking | 0.953 | 1 | 32 | 8 (manual) | 0.3717 | 0.3521 |
| 6 | Visions Lace Maxi Dress | Third Form | 420.0 | 1.0 | occasion | rising | 2.026 | 1 | 33 | unmeasured | 0.3488 | 0.3488 |
| 7 | Kira Draped Silk Maxi Dress | STAUD | 795.0 | 1.0 | going_out | rising | 1.476 | 1 | 379 | unmeasured | 0.4175 | 0.2922 |
| 8 | Portia Silk Dress | STAUD | 695.0 | 1.0 | occasion | peaking | 1.05 | 1 | 30 | unmeasured | 0.2884 | 0.2884 |
| 9 | Himalia Maxi Dress in Antique Tull | De La Vali | 980.0 | 1.0 | occasion | sustained | 0.714 | 1 | 21 | unmeasured | 0.2824 | 0.2824 |
| 10 | Kelsa Dress | Retrofete | 385.0 | 0.94 | occasion | peaking | 1.055 | 1 | 33 | unmeasured | 0.2917 | 0.2742 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Satin Silk Dress | DÔEN | 38098 | 16965 | 597 | 0.151 |
| Marta Gown | Sachin & Babi | 30689 | 20230 | 150 | 0.032 |
| The Plunge Drape Gown | Heiress Beverly Hills | 22088 | 4916 | 87 | 0.076 |
| Phare Silk Maxi Dress | STAUD | 8743 | 1436 | 76 | 0.227 |
| Chantelle Maxi Dress | Show Me Your Mumu | 5554 | 4014 | 75 | 0.08 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._