# TRACE Demand Radar: Findings

**Jatan Patel · 22–24 August 2026**

Everything below was observed directly. Every number has a source and a date. Where I could not
observe something, I say so rather than estimating it.

---

## The short version

**Recommendation: Kilentar's Ano Layered Raffia Dress, $750.**

There is **exactly one available to rent in New York.** For comparison, the dress that every other
signal pointed at has **roughly twelve.** That single New York unit rents at **40% of retail**, double
Pickle's own published guidance to lenders, which is what scarcity looks like in pricing. The dress
sits inside your $400–1,000 band and is peaking rather than fading.

**And the timing is the part I would act on.** A creator posted a *"fall wedding guest dresses"*
roundup five hours before I looked, with the Ano selected among the options. Fall wedding season has
not happened yet. Creators are pre-positioning for it now, and there is one unit available to rent in
New York. So there is a window to organize presale demand ahead of the season rather than chase it during.

**I am not recommending the hottest dress I found.** Réalisation Par's Cora had a 10x single-day jump
in click-throughs, 100+ TikTok posts, videos posted 47 minutes before I looked, and it holds 82–111% of
retail on resale while its sibling products discount to 38–68%. Every automated signal favored it.
Then I checked Pickle by hand and found 22+ units already rentable, a dozen in your home market. The
supply has already formed and Pickle has captured it.

**What I built:** a demand radar that has run unattended twice daily since 22 August, committing its
own snapshots. It flagged Cora's acceleration on published click data before I had looked at TikTok at
all, so the detection works.

**What I learned about it:** the system is good at finding candidates and bad at qualifying them. It
measures demand well and supply badly, because the platform that decides the answer is the one that
cannot be scraped. **Measured precision on its own opportunity calls is 1 of 3.** That is not a reason
to distrust the demand side, which held up under three independent corroborations, it is a precise
statement of where the automation ends and why the human step is load-bearing rather than decorative.

Detail, method, named creators, five failure modes and everything I am still unsure about follows.

---

### Update from this morning's run, 24 August

The system published a new batch while I was finishing this, so here is what one more day did. I have
left the body of the document at run 7 and put the delta here rather than quietly restating everything.

| | Run 7 (23 Aug) | Run 8 (24 Aug) | |
|---|---|---|---|
| **Ano** (the recommendation) | 36 daily, accel 0.99, `peaking` | **48 daily, accel 1.46, `rising`** | strengthened |
| **Cora** (not recommended) | 3,653 daily, accel 3.62, `rising` | **442 daily, accel 0.42, `sustained`** | the spike reverted |
| **Porter Midi** (demoted) | 75 daily, accel 2.84, `rising` | 102 daily, accel 2.60, `rising` | still climbing |

Three things worth drawing out.

**The recommendation got stronger.** The Ano crossed from peaking into rising overnight, which is the
trajectory you said you wanted to catch, and it is still ranked first.

**Cora's 10x jump was a single-day event.** Daily click-throughs fell from 3,653 to 442 in one publish.
I declined to recommend it because the rental supply had already formed; a day later the demand
signal has reverted too. So the call was right for a second reason I had not claimed.

**Porter Midi is still climbing and I still would not act on it.** The radar has now ranked it second on
click momentum two batches running, while the manual checks that demoted it (no product-level
attention, probable occasion mismatch, 30+ ALÉMAIS rental listings with 15+ in New York) have not
changed. That is failure mode 1 doing exactly what I described, on live data, rather than as a
hypothetical.

---

## 1. How I framed the problem

TRACE does not need a trend tracker. Trend trackers are a commodity, and a ranked list of hot dresses
would not tell you where to act.

What TRACE needs is a **supply-gap detector.** The business is presale: demand has to form *before*
supply exists. So the decision-relevant signal is not "what is popular" but the intersection of
**demand accelerating** with **secondary supply not yet formed**. It is the only output that points
at an action.

So I built the system around that intersection, and I built it to be honest about the half it cannot
measure well.

**The headline result is that this reframing survived contact with the data, but my first two
candidate answers did not.** Both were overturned by manual checks. That process is the most useful
thing in this document, so I have written it up as it actually happened rather than presenting only
the conclusion.

---

## 2. Where I began, and what I deliberately did not do

