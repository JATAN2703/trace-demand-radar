# TRACE Demand Radar

A near-real-time cross-platform fashion demand and liquidity radar, built for the TRACE Applied AI
Engineering exercise.

**Findings and recommendation: [`FINDINGS.md`](FINDINGS.md)**. Start there if you want the answer
rather than the machinery.
**What was and was not reachable: [`PROBE_LOG.md`](../Trace%20-%20Interview%20Prep/PROBE_LOG.md)**

---

## What it does

Tracks occasionwear dresses that creators are actively pushing, detects when one starts accelerating,
and ranks them by demand against available secondary supply, so the output is a decision, not a
dashboard.

It has run unattended twice daily since 22 August 2026, committing its own snapshots to this repo.
`reports/latest.md` is the current digest.

```
TikTok (MANUAL)  ──>  seed set of occasionwear creators
                        │
                        ▼
              ShopMy API (AUTOMATED)  ── clicks, promoters, price, category, timestamps
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
  Google Trends    Poshmark        Pickle (MANUAL, bot-gated)
  (AUTOMATED)      (AUTOMATED,     product-level rental supply
  independent      permitted
  demand check     paths only)
        │               │                │
        └───────────────┴────────────────┘
                        ▼
        priority = gap × price_fit × occasion_weight
                        ▼
          ranked digest + threshold alerts, daily
```

## Why this shape

**The reframe.** TRACE does not need a trend tracker; those are a commodity. Because the business is
presale, demand has to form *before* supply exists, so the decision-relevant signal is the
intersection of accelerating demand with secondary supply that has not yet formed. The system is built
around that intersection.

**Why ShopMy is the engine.** It is the only one of the three named platforms whose `robots.txt` grants
`Allow: /`, and its public API returns product-level `dailyClicks`, `weeklyClicks`, `monthlyClicks`,
`num_promoters`, price and category. That is five of the seven requested signals with real numbers. And
clicks on monetised retailer links measure intent to shop, which is strictly stronger than views.

**Why discovery is creator-seeded.** ShopMy's global product search requires authentication (verified
401). Rather than bypass it, the system starts from a curated creator list. This suits TRACE's
creator-driven thesis anyway, and choosing which creators matter is exactly where human judgement
beats automation.

## Quick start

```bash
pip install -r requirements.txt
python run.py                       # full run: collect, score, alert, write digest
python run.py --creators 2 --no-trends   # fast smoke test
python eval/counter_cadence.py      # how often does the source actually republish?
python eval/precision.py            # measured precision of the system's own hypotheses
```

No API keys and no paid services. `data/radar.sqlite` and `reports/` are committed, so the history is
auditable rather than asserted.

## Layout

| Path | Purpose |
|---|---|
| `run.py` | Entry point: collect → store → score → alert → digest |
| `store.py` | Append-only SQLite. Never overwrites, because momentum is a derivative |
| `score.py` | Acceleration ratios, trajectory labels, price fit, gap and priority |
| `alerts.py` | Diffs against the previous upstream batch; builds the markdown digest |
| `collectors/shopmy.py` | The demand engine |
| `collectors/poshmark.py` | Supply attempt, kept including its negative result |
| `collectors/trends.py` | Independent demand cross-check |
| `watchlist.yaml` | Creator seeds, price band, occasion weights, all tunable |
| `manual_supply.yaml` | Hand-measured product-level supply (Poshmark + Pickle) |
| `tiktok_observations.yaml` | The manual TikTok pass, with sources and dates |
| `eval/` | Cadence analysis and precision measurement |

## How momentum is computed

The source reports overlapping cumulative windows, so:

```
accel_short = dailyClicks / (weeklyClicks / 7)          # today vs this week
accel_mid   = (weeklyClicks / 7) / (monthlyClicks / 30) # this week vs this month
```

Trajectory labels: `rising` · `peaking` · `sustained` · `cooling` · `faded` · `insufficient_volume`.

`sustained` exists because the brief counts an item "especially popular over the past two weeks" as in
scope. Without it, a consistently popular dress gets discarded as merely cooling, and the two
highest-volume items in the dataset are `sustained`, so the label does real work.

`faded` is what separates a live opportunity from a retrospective report. Tuckernuck's Marcie Dress has
the largest all-time click total in the dataset (55,700) and a week-vs-month ratio of 0.155. A "most
popular dresses" report leads with it. It is comprehensively over.

**Two limitations handled rather than hidden.** Low-volume items produce wild ratios (1 → 7 clicks
reads as 5x), so `MIN_DAILY` and `MIN_WEEKLY` gate them into `insufficient_volume` and they are never
alerted. And `dailyClicks` is a single day, so a weekend snapshot would inflate `accel_short` across
the board, which the stored history corrects for.

## The most important thing measured about the data source

**ShopMy republishes its click counters as a once-daily batch, not live.**

```
run 1 → 2      0 of 525 products changed   (23:26 → 23:46 UTC)
run 2 → 3      0 of 525                    (23:46 → 01:56)
run 3 → 4      0 of 525                    (01:56 → 02:19)
run 4 → 5      0 of 525                    (02:19 → 07:26)
run 5 → 6    248 of 526  (47%)             (07:26 → 13:25)
```

Consequences, all applied:

- Polling cut from 4x to 2x daily around the observed publish window. Three of every four requests were
  fetching an identical payload.
