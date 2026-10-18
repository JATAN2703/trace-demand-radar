# TRACE Demand Radar

Run `113`, compared against run 110 (previous upstream batch, skipped 2 same-batch run(s)).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
696 dress products from 9 creators across 108 collections. 66 cleared the volume floor, 56 are in play (rising, peaking or sustained).

## Alerts

- **accelerating** - Charli Silk Dress (STAUD) acceleration rose +0.358 to 0.908 since the last run
- **trajectory_change** - Charli Silk Dress (STAUD) sustained -> peaking
- **new_entrant** - Lorela Dress (Rat & Boa) entered the top 10 at #9 (gap 0.303, rising)
- **accelerating** - Lorela Dress (Rat & Boa) acceleration rose +1.437 to 1.75 since the last run
- **trajectory_change** - Lorela Dress (Rat & Boa) insufficient_volume -> rising
- **suppressed** -  24 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ava Bustier Maxi Dress | Leo Lin | 835.0 | 1.0 | occasion | rising | 3.5 | 1 | 84 | unmeasured | 0.4424 | 0.4424 |
| 2 | Ambrosia Dress | Retrofete | 798.0 | 1.0 | occasion | rising | 1.362 | 1 | 94 | unmeasured | 0.4251 | 0.4251 |
| 3 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | peaking | 0.908 | 1 | 227 | unmeasured | 0.3651 | 0.3651 |
| 4 | Ano Layered Raffia Dress | Kilentar | 1088.0 | 0.941 | occasion | sustained | 0.607 | 1 | 19 | 8 (manual) | 0.3545 | 0.3337 |
| 5 | Marion Strapless Printed Midi Dres | ALÉMAIS | 590.0 | 1.0 | occasion | rising | 2.375 | 1 | 19 | unmeasured | 0.3286 | 0.3286 |
| 6 | Himalia Maxi Dress in Antique Tull | De La Vali | 980.0 | 1.0 | occasion | rising | 1.65 | 1 | 33 | unmeasured | 0.3123 | 0.3123 |
| 7 | Kyla Fringe Dress | Yellow the Label | 428.0 | 1.0 | occasion | peaking | 1.293 | 1 | 29 | unmeasured | 0.3066 | 0.3066 |
| 8 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | sustained | 0.357 | 1 | 20 | unmeasured | 0.3039 | 0.3039 |
| 9 | Lorela Dress | Rat & Boa | 560.0 | 1.0 | occasion | rising | 1.75 | 1 | 16 | unmeasured | 0.303 | 0.303 |
| 10 | Thalia Dress | Retrofete | 648.0 | 1.0 | occasion | rising | 1.511 | 1 | 19 | unmeasured | 0.3021 | 0.3021 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Satin Silk Dress | DÔEN | 38231 | 16566 | 345 | 0.089 |
| The Plunge Drape Gown | Heiress Beverly Hills | 22126 | 4732 | 59 | 0.053 |
| Cali Knit Dress | Reformation | 11653 | 6591 | 439 | 0.285 |
| Kleo One Shoulder Maxi Dress | Petal & Pup | 10029 | 4230 | 235 | 0.238 |
| Maxi Phare Silk Dress | STAUD | 8815 | 1315 | 90 | 0.293 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._