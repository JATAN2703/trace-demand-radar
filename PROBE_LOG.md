# Feasibility Probe Log: what can actually be observed

**Probed Sat Aug 22, 2026.** This log answers the exercise's own framing: *"part of the exercise is
determining what can be observed, which signals are meaningful, what can be inferred responsibly."*
Every finding below was verified by direct request, not assumed. Reproduce with the commands noted.

---

## Summary table

| Source | Status | What it gives | Signals served |
|---|---|---|---|
| **ShopMy public web API** | ✅ **OPEN** (robots: `Allow: /`) | Creator storefronts, collections, product-level pins with click + promoter counts | heat, momentum, recency, creator activity, commerce intent |
| **Google Trends** (`pytrends`) | ✅ OPEN | Hourly search-interest series, free | momentum (independent cross-check) |
| **Poshmark** brand/category pages | ⚠️ PARTIAL | ~296 listing tiles/page. `robots.txt` **disallows `/search`**; brand + category paths are permitted | secondary-market supply |
| **Pickle** (shoponpickle.com) | ❌ **BLOCKED** | Vercel bot gate, HTTP 429 on every host incl. `robots.txt` | rental liquidity → manual only |
| ShopMy `/Products/`, `POST /Pins/search` | ❌ AUTH REQUIRED (401) | n/a | not used (see ethics note) |
| Depop / By Rotation / Rent the Runway | ❌ BLOCKED (403 / 404 / 406) | n/a |, |
| TikTok | ⚠️ MANUAL | Creator + trend discovery by hand | attention, creator seeding |

---

## 1. Pickle: programmatically inaccessible (documented)

The correct domain is **shoponpickle.com** (`getpickle.com` is an unrelated 1.4 KB placeholder, worth flagging because
since guessing the domain would have produced a false negative).

Every host returns **HTTP 429** with a Vercel "Security Checkpoint" interstitial (~33 KB):
- `www.shoponpickle.com/` → 429
- `www.shoponpickle.com/how-it-works` → 429
- `shop.shoponpickle.com/` and `/closet/{uuid}` → 429
- **`shoponpickle.com/robots.txt` → 429** (I cannot even read their crawling policy)
- Only `help.shoponpickle.com` (Intercom) returns 200, and it holds no listing data.

A rendering fetch (headless/markdown proxy) also returned 429. So this is not a user-agent problem.

**Google *does* index the site**, so the pages are public; they are gated against automation specifically.
Indexed structure is informative and predictable:
- `/shop/rent/dresses`, `/shop/rent/dresses/midi`, `/shop/rent/dresses/high-low`
- **`/shop/rent/{brand}/dresses`** (e.g. `house-of-cb`, `alc`) ← would be the ideal brand-level supply probe
- `shop.shoponpickle.com/closet/{uuid}`

**Decision: do not circumvent.** Not only because bypassing an explicit anti-bot control is a ToS problem,
but because shipping a circumvention scraper into TRACE's stack would put *TRACE* at legal risk. Pickle is
handled as a **structured manual observation** with an explicit `confidence: manual` tag and an observation
timestamp. The documented path to automating it properly is a data partnership or API access, which is a
business conversation, not an engineering one. Worth saying out loud: Pickle is a **direct competitor
comparable**, so a partnership is unlikely and a licensed-data or manual-panel approach is the realistic route.

This also confirms the brief's own warning ("Pickle's public web experience is significantly more limited than
its mobile app") with hard evidence rather than restating it.

---

## 2. ShopMy: OPEN, and the richest source by far (the centerpiece)

`shopmy.us/robots.txt` is `User-agent: * / Allow: /`, the only one of the three named platforms that
explicitly permits crawling. Sitemap exists but lists only marketing/blog pages (187 URLs, 168 of them blog),
so **creators cannot be enumerated from the sitemap**, discovery must be seeded (see §6).

The site is a client-side React SPA (3.8 KB shell, `<div id="root">`), so HTML scraping yields nothing. The
bundle (`/static/js/main.db024bc9.js`, 14 MB) exposes `REACT_APP_API_URL = https://apiv3.shopmy.us`, and the
working prefix is **`/api`**.

### Verified public endpoints (no auth)
```
GET https://apiv3.shopmy.us/api/Users/username/{handle}
GET https://apiv3.shopmy.us/api/Collections/{id}/pins?offset=0&limit=50
GET https://apiv3.shopmy.us/api/Categories/            # taxonomy; Dresses = id 192, Department_id 44
```