- **Alerting diffs against the previous distinct *batch*, not the previous run** (`store.previous_batch_run`).
  Two runs inside one batch window would otherwise produce an empty diff that reads as "nothing is
  happening" when really nothing has been *published*.
- Any reported change means one published day of movement, never elapsed wall-clock time.

Worth noting how this was got wrong first: the initial analyzer inspected per-product drift, saw
mostly no movement, found no midnight resets, and concluded "rolling 24h window, safe to poll more
often." Flat-because-stale is indistinguishable from flat-because-steady when you look product by
product. The signature that separates them is **synchronisation across the panel**, so the analyzer was
rewritten to test the panel instead.

## Design decisions worth arguing with

**Interpretable scoring over a better model.** Every weight lives in `watchlist.yaml`. A weighted score
Ella can disagree with beats a model nobody can question, and disagreement should be a config edit.

**`gap` and `priority` are kept separate.** `gap = demand × (1 − supply_pressure)` is the measurement,
true whether or not TRACE cares. `priority = gap × price_fit × occasion_weight` layers on TRACE's
stated targeting. Splitting them means strategy changes without touching the measurement.

**Price band is a soft factor, not a filter**, because the brief said there is no strict cutoff. The
taper is deliberately asymmetric: below $400 the presale mechanic breaks down, since a cheap dress's
resale value does not change anyone's purchase decision. Above $1,000 the mechanic still works and the
item is merely dearer than the stated focus, so it is penalised far more gently.

**Unmeasured supply scores neutral (0.5), not zero.** Absence of data is not absence of supply. This
stops an unchecked item masquerading as a confirmed gap.

**Tuned for precision, not coverage.** One alert triggers content, creator outreach, comment
engagement, lister identification and possibly a seeded listing, real coordinated effort, so a false
positive is expensive. Volume floor raised, rising threshold lifted to 1.35, alerts gated on price fit
and capped at 5 per run. A recent run produced 5 alerts and suppressed 13.

**Collectors fail soft.** A radar that dies because one source is down is worse than one that reports
what it reached and names what it did not. The digest lists unavailable sources.

## Boundaries deliberately not crossed

- **Pickle's bot protection was not circumvented.** Every host returns HTTP 429 behind a Vercel
  checkpoint, including `robots.txt`. Bypassing an explicit anti-bot control would create legal
  exposure for TRACE, not for me. Pickle is handled as manual observation, with a documented path to
  proper access, a data partnership or licensed provider, which is a business conversation.
- **Authentication was not bypassed.** ShopMy's `/Products/` and `POST /Pins/search` return 401 and are
  untouched.
- **Poshmark's `robots.txt` is respected.** `/search` is disallowed, so only brand and category paths
  are used programmatically. Product-level counts were done by hand in a browser.
- **Incidental data is not persisted.** The ShopMy user endpoint returns unrelated internal fields
  (a referring brand's `stripeCustomerId`, a support phone number, admin flags). The collector
  whitelists only what it scores; everything else is dropped rather than stored "just in case".

## Known limitations

1. **Demand is measured well, supply badly.** The system will systematically over-rank items whose
   supply it cannot see. Pickle is unreachable and Poshmark's automated count saturates at 48 for every
   brand, so the supply term is usually neutral, and neutral supply flatters a high-demand item.
2. **Brand-level and product-level supply give opposite answers.** Brand-level, Kilentar looks well
   supplied and Réalisation Par thin. Product-level it inverts: Cora 22+, Ano 3. The radar only reaches
   brand level. This single distinction decided the recommendation.
3. **Creator concentration.** 18 of the top 20 ranked items came from one seeded creator. The board
   currently reflects one curator's taste more than the market.
4. **Occasion inference is noisy.** It reads a curator's collection title, not the product's cultural
   positioning. Correct on Kilentar's Ano, wrong on ALÉMAIS's Porter Midi.
5. **A vanished Pickle listing is ambiguous**, rented, sold, removed and deactivated are
   indistinguishable from outside. Nothing here treats disappearance as a rental.
6. **Two distinct batches of history so far**, so one genuine day-over-day transition.

## What I would build next

1. **Product-level supply**, since that is what decides recommendations. Realistically a Pickle
   partnership or licensed resale data rather than more scraping.
2. **Widen the creator seeds** and require cross-creator corroboration before an item tops the board.
   Suggestive: the only item two seeded creators both pinned was also the only one independently
   validated on TikTok.
3. **Add LTK.** Fully permissive `robots.txt`, public SSR creator pages. Deferred because its payload is
   minified and it exposes no click or promoter counts, so it adds breadth but not momentum.
4. **Occasion classification from product attributes** rather than collection titles.
5. **Test whether creator pinning leads public search interest.** If it leads, the radar gains days.
6. **Alerts into Slack** with a one-line why, so they land where decisions get made.

## Reliability note

The scheduled job lost a snapshot on 23 August to a push race: the radar collected fine, then `git
push` was rejected because a commit landed between checkout and push, and the ephemeral runner meant
the data was gone. Diagnosed from the logs and fixed with `fetch` + `reset --soft` onto the new tip
(not pull/rebase, because the SQLite file is binary and a rebase can conflict on it with no sensible
textual resolution).

Recorded because a system that has never failed is usually one that has not run long enough.