I started by probing what is actually reachable, before writing any pipeline. The brief says
determining what can be observed is part of the exercise, and it turned out to be the decision that
shaped everything else. Full log in [`PROBE_LOG.md`](PROBE_LOG.md).

**What I chose to automate: the demand side, via ShopMy.** It is the only one of the three named
platforms whose `robots.txt` grants `Allow: /`, and its public API returns product-level
`dailyClicks`, `weeklyClicks`, `monthlyClicks`, `num_promoters`, price and category. That covers five
of the seven signals you listed, with real numbers, and clicks on monetized retailer links measure
intent to shop rather than mere attention.

**What I deliberately did not do:**

- **I did not circumvent Pickle's bot protection.** Every Pickle host returns HTTP 429 behind a Vercel
  checkpoint, including `robots.txt`. Bypassing an explicit anti-bot control would put legal exposure
  on TRACE, not on me, and Pickle is your closest comparable so a data partnership is unlikely.
  Pickle is handled as manual observation with a documented path to proper access.
- **I did not bypass authentication.** ShopMy's `/Products/` and `POST /Pins/search` return 401. That
  makes global product search unavailable, so discovery is creator-seeded instead, which suits your
  creator-driven thesis better anyway.
- **I did not scrape Poshmark's disallowed paths.** `robots.txt` disallows `/search`, so I used only
  brand and category paths, and hand-checked product level in a browser.
- **I did not build an LTK integration**, despite LTK being fully permissive and the obvious way to
  de-risk single-source dependence. Its payload is minified and, more decisively, it exposes no click
  or promoter counts, so it would add breadth but not momentum. Documented as the best next
  integration rather than half-built.