`Users/username/lexxhidalgo` returned 210 KB: 282 collections and 12 sections, each collection carrying
`name`, `createdAt`, `updatedAt`, `num_pins`, `numShoppablePins`. One collection had been updated the
previous day, so **the recency signal is genuinely live**.

### The payload that makes this work
`/Collections/{id}/pins` returns, per pin, a nested `product` object with:

| Field | Serves |
|---|---|
| `title`, `AllBrand_name` | exact product + brand identification |
| `Category_name` (`Dresses`), `Department_name` | topical filtering |
| `fallbackPrice` | **price-tier filtering** (directly answers the price-band question put to Ella) |
| `num_promoters`, `yearlyElitePromoters` | creator breadth, how many creators push this item |
| **`dailyClicks`, `weeklyClicks`, `monthlyClicks`, `totalClicks`** | **current heat + momentum + commerce intent** |
| `domain`, `merchant_data.name`, `affiliate_link` | retailer, monetized intent |
| `createdAt` (pin), `Product_createdAt` | recency, creator-adoption timing |

Clicks are click-throughs to a retailer on monetized links, so that is *commerce intent* measured directly,
strictly stronger than TikTok views, which prove only attention. The PDF explicitly makes this distinction.

### Real sample (collection 4906491, "Wedding guest?!", 33/34 pins carried product data)
| Product | Brand | $ | Promoters | Daily | Weekly | Monthly | Total |
|---|---|---|---|---|---|---|---|
| Everly Lace Dress | Retrofete | 648 | 408 | 64 | 485 | 2459 | 6238 |
| Dinah Lace and Satin Maxi Dress | MESHKI | 195 | 1309 | 46 | 429 | 16736 | 54174 |
| Soleil Knit and Mesh Halter Maxi Dress | MESHKI | 145 | 155 | 36 | 160 | 1118 | 5069 |
| Thalia Halter Dress | Retrofete | 598 | 393 | 17 | 68 | 319 | 10324 |
| Indira Gathered Slinky Halter Maxi Dress | MESHKI | 145 | 191 | 15 | 79 | 738 | 7950 |

### Momentum is computable from a single snapshot
```
accel_short = dailyClicks / (weeklyClicks / 7)      # today vs this week's average
accel_mid   = (weeklyClicks / 7) / (monthlyClicks / 30)   # this week vs this month's average
```
Applied to the sample:
- **Soleil** `36 / (160/7) = 1.57` → **accelerating now**
- **Thalia** `17 / (68/7) = 1.75` → **accelerating now**
- **Everly** `64 / (485/7) = 0.92` → steady / at peak
- **Dinah** week-vs-month `= 0.11` → **well past peak, declining** despite the largest all-time volume (1309
  promoters, 54K clicks). A retrospective "most popular" list would wrongly surface Dinah; this ratio
  correctly demotes it. That is exactly the retrospective-report failure mode the brief warns against.

This separates *rising* from *peaking* from *faded*, the exercise's central ask, on day one, with no history.
Daily snapshots then upgrade these ratios into a true time series.

### Ethics and data hygiene, deliberate choices
- `/api/Products/` (401) and `POST /api/Pins/search` (401) require auth. **Not used, not bypassed.**
  Discovery is therefore creator-seeded rather than global-search, which suits TRACE's creator-driven thesis.
- The `Users` response incidentally leaks non-public fields (a referring brand's `stripeCustomerId`, a
  `noirPhoneNumber`, admin flags). The collector **whitelists only the fields it needs and discards the rest**;
  nothing incidental is persisted. Worth stating explicitly, a founder should want this instinct.
- Undocumented internal API: fine for a PoC, but the write-up should say a production system needs a sanctioned
  integration, and the collector must rate-limit politely and cache.

---

## 3. Google Trends: works, free, hourly

`pytrends` installed and verified: `build_payload(['floral maxi dress'], timeframe='now 7-d', geo='US')`
returned **169 hourly rows**. Serves as an **independent momentum cross-check**, which matters because it
guards against ShopMy-only bias, if clicks rise but search interest doesn't, the signal may be creator-side
promotion rather than genuine consumer demand. That divergence is itself worth alerting on.
Caveat: unofficial endpoint, historically rate-limited; needs retry/backoff and caching.

---

## 4. Poshmark: usable, within robots limits

`robots.txt` returns 200 and **explicitly `Disallow: /search`** (also `/api`, `/listings`, `/users`).
Brand and category paths are *not* disallowed and both work:
- `poshmark.com/brand/House_of_CB-Women-Dresses` → 200, ~296 tiles
- `poshmark.com/category/Women-Dresses` → 200, ~296 tiles

