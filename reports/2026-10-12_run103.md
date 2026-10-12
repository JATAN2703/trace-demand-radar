# TRACE Demand Radar

Run `103`, compared against run 102 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
669 dress products from 9 creators across 108 collections. 62 cleared the volume floor, 52 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Darcy Dress (Arcina Ori) entered the top 10 at #1 (gap 0.4488, rising)
- **accelerating** - Darcy Dress (Arcina Ori) acceleration rose +3.081 to 3.599 since the last run
- **trajectory_change** - Darcy Dress (Arcina Ori) cooling -> rising
- **new_entrant** - Portia Silk Dress (STAUD) entered the top 10 at #2 (gap 0.4368, rising)
- **accelerating** - Portia Silk Dress (STAUD) acceleration rose +3.298 to 4.298 since the last run
- **suppressed** -  29 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Darcy Dress | Arcina Ori | 480.0 | 1.0 | occasion | rising | 3.599 | 1 | 127 | unmeasured | 0.4488 | 0.4488 |
| 2 | Portia Silk Dress | STAUD | 695.0 | 1.0 | occasion | rising | 4.298 | 1 | 105 | unmeasured | 0.4368 | 0.4368 |
| 3 | Ano Layered Raffia Dress | Kilentar | 1081.0 | 0.946 | occasion | rising | 1.615 | 1 | 51 | 8 (manual) | 0.4129 | 0.3906 |
| 4 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | peaking | 1.196 | 1 | 390 | unmeasured | 0.3874 | 0.3874 |
| 5 | Ashika Dress | Cult Gaia | 998.0 | 1.0 | occasion | rising | 3.97 | 1 | 38 | unmeasured | 0.3861 | 0.3861 |
| 6 | Helena Dress | Arcina Ori | 480.0 | 1.0 | occasion | peaking | 0.97 | 1 | 28 | unmeasured | 0.3535 | 0.3535 |
| 7 | The Sabine Dress in Silk Chiffon | Helsa | 497.0 | 1.0 | occasion | rising | 2.5 | 1 | 15 | unmeasured | 0.3242 | 0.3242 |
| 8 | Lorela Dress | Rat & Boa | 560.0 | 1.0 | occasion | rising | 1.68 | 1 | 18 | unmeasured | 0.3132 | 0.3132 |
| 9 | Bea-Silk Organza Boat Neck Midi Dr | ILA | 1100.0 | 0.933 | occasion | rising | 2.077 | 1 | 27 | unmeasured | 0.3207 | 0.2993 |
| 10 | Marsla Gown  | Cult Gaia | 1198.0 | 0.868 | occasion | rising | 1.556 | 2 | 62 | unmeasured | 0.3444 | 0.2989 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Fiona Dress | DÔEN | 38048 | 16945 | 683 | 0.173 |
| Marta Gown | Sachin & Babi | 30675 | 20227 | 158 | 0.033 |
| Riti Dress | Cult Gaia | 6826 | 1050 | 68 | 0.278 |
| Chantelle Maxi Dress | Show Me Your Mumu | 5533 | 3999 | 73 | 0.078 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._