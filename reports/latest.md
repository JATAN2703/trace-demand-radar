# TRACE Demand Radar

Run `143`, compared against run 142 (previous upstream batch).

> The source republishes its click counters as a once-daily batch (measured: zero of 525 products changed across five snapshots spanning 23:27-07:27 UTC, then 248 of 526 changed at once at 13:27). Deltas below are therefore one publish apart, so a change means one day of movement, not the elapsed wall-clock time between runs.
490 dress products from 9 creators across 108 collections. 55 cleared the volume floor, 46 are in play (rising, peaking or sustained).

## Alerts

- **accelerating** - Thalia Dress (Retrofete) acceleration rose +0.802 to 1.963 since the last run
- **trajectory_change** - Thalia Dress (Retrofete) peaking -> rising
- **new_entrant** - Mimi Dress (STAUD) entered the top 10 at #2 (gap 0.393, rising)
- **new_entrant** - Anchored Floor Length Dress (Third Form) entered the top 10 at #3 (gap 0.3857, rising)
- **accelerating** - Anchored Floor Length Dress (Third Form) acceleration rose +3.875 to 4.511 since the last run
- **suppressed** -  28 further threshold crossings not shown; raise MAX_ALERTS to see them.

## In play, ranked by priority

Rising, peaking, or sustained (especially popular recently), ordered by priority = gap x price fit x occasion weight. Targeting is TRACE's stated focus: contemporary-to-premium occasionwear, roughly $400 to $1,000.

| # | Product | Brand | $ | Fit | Occasion | State | Accel | Creators | Daily | Supply | Gap | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Thalia Dress | Retrofete | 648.0 | 1.0 | occasion | rising | 1.963 | 1 | 136 | unmeasured | 0.4275 | 0.4275 |
| 2 | Mimi Dress | STAUD | 450.0 | 1.0 | unknown | rising | 2.808 | 1 | 69 | unmeasured | 0.393 | 0.3144 |
| 3 | Anchored Floor Length Dress | Third Form | 420.0 | 1.0 | unknown | rising | 4.511 | 1 | 29 | unmeasured | 0.3857 | 0.3086 |
| 4 | The Pieta Maxi Dress | Solace London | 860.0 | 1.0 | occasion | rising | 1.929 | 1 | 27 | unmeasured | 0.2981 | 0.2981 |
| 5 | Freda Silk Dress | STAUD | 795.0 | 1.0 | unknown | rising | 1.924 | 1 | 36 | unmeasured | 0.3296 | 0.2637 |
| 6 | Lace Off Shoulder Mini Dress | Mac Duggal | 898.0 | 1.0 | unknown | rising | 2.827 | 1 | 21 | unmeasured | 0.3228 | 0.2582 |
| 7 | Florencia Maxi Dress | De La Vali | 985.0 | 1.0 | unknown | rising | 2.164 | 1 | 17 | unmeasured | 0.2968 | 0.2374 |
| 8 | Josie Bodice Midi Dress | ALÉMAIS | 690.0 | 1.0 | unknown | peaking | 1.024 | 1 | 37 | unmeasured | 0.2899 | 0.2319 |
| 9 | Izel Cape Gown                  | SIMKHAI | 747.0 | 1.0 | unknown | peaking | 1.167 | 1 | 11 | unmeasured | 0.2776 | 0.2221 |
| 10 | Mynah Maxi Dress | Deme by Gabriella | 482.0 | 1.0 | unknown | rising | 1.936 | 1 | 13 | unmeasured | 0.2687 | 0.215 |

## Past peak (what a retrospective report would wrongly surface)

High all-time volume, thin recent activity. Listed so the contrast is explicit: these are the products a 'most popular dresses' report would lead with, and they are exactly the ones TRACE should not organize demand around now.

| Product | Brand | Total clicks | Monthly | Weekly | Week vs month |
|---|---|---|---|---|---|
| Audience Satin Mini Halter Dress | Ten | 15428 | 1875 | 69 | 0.158 |
| Fawn Silk Maxi Dress | STAUD | 4069 | 867 | 49 | 0.242 |

## Sources unavailable this run

- https://poshmark.com/brand/ONE/OF-Women-Dresses -> HTTP 404

_Supply shown as `unmeasured` is not the same as zero; those rows are scored at neutral supply so an unchecked item cannot masquerade as a confirmed gap._