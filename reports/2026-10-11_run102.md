# TRACE Demand Radar

Run `102`, compared against run 100 (previous upstream batch, skipped 1 same-batch run(s)).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
660 dress products from 9 creators across 108 collections. 52 cleared the volume floor, 38 are in play (rising, peaking or sustained).

## Alerts

- **trajectory_change** - Charli Silk Dress (STAUD) rising -> peaking
- **trajectory_change** - Helena Dress (Arcina Ori) rising -> peaking
- **new_entrant** - Kelsa Dress (Retrofete) entered the top 10 at #9 (gap 0.2812, peaking)
- **trajectory_change** - House of Harlow 1960 x Revolve Hera Fringe Maxi Dress (House of Harlow 1960) rising -> peaking
- **accelerating** - Helsi x By Anthropologie Weddings Gloria Shift Dress (Helsi) acceleration rose +0.473 to 0.982 since the last run
- **suppressed** -  3 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | peaking | 1.215 | 1 | 353 | unmeasured | 0.3832 | 0.3832 |
| 2 | Helena Dress | Arcina Ori | 480.0 | 1.0 | occasion | peaking | 1.062 | 1 | 27 | unmeasured | 0.3491 | 0.3491 |
| 3 | Kyla Fringe Dress | Yellow the Label | 428.0 | 1.0 | occasion | sustained | 0.557 | 1 | 32 | unmeasured | 0.3427 | 0.3427 |
| 4 | Ano Layered Raffia Dress | Kilentar | 1081.0 | 0.946 | occasion | sustained | 0.798 | 1 | 22 | 8 (manual) | 0.344 | 0.3254 |
| 5 | Lorela Dress | Rat & Boa | 560.0 | 1.0 | occasion | rising | 1.898 | 1 | 16 | unmeasured | 0.3101 | 0.3101 |
| 6 | Charlotte Gown | ALÉMAIS | 790.0 | 1.0 | occasion | sustained | 0.189 | 1 | 25 | unmeasured | 0.3081 | 0.3081 |
| 7 | Kira Draped Silk Maxi Dress | STAUD | 795.0 | 1.0 | going_out | rising | 1.593 | 1 | 373 | unmeasured | 0.4324 | 0.3027 |
| 8 | Madalena Dress | Arcina Ori | 560.0 | 1.0 | occasion | sustained | 0.766 | 1 | 21 | unmeasured | 0.2857 | 0.2857 |
| 9 | Kelsa Dress | Retrofete | 698.0 | 1.0 | occasion | peaking | 0.891 | 1 | 28 | unmeasured | 0.2812 | 0.2812 |
| 10 | Alice Linen Mini Dress | POSSE | 330.0 | 0.72 | occasion | rising | 1.643 | 1 | 54 | unmeasured | 0.3784 | 0.2724 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Dress | DÔEN | 37969 | 16900 | 828 | 0.21 |
| Marta Gown | Sachin & Babi | 30633 | 20192 | 149 | 0.032 |
| Portia Silk Dress | STAUD | 9286 | 1877 | 56 | 0.128 |
| Riti Dress | Cult Gaia | 6805 | 1039 | 52 | 0.214 |
| Chantelle Maxi Dress | Show Me Your Mumu | 5525 | 3996 | 90 | 0.097 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._