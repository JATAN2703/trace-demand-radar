"""ShopMy collector: the demand engine.

Why this is the primary source (see PROBE_LOG.md for the evidence):

  * It is the only one of TRACE's three named platforms whose robots.txt grants
    `Allow: /`.
  * Its public API returns product-level `dailyClicks`, `weeklyClicks`,
    `monthlyClicks`, `num_promoters`, price and category. That covers current
    heat, momentum, recency, creator activity and commerce intent, which is five
    of the seven signals the brief asks for.
  * Clicks are click-throughs on monetized retailer links, so they measure
    intent to shop rather than mere attention. TikTok views prove eyeballs;
    these prove someone went looking for the product.

Endpoints used, all unauthenticated and read-only:
    GET /api/Users/username/{handle}
    GET /api/Collections/{id}/pins?offset=&limit=

Deliberately NOT used: /api/Products/ and POST /api/Pins/search both return 401.
We do not bypass authentication, so discovery stays creator-seeded.
"""

import datetime as dt

API = "https://apiv3.shopmy.us/api"
REFERER = "https://shopmy.us/"


def classify_occasion(collection_name: str | None, keywords: dict) -> str:
    """Infer occasion from the collection a creator filed the item under.

    Creators name collections for the occasion they have in mind ("Wedding Guest
    Dresses", "Formal dresses"), which makes the collection title a better
    occasion signal than the product title. Returns 'unknown' rather than
    guessing when nothing matches; downstream weighting treats unknown as
    mildly discounted, not disqualified.
    """
    if not collection_name:
        return "unknown"
    name = collection_name.lower()
    for occasion, terms in (keywords or {}).items():
        if any(str(t).lower() in name for t in terms):
            return occasion
    return "unknown"


def _days_since(iso: str | None) -> float:
    if not iso:
        return 1e9
    try:
        d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (dt.datetime.now(dt.timezone.utc) - d).days
    except Exception:
        return 1e9


def fetch_creator(fetcher, handle: str) -> dict | None:
    data = fetcher.get(f"{API}/Users/username/{handle}", referer=REFERER)
    if not data or not data.get("exists"):
        return None
    return data.get("user")


def select_collections(user: dict, max_n: int, staleness_days: int) -> list[dict]:
    """Most-recently-updated collections, freshest first, staleness-bounded."""
    cols = [c for c in (user.get("collections") or []) if not c.get("private")
            and not c.get("isArchived")]
    cols = [c for c in cols if _days_since(c.get("updatedAt")) <= staleness_days]
    cols.sort(key=lambda c: c.get("updatedAt") or "", reverse=True)
    return cols[:max_n]


def _extract(pin: dict, category_filter: str) -> dict | None:
    """Map one pin to our whitelisted product row, or None if not in scope.

    Only the fields we actually score are copied out. The upstream payload also
    contains unrelated internal values (a referring brand's Stripe customer id,
    a support phone number, admin flags). Those are not ours and are not stored.
    """
    prod = pin.get("product") or {}
    if not prod:
        return None
    category = prod.get("Category_name")
    if category_filter and category != category_filter:
        return None
    pid = prod.get("id") or prod.get("Product_id") or pin.get("Product_id")
    if not pid:
        return None
    price = prod.get("fallbackPrice")
    try:
        price = float(price) if price not in (None, "") else None
    except (TypeError, ValueError):
        price = None
    return {
        "product_id": str(pid),
        "title": prod.get("title") or pin.get("title"),
        "brand": prod.get("AllBrand_name"),
        "category": category,
        "price": price,
        "num_promoters": prod.get("num_promoters"),
        "daily_clicks": prod.get("dailyClicks"),
        "weekly_clicks": prod.get("weeklyClicks"),
        "monthly_clicks": prod.get("monthlyClicks"),
        "total_clicks": prod.get("totalClicks"),
        "domain": pin.get("domain") or (pin.get("merchant_data") or {}).get("domain"),
        "_pinned_at": pin.get("createdAt"),
    }


def collect(fetcher, creators: list[str], category_filter: str = "Dresses",
            max_collections: int = 12, staleness_days: int = 400,
            occasion_keywords: dict | None = None) -> tuple[list[dict], list[dict], dict]:
    """Walk seeded creators and return (products, pins, meta).

    Products are deduped by id at the store layer; the same dress legitimately
    appears in several creators' collections, and that overlap is itself the
    creator-breadth signal we want to keep in `pins`.
    """
    products: list[dict] = []
    pins: list[dict] = []
    meta = {"creators_ok": [], "creators_failed": [], "collections_scanned": 0}

    for handle in creators:
        user = fetch_creator(fetcher, handle)
        if not user:
            meta["creators_failed"].append(handle)
            continue
        meta["creators_ok"].append(handle)

        for col in select_collections(user, max_collections, staleness_days):
            cid = col.get("id")
            cname = col.get("name")
            occasion = classify_occasion(cname, occasion_keywords or {})
            payload = fetcher.get(
                f"{API}/Collections/{cid}/pins?offset=0&limit=100", referer=REFERER
            )
            meta["collections_scanned"] += 1
            if not payload:
                continue
            for pin in (payload.get("pins") or []):
                row = _extract(pin, category_filter)
                if not row:
                    continue
                pinned_at = row.pop("_pinned_at", None)
                products.append(row)
                pins.append({
                    "creator": handle,
                    "collection_id": cid,
                    "collection_name": cname,
                    "occasion": occasion,
                    "product_id": row["product_id"],
                    "pinned_at": pinned_at,
                })
    return products, pins, meta