- **I did not persist incidental data.** The ShopMy user endpoint leaks unrelated internal fields (a
  referring brand's `stripeCustomerId`, a support phone number, admin flags). The collector whitelists
  only what it scores and drops the rest.

---

## 3. What I could and could not observe

| Source | Status | What it gave |
|---|---|---|
| **ShopMy public API** | Open (`Allow: /`) | Product-level clicks, promoters, price, category, timestamps |
| **Google Trends** | Open | Hourly search interest, independent momentum cross-check |
| **Poshmark** | Partial | Brand/category pages only. Page one **saturates at 48 for every brand**, so the automated count is uninformative. Product level done by hand |
| **Pickle** | **Blocked** | HTTP 429 on every host including `robots.txt`. Manual app checks only |
| **TikTok** | Manual | Attention, creator discovery, occasion validation |
| Depop / By Rotation / RTR | Blocked | 403 / 404 / 406 |

One finding about the primary source matters enough to state up front: **ShopMy republishes its click
counters as a once-daily batch, not live.** Measured across seven snapshots, zero of 525 products
changed between 23:26 and 07:26 UTC, then 248 of 526 changed at once at 13:25. So polling four times a
day fetched an identical payload three extra times. I cut the schedule to twice daily around the
observed publish window and re-anchored all comparisons to the previous *batch* rather than the
previous run. Any reported change therefore means one published day of movement, never elapsed
wall-clock time.

---

## 4. The dresses

Radar output as of run 7. Occasionwear only, ranked by priority against your $400–1,000 band.

### 4.1 Kilentar Ano Layered Raffia Dress · $750 · **the recommendation**

**Why this one.** It is the only candidate where demand, attention, occasion, price band and thin
product-level supply all hold at once.

| Signal | Observation |
|---|---|
| Current heat | 36 daily clicks, 255 weekly (ShopMy, 23 Aug) |
| Momentum | `accel_short` 0.99 → classified **peaking**, not rising |
| Recency | **Measured, not inferred:** a date-filtered search returned 4 Kilentar posts this week, 2 of them featuring the Ano, at 5 and 10 hours old |
| Creator activity | 205 promoters on ShopMy; at least 4 distinct TikTok creators on this dress |
| Cross-platform breadth | ShopMy ✓ · TikTok ✓ (product-level) · Poshmark ✓ · Pickle ✓ |
| Commerce intent | 8,537 total clicks; Pickle buy-outs on Kilentar at $500–1,000 |
| **Rental liquidity** | **3 Pickle listings nationwide, exactly 1 in New York**, renting at **26–40% of retail** |

**What makes this the pick:**

**Product identity and occasion are independently confirmed.** A TikTok editorial listicle titled
*"The Wedding Guest Outfit Even The Bride Is Talking About - 8 African Brands Making Them"* names it
directly: *"1. Kilentar - Ano Dress. Sunshine yellow. Four tiers of fringe that move before you do.
The whole table turns before you've reached your seat."* Two further creators tagged the same dress
`#weddingguestdress`, one styled with a partner in a suit. My pipeline had inferred `occasion` from a
curator's collection name; TikTok agreed.

**The supply is thin where it counts, and the price proves it.** A targeted product search returns
**three Ano listings nationwide**: Kips Bay NY at $300, Dallas at $240, Uptown TX at $195, plus one
probable fourth in Woburn MA identified visually. The count is reliable rather than a floor because
search relevance collapsed into unrelated inventory after the fourth result; the result set exhausted
itself.

Pickle is peer-to-peer with local delivery, so local supply is what competes. **There is exactly one
Ano available to rent in New York, against roughly twelve Coras.**

And the New York unit is the most expensive of the three: $300, or **40% of retail**, against $240 in
Dallas and $195 in Uptown. Pickle's own guidance to lenders is 10–20%. The highest price sits in the
highest-demand market, on the only local unit. Scarcity expressed in price rather than
inferred from a count, and it is observed rather than modeled.

Demand pressure against those units is visible too: 135 and 136 saves on two of the three listings,
for a product with three units on the platform.

**And the timing signal, which is the part I would act on first.** A date-filtered search returned
exactly four Kilentar posts this week (the app then showed "No more results", so that is a complete
set, not a sample). Two feature the Ano, at 5 and 10 hours old. The 5-hour-old one is a curated
roundup titled *"Unique & chic fall wedding guest dresses"*, in which the Ano appears among a
shortlist of options.

That is **forward-looking demand.** Fall wedding season has not happened yet. Creators are
pre-positioning for it now, the Ano is being selected against alternatives in that content, and there
is exactly one available to rent in New York. Presale demand can be organized ahead of the season
rather than chased during it, which is the window the presale model exists to exploit.

Note also what the same search does *not* show: four posts brand-wide in a week is modest volume. This
is steady-to-peaking, not a viral explosion, and I am describing it that way. That independently agrees
with the click series classifying it `peaking` rather than `rising`, which is a genuine cross-source
agreement on trajectory rather than a restatement of the same evidence.

**Absent signals, stated:** only 5 Kilentar listings on Poshmark brand-wide. Read alongside ~32
Kilentar rental listings on Pickle, the pattern suggests Kilentar is a rent-not-resell brand, which is
consistent with statement occasionwear worn once. Directional at this sample size, not established.

---

### 4.2 Réalisation Par: The Cora Dress · $360 · **hottest, and I am not recommending it**

This is the most instructive case in the document.

| Signal | Observation |
|---|---|
| Current heat | **3,653 daily clicks**, 7,072 weekly |
| Momentum | `accel_short` **3.62**. Published daily figure jumped 378 → 3,653 in one batch, ~10x |
| Recency | TikTok posts **47 minutes** and 1 hour before my pass |
| Creator activity | 977 promoters; **11+ distinct TikTok creators**; the only item 2 of my seeded creators both pinned |
| Cross-platform breadth | Present and strong on all four sources |
| Commerce intent | Two explicit "where is this from" comments answered in-thread; save-to-like ratios of 4,496 on 58K |
| **Rental liquidity** | **22+ Pickle listings, at least 12 in New York** |

**Every automated signal favored Cora. The automated recommendation would have been wrong.**

It also holds value on resale in a way its siblings do not. Three Cora listings at $295, $360 and $400
against $360 retail, two of them new with tags, one **above** retail, while every other Réalisation
Par dress on the same page discounts hard (Iris 38% of retail, Christy 52%, black mini 60%, Alba 68%,
Elsa 67%, Gia 89%). Cora holds 82–111%. That within-brand comparison controls for brand effects, and
it is a direct demonstration of your criterion that resale value must be high enough to influence the
purchase decision.

**And then the supply check killed it.** 22+ units of this exact dress are already rentable, a dozen
of them in your home market. Your own brief anticipates this test: a dress accelerating on TikTok and
linked on ShopMy *"but has little presence on Pickle"* is the opportunity. Cora has heavy Pickle
presence. Organizing presale demand around it means competing with a dozen existing NYC listings for
the same garment.

One manual check on the one platform that cannot be scraped reversed the conclusion.

---

### 4.3 ALÉMAIS: Porter Midi Dress · $690 · **radar ranked it, manual check demoted it**

| Signal | Observation |
|---|---|
| Current heat | 75 daily clicks, 185 weekly |
| Momentum | `accel_short` 2.84, classified rising |
| Recency | Brand posts mostly Jul 17–18 and Mar 21; only recent post had 585 likes |
| Creator activity | ShopMy promoters present; **zero TikTok posts featuring this dress** |
| Cross-platform breadth | ShopMy only at product level |
| Commerce intent | Clicks only, no corroborating attention |
| Rental liquidity | Poshmark 28 brand-wide. **Pickle: 30+ ALÉMAIS listings, 15+ of them in New York, but none titled or identifiable as the Porter** |

**Two reasons it drops out.** The Porter Midi itself appears in no TikTok search, four queries
returned only *other* ALÉMAIS pieces. And the occasion tag is probably wrong: TikTok positions ALÉMAIS
as vacation and resort wear (Portugal, palm trees, "summer sun dress"), while my pipeline tagged
Porter `occasion` from a curator's collection name.

**And the Pickle check closes it.** ALÉMAIS has at least 30 rental listings, 15 or more in New York:
Seaport ×3, Chelsea ×3, West Village ×3, Greenwich Village ×2, Carnegie Hill, Financial District,
Flatiron, Tribeca, Lincoln Square, Brooklyn Heights, Lenox Hill. Saves run high throughout, up to 1.1K
on one listing. So the brand is an established, well-supplied rental name in exactly TRACE's market.

The pricing agrees, from independent evidence. ALÉMAIS rents at roughly **$60 to $210, about 15–25% of
retail**, squarely inside Pickle's own 10–20% guidance. No scarcity premium at all. Compare the Ano at
33–40%. Count and price discriminate in the same direction.

So Porter Midi fails every qualifying check: click momentum with no product-level attention, an occasion
tag that is probably wrong, and abundant brand rental supply at normal platform pricing. **The radar
ranked it fourth and every manual check demoted it.**

It's a concrete instance of a known weakness in my own inference, caught by the manual step. It is
in the write-up rather than quietly dropped, because it is the clearest example of the automation
generating a candidate that qualification kills, and the failure mode matters more than the item.

---

### 4.4 The counter-example: what a retrospective report would have led with

**Tuckernuck's Marcie Dress.** 55,711 total clicks, the largest in the dataset. Also 4,035 monthly
against **149 weekly**, a week-vs-month ratio of **0.158**.

A "most popular dresses" report ranks Marcie first. It is comprehensively over. The same ratio flags
ASTR the Label's Wedelia (31,812 total, 0.185) and Leo Lin's Ava (18,297 total, 0.099).

This is the retrospective-report failure your brief warns about, and separating it out is the single
cheapest thing the system does.

---

## 5. Creators currently driving these dresses

**On the Ano (the recommendation):**

- **Laura Morgan** (TikTok), three posts on the Ano across Jun 21/23/27, 154 / 1.3K / 2.1K likes,
  tagged `#kilentar #weddingguestdress`, one styled with a partner in a suit. The most consistent
  single voice on this dress.
- **Olive** (TikTok), the editorial listicle that names the Ano Dress and frames it as wedding-guest
  wear, 5.1K likes, Apr 24. High-authority framing rather than a fit check.
- **Anne Leopard** (TikTok), posted 5 hours before my final pass: *"MY TOP FAVORITE niche and fun fall
  wedding guest dresses"*, 87 likes, with the Ano selected among a shortlist. **The one I would contact
  first.** She is producing forward-looking fall-season content, she chose this dress against
  alternatives, and she posted the same day I ran the search.
- **Surya Garg** (TikTok), 10 hours before that pass, `"@kilentar let's get married
  #weddingguestdress"`, overlay *"potentially the greatest dress I will ever wear."* Small account, but
  current and unambiguous about occasion.

**On the Cora** (included because it is one of the three dresses, even though I am not recommending it):

- **Angel Song** `@angeltrsong` (TikTok), the anchor post at **58K likes, 4,496 saves, 1,635 shares**,
  tagged `#weddingguestlook`, 6 days old. 5.6K followers but 1.7M total likes, so reach far exceeds
  follower count. She also answered two separate "where is this from" comments in-thread with the brand.
- **Eliza** `@elizasmithx` (TikTok), 57.9K views, 2,703 likes: *"The hype around this dress is deserved."*
  Note the caption reacts to an existing trend rather than starting one.
- **courtney** (TikTok, and **has a ShopMy storefront**), the dupe angle: two posts titled *"Realisation
  P@r lookalike dress"* with TikTok Shop tags attached. Commercially the most interesting of the Cora
  creators, because monetizing a lookalike means demand exceeds affordable access.

**On the ShopMy side:** `curatedbymc` is the single most valuable creator in the pipeline. She
surfaced both finalists and 18 of the top 20 ranked items, which is also a risk, see §7.

**One structural observation worth your attention.** The creators driving virality on TikTok are
largely *not* on ShopMy. `@angeltrsong` (58K likes on Cora), `@elizasmithx`, `@miahiraani` have no
ShopMy storefront under those handles. Going viral and running a monetized storefront are different
businesses. But the radar still caught Cora, because a ShopMy curator picked it up. **ShopMy creators
function as a sensing layer for trends that originate elsewhere**, which means for recruitment you
should be looking at TikTok, and for measurement at ShopMy.

Kilentar's own brand account illustrates the same point: 100.3K followers, but its own posts get
60–112 likes while creator posts on the same dresses reach 5–13K. Reach here is creator-driven.

---

## 6. The prototype

Live and running: **github.com/JATAN2703/trace-demand-radar**

What is automated, and why this piece: **the demand side plus change detection.** It is the part with
a legitimate, reliable data source, and the part a human cannot do daily by hand.

- **Collectors** (ShopMy, Google Trends, Poshmark) behind one interface, so a manual source becomes
  automated later without touching scoring
- **Append-only SQLite snapshots**: momentum is a derivative, so history is the asset
- **Scoring**, `accel_short = dailyClicks / (weeklyClicks/7)`, plus a volume floor, a soft $400–1,000
  price fit, and occasion weighting. All weights in `watchlist.yaml`
- **Alerting**, diffs against the previous upstream *batch*, capped at 5 alerts per run
- **GitHub Actions**, twice daily, committing its own snapshots

It has been running unattended since 22 August and has produced real detected change, including the
Cora 10x jump and two trajectory transitions.

Ranking separates `gap` (the measurement) from `priority` (`gap × price_fit × occasion_weight`, your
targeting), so a change in strategy is a config edit and the underlying measurement stays reusable.

**Tuned for precision, because you told me an alert triggers content, creator outreach, comment
engagement, lister identification and possibly a seeded listing.** Real coordinated effort per
flag, so a false positive is expensive. Volume floor raised, rising threshold lifted to 1.35, alerts
gated on price fit and capped. One run produced 5 alerts and suppressed 13.

---

## 7. How I would know if it works, and where it currently fails

**Measured precision on the hypotheses the system generated: 1 of 3 (33%).** Run
`python eval/precision.py` for the labels and the failure taxonomy. Ano was confirmed by manual check;
Cora and Porter Midi were both refuted.

The demand side, by contrast, held up under three independent corroborations: click acceleration,
TikTok volume and recency, and Poshmark price retention all agreed on Cora.

**External sanity check.** I compared my output to a fashion-press roundup of this week's trending
dresses. Most of its picks fall outside your brief by design (a $90 slip, a $169 polka-dot day dress, a
knit day dress), so their absence is the occasionwear targeting working. But DÔEN appears in both:
editorial calls it "the cult label of the moment," and my board independently surfaced two DÔEN dresses
from click data alone. One plausible in-scope miss, Sleeper's Genus Rosa at $458, is absent because none
of my nine seeded creators pinned it, which is the creator-concentration limitation below showing up
concretely rather than theoretically.

**So the failure is specific and diagnosable, not general.**

**Failure mode 1, the system measures demand well and supply badly.** It will systematically
over-rank items whose supply it cannot see. Pickle is unreachable and Poshmark's automated count
saturates, so the supply term is usually neutral, and neutral supply flatters a high-demand item.

**Failure mode 2, brand-level and product-level supply give opposite answers.** Brand-level, Kilentar
looks well supplied: around 32 Pickle listings brand-wide. Product-level it inverts completely, to
just 3 Ano units, one of them in New York. The radar can only reach brand level. This single distinction decided the
recommendation, and the automation is structurally blind to it.

**Failure mode 3, creator concentration.** 18 of the top 20 ranked items came from one seeded creator,
`curatedbymc`; 2 of 9 creators produced essentially the whole board. The output currently reflects one
curator's taste more than the market.

**Failure mode 4, occasion inference is noisy.** It reads a curator's collection title, not the
product's cultural positioning. Right on Ano, wrong on Porter Midi.

**Failure mode 5, a vanished Pickle listing is ambiguous.** Rented, sold, removed and deactivated are
indistinguishable from outside. Nothing in this document treats disappearance as a rental.

**Reliability note.** The scheduled job lost a snapshot on 23 August to a push race, diagnosed from the
logs and fixed. Recorded because a system that has never failed is usually one that has not run long
enough.

---

## 8. What remains uncertain

- **Precision is measured on n=3.** Directionally useful, statistically nothing.
- **Poshmark prices are asking, not sold.** Sold history needs a login. So price retention shows what
  sellers believe the market bears, not confirmed transactions.
- **TikTok dates from the unfiltered pass cannot support recency claims**, because the "Top" tab ranks
  by engagement rather than date. I caught this after the fact and re-ran a date-filtered search for
  Kilentar, which is why the Ano recency figure is measured. The equivalent filtered pass was **not**
  run for Cora or ALÉMAIS, so their date spreads carry the same caveat and should be read as "content
  exists at these times", not as a recency distribution.
- **The Ano count is reliable; the others are floors.** The targeted "Kilentar Ano" product search
  exhausted itself (relevance collapsed into unrelated inventory), so three nationwide and one in NYC
  is a total. But "22+ Cora" and "~32 Kilentar brand-wide" are minimums, because scrolling stopped
  before the end in both cases. The comparison that matters, 1 Ano versus ~12 Cora in New York, is
  therefore conservative in the direction that *weakens* my case, not strengthens it.
- **The filter chip read "Local"** while returning results from six states, so its semantics are
  unresolved and my NYC subset is what I saw, not a complete NYC inventory.
- **The Woburn "Yellow Fringe" listing** is my visual identification as an Ano, not a titled match.
- **One genuine day-over-day transition** exists in the data so far. Seven runs, two distinct batches.
- **Whether creator pinning leads or lags consumer search** is untested. I have the Google Trends
  series to test it and did not have enough days.

---

## 9. What I would build next, in order

1. **Product-level supply, since that is what decides recommendations.** Realistically this means a
   Pickle data partnership or licensed resale data, not more scraping. It is a business conversation.
2. **Widen the creator seed set** to break the `curatedbymc` concentration, and require cross-creator
   corroboration before an item can top the board. Suggestive signal: the only item two seeded
   creators both pinned was also the only one independently validated on TikTok.
3. **Add LTK** for breadth and to remove single-source dependence.
4. **Occasion classification from product attributes** rather than collection titles.
5. **Test the lead-lag question** between creator pinning and public search interest. If pinning leads,
   the radar gains days of head start.
6. **Alert into Slack** with a one-line why, so it lands where decisions get made.

---

## 10. The short version

The radar works on demand and is honest about supply. It found the hottest dress in the market inside
a day, and the manual step then told me not to recommend it.

My recommendation is **Kilentar's Ano Layered Raffia at $750**: wedding-guest positioning confirmed by
an independent editorial, in your price band, peaking rather than fading, and **exactly one rental unit
available in New York against roughly twelve for the dress everything else pointed at**, with that
single local unit priced at 40% of retail, double Pickle's own guidance. That is what scarcity looks
like before anyone has organized it.

The most transferable thing I learned is that on this problem the automation is good at finding
candidates and bad at qualifying them, and that the qualifying step is one platform you cannot
scrape. I would rather tell you that now than have you find it later.