Parsing verified with BeautifulSoup: 48 tiles per viewport chunk, prices extractable, aggregate counts present
in-page. **Used only via permitted brand/category paths**, a deliberate constraint to record in the write-up.
Serves as the automatable **secondary-market supply** proxy, standing in for what Pickle would give.

---

## 4b. LTK (LikeToKnowIt): viable, deliberately deferred

LTK is ShopMy's largest competitor, so it is the obvious way to de-risk the fact
that my entire demand signal currently rests on one platform. Probed rather
than assumed:

- **`www.shopltk.com/robots.txt` is `User-Agent: * / Disallow:`**, an empty
  Disallow, so crawling is fully permitted. Best robots posture of anything here.
- Creator storefronts are public and server-rendered (Nuxt SSR):
  `shopltk.com/explore/{handle}`, e.g. `/explore/DressWithDani`,
  `/explore/outfitreport`. Returns HTTP 200, ~1.5 MB.
- The product data is genuinely present: 288 product-image CDN references and
  readable retailer names in-page (Amazon 60, Target 48, Nordstrom 31, Revolve).
- `liketoknow.it` redirects into `shopltk.com/explore/...`; `api.rewardstyle.com`
  responds 200 but exposes no documented public product route I could verify.

**Two reasons it is not in the PoC:**

1. The Nuxt payload is minified (`window.__NUXT__ = (function(a,b,c,...)`), so
   the object keys are substituted. Extraction needs either a headless render or
   reverse-engineering the obfuscated state. That is a day of work with a
   fragility cost, not an afternoon.
2. More decisively, **LTK does not appear to expose click-through or promoter
   counts.** Those velocity metrics are exactly what makes ShopMy the primary
   source. LTK would add cross-platform breadth, not momentum, so it improves
   confirmation rather than detection.

**Recommendation: this is the highest-value next integration**, because
"appears on both ShopMy and LTK" is a much stronger breadth signal than
"appears on ShopMy", and it removes a single-source dependency. Deferred on
purpose rather than half-built.

---

## 5. Also probed, unusable
`Depop` 403 · `By Rotation` 404 · `Rent the Runway` 406 · `eBay` robots reachable but `/b/` browse rules are a
maze of conflicting allow/disallow and it is less fashion-resale-relevant than Poshmark, so deprioritized.

---

## 6. What this means for the design

Because global product search needs auth, **discovery is creator-seeded**, and that is the better fit for
TRACE anyway, whose entire thesis is creator-driven demand.

```
TikTok (MANUAL, human-in-the-loop)
   └─> seed list of fashion creators driving dress discovery
        └─> ShopMy API (AUTOMATED)  ── dress pins, clicks, promoters, prices, timestamps
             ├─> Google Trends (AUTOMATED) ── independent momentum cross-check
             ├─> Poshmark (AUTOMATED, permitted paths) ── secondary-market supply
             └─> Pickle (MANUAL, blocked) ── rental supply spot-check, confidence-tagged
                  └─> GAP SCORE = demand x (1 - supply)  ->  ranked, alerted, daily
```

The manual TikTok step is not a shortcut. It is the **human-in-the-loop stage the role description explicitly
asks for**, placed where a human genuinely adds judgment (deciding which creators matter) and automation
genuinely cannot.

**The gap the brief asks for is now directly computable:** accelerating ShopMy clicks + rising promoter
count + thin Poshmark supply + absent from Pickle = demand forming before secondary supply exists.


---

## Postscript, written after testing the above

The closing hypothesis on this page, that thin Poshmark supply plus absence from Pickle marks a
presale opportunity, was the right thing to test and **it did not survive testing.**

Manual product-level checks found 22+ Réalisation Par Cora rental listings on Pickle, roughly a dozen
of them in New York, on the item every automated signal favored. The naive "absent from Pickle" test
also failed for Kilentar, which turned out to have around 32 brand-wide listings.

What replaced it is narrower and holds up: brand-level and product-level supply can point in opposite
directions, and only the product level decides anything. Kilentar's Ano has 3 rental units nationwide
and exactly 1 in New York, renting at 33-40% of retail against Pickle's own 10-20% guidance.

This page is left as written on 22 August rather than edited to match the conclusion, because the
sequence matters: the probe set the hypothesis, the manual work refuted it, and the recommendation
came from what was left. See `FINDINGS.md` §4 and §7.
