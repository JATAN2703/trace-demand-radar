# TRACE Demand Radar

Run `109`, compared against run 108 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
666 dress products from 9 creators across 108 collections. 60 cleared the volume floor, 47 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Ambrosia Dress (Retrofete) entered the top 10 at #1 (gap 0.4353, rising)
- **accelerating** - Ambrosia Dress (Retrofete) acceleration rose +2.698 to 2.757 since the last run
- **trajectory_change** - Ambrosia Dress (Retrofete) insufficient_volume -> rising
- **new_entrant** - Ava Bustier Maxi Dress (Leo Lin) entered the top 10 at #2 (gap 0.3972, rising)
- **accelerating** - Ava Bustier Maxi Dress (Leo Lin) acceleration rose +2.985 to 3.303 since the last run
- **suppressed** -  27 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ambrosia Dress | Retrofete | 798.0 | 1.0 | occasion | rising | 2.757 | 1 | 154 | unmeasured | 0.4353 | 0.4353 |
| 2 | Ava Bustier Maxi Dress | Leo Lin | 835.0 | 1.0 | occasion | rising | 3.303 | 1 | 42 | unmeasured | 0.3972 | 0.3972 |
| 3 | Porter Midi Dress | ALÉMAIS | 730.0 | 1.0 | occasion | rising | 5.306 | 1 | 47 | 28 (manual) | 0.3808 | 0.3808 |
| 4 | Himalia Maxi Dress in Antique Tull | De La Vali | 980.0 | 1.0 | occasion | rising | 2.846 | 1 | 50 | unmeasured | 0.3638 | 0.3638 |
| 5 | Ano Layered Raffia Dress | Kilentar | 1082.0 | 0.945 | occasion | sustained | 0.686 | 1 | 25 | 8 (manual) | 0.3717 | 0.3514 |
| 6 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | sustained | 0.55 | 1 | 153 | unmeasured | 0.3513 | 0.3513 |
| 7 | Kyla Fringe Dress | Yellow the Label | 428.0 | 1.0 | occasion | peaking | 1.341 | 1 | 50 | unmeasured | 0.3448 | 0.3448 |
| 8 | Marion Strapless Printed Midi Dres | ALÉMAIS | 590.0 | 1.0 | occasion | rising | 2.8 | 1 | 20 | unmeasured | 0.3435 | 0.3435 |
| 9 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | sustained | 0.574 | 1 | 32 | unmeasured | 0.3221 | 0.3221 |
| 10 | Indigo Twist Dress | SIR. | 490.0 | 1.0 | unknown | peaking | 1.1 | 1 | 36 | unmeasured | 0.3854 | 0.3083 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| The Cora Dress | Réalisation Par | 42075 | 3104 | 214 | 0.295 |
| Fiona Satin Silk Dress | DÔEN | 38212 | 16846 | 390 | 0.099 |
| Marta Gown | Sachin & Babi | 30622 | 20208 | 146 | 0.031 |
| Cali Knit Dress | Reformation | 11629 | 6733 | 464 | 0.295 |
| Kleo One Shoulder Maxi Dress | Petal & Pup | 9970 | 4262 | 254 | 0.255 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._