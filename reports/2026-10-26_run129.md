# TRACE Demand Radar

Run `129`, compared against run 128 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
754 dress products from 9 creators across 108 collections. 74 cleared the volume floor, 69 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - Penelope Backless Satin Gown (Sau Lee) entered the top 10 at #2 (gap 0.3723, rising)
- **accelerating** - Penelope Backless Satin Gown (Sau Lee) acceleration rose +2.725 to 3.145 since the last run
- **trajectory_change** - Penelope Backless Satin Gown (Sau Lee) insufficient_volume -> rising
- **new_entrant** - Bondera Sequin Dress (Retrofete) entered the top 10 at #4 (gap 0.4446, rising)
- **trajectory_change** - Bondera Sequin Dress (Retrofete) insufficient_volume -> rising
- **suppressed** -  28 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ano Layered Raffia Dress | Kilentar | 750.0 | 1.0 | occasion | sustained | 0.498 | 1 | 42 | 8 (manual) | 0.3957 | 0.3957 |
| 2 | Penelope Backless Satin Gown | Sau Lee | 595.0 | 1.0 | occasion | rising | 3.145 | 1 | 31 | unmeasured | 0.3723 | 0.3723 |
| 3 | Vinicia Dress | Retrofete | 598.0 | 1.0 | occasion | rising | 1.596 | 1 | 26 | unmeasured | 0.3649 | 0.3649 |
| 4 | Bondera Sequin Dress | Retrofete | 898.0 | 1.0 | unknown | rising | 6.786 | 1 | 413 | unmeasured | 0.4446 | 0.3557 |
| 5 | Charli Silk Dress | STAUD | 750.0 | 1.0 | occasion | sustained | 0.59 | 1 | 180 | unmeasured | 0.3522 | 0.3522 |
| 6 | Dahlia Strapless Maxi Dress | Bronx and Banco | 826.0 | 1.0 | occasion | peaking | 0.896 | 1 | 16 | unmeasured | 0.3201 | 0.3201 |
| 7 | Daniela Silk Dress | Reformation | 398.0 | 0.992 | occasion | peaking | 1.328 | 1 | 26 | unmeasured | 0.3079 | 0.3054 |
| 8 | Paloma Maxi Dress | BAOBAB | 375.0 | 0.9 | occasion | rising | 2.196 | 1 | 16 | unmeasured | 0.3322 | 0.299 |
| 9 | Sabela Maxi Dress | De La Vali | 780.0 | 1.0 | unknown | rising | 4.511 | 1 | 29 | unmeasured | 0.3704 | 0.2963 |
| 10 | The Plunge Drape Gown | Heiress Beverly Hills | 368.0 | 0.872 | occasion | peaking | 1.31 | 1 | 32 | unmeasured | 0.3328 | 0.2902 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Audience Satin Mini Halter Dress | Ten | 15359 | 1927 | 59 | 0.131 |
| Cali Knit Dress | Reformation | 12038 | 5018 | 311 | 0.266 |
| Side Pleated Midi Dress  | LOFT | 1784 | 1195 | 71 | 0.255 |

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._