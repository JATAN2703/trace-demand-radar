# TRACE Demand Radar

Run `141`, compared against run 140 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
487 dress products from 9 creators across 108 collections. 49 cleared the volume floor, 42 are in play (rising, peaking or sustained).

## Alerts

- **new_entrant** - The Pieta Maxi Dress (Solace London) entered the top 10 at #2 (gap 0.3404, rising)
- **accelerating** - The Pieta Maxi Dress (Solace London) acceleration rose +2.057 to 2.965 since the last run
- **trajectory_change** - The Pieta Maxi Dress (Solace London) insufficient_volume -> rising
- **new_entrant** - Abbey Jersey Dress (Junie) entered the top 10 at #3 (gap 0.321, rising)
- **trajectory_change** - Abbey Jersey Dress (Junie) insufficient_volume -> rising
- **suppressed** -  18 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Thalia Dress | Retrofete | 648.0 | 1.0 | occasion | peaking | 1.161 | 1 | 70 | unmeasured | 0.3785 | 0.3785 |
| 2 | The Pieta Maxi Dress | Solace London | 860.0 | 1.0 | occasion | rising | 2.965 | 1 | 36 | unmeasured | 0.3404 | 0.3404 |
| 3 | Abbey Jersey Dress | Junie | 526.0 | 1.0 | unknown | rising | 3.182 | 1 | 20 | unmeasured | 0.321 | 0.2568 |
| 4 | Izel Cape Gown                  | SIMKHAI | 747.0 | 1.0 | unknown | rising | 1.806 | 1 | 16 | unmeasured | 0.3067 | 0.2454 |
| 5 | Josie Bodice Midi Dress | ALÉMAIS | 690.0 | 1.0 | unknown | sustained | 0.53 | 1 | 24 | unmeasured | 0.2651 | 0.2121 |
| 6 | Mock Neck Long Sleeve Lace Gown | Mac Duggal | 498.0 | 1.0 | unknown | rising | 2.019 | 1 | 15 | unmeasured | 0.2647 | 0.2118 |
| 7 | The Cora Dress | Réalisation Par | 360.0 | 0.84 | unknown | sustained | 0.598 | 1 | 37 | 25 (manual) | 0.3061 | 0.2057 |
| 8 | Amara Bustier Pleated Fit & Flare  | HUTCH | 348.0 | 0.792 | occasion | peaking | 1.05 | 1 | 9 | unmeasured | 0.2571 | 0.2036 |
| 9 | Brynhild Strapless Maxi Dress | SAYLOR | 264.0 | 0.456 | occasion | rising | 6.748 | 1 | 751 | unmeasured | 0.4289 | 0.1956 |
| 10 | Mynah Maxi Dress | Deme by Gabriella | 482.0 | 1.0 | unknown | rising | 1.5 | 1 | 9 | unmeasured | 0.2415 | 0.1932 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Audience Satin Mini Halter Dress | Ten | 15419 | 1877 | 71 | 0.162 |
| Viviana Dress | STAUD | 5360 | 1153 | 79 | 0.294 |
| Puff Sleeve Valentina Mini Dress | Hyacinth House | 4545 | 4044 | 261 | 0.277 |

## Sources unavailable this run

- https://poshmark.com/brand/ONE/OF-Women-Dresses -> HTTP 404

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._