"""Poshmark collector: an attempt at automated supply, and why it is inconclusive.

This module is kept deliberately, including its negative result, because "what
can be observed" is part of the problem. Shipping a number I cannot explain
would be worse than shipping none.

What was tried, within robots.txt limits (Poshmark disallows `/search`, `/api`,
`/listings`, `/users`; brand and category paths are permitted):

  * `poshmark.com/brand/{Brand}-Women-Dresses` returns HTTP 200 and parses fine.
  * Page one contains **exactly 48 listings for every brand tested** (MESHKI,
    House of CB, Teri Jon, Mac Duggal). 48 is the page size, so the count is
    saturated and carries no information beyond "at least 48 exist".
  * The embedded JSON exposes a `"total"` alongside colour facets, but its scope
    does not survive a sanity check: Mac Duggal 219,947 and House of CB 205,694
    against MESHKI 89,011 and Teri Jon 12,272. Those orderings do not match the
    relative size of the brands, so the field is not a brand-filtered dress
    count and its true meaning is unverified.
  * Paginating to a true total would require the disallowed `/search` path.

So automated supply is reported as a saturated floor and tagged
`floor_saturated`, which the scorer treats as **unmeasured** rather than as
evidence of thin supply. Supply for finalist products is measured by hand
instead (see `manual_supply.yaml`), which is tractable because the brief asks
about two or three dresses, not thousands.

Path to automating this properly: Poshmark API access, or a licensed resale data
provider. That is a business conversation, not a scraping problem.
"""

import re

BASE = "https://poshmark.com"
PAGE_SIZE = 48


def brand_slug(brand: str) -> str:
    """'House of CB' -> 'House_of_CB', matching Poshmark's brand paths."""
    return re.sub(r"\s+", "_", brand.strip())


def brand_dresses_url(brand: str) -> str:
    return f"{BASE}/brand/{brand_slug(brand)}-Women-Dresses"


def page_one_count(fetcher, brand: str) -> tuple[int | None, str]:
    """Listings visible on page one. Returns (count, note)."""
    url = brand_dresses_url(brand)
    html = fetcher.get(url, as_json=False)
    if not html:
        return None, f"unreachable: {url}"
    n = len(re.findall(r'"active_item"\s*:\s*true', html))
    if n == 0:
        return None, "no listings parsed"
    if n >= PAGE_SIZE:
        return n, (f"saturated at page size ({PAGE_SIZE}); true total needs the "
                   "robots-disallowed /search path, so treated as unmeasured")
    return n, "page-one count, below page size so likely the full set"


def collect(fetcher, brands: list[str]) -> list[dict]:
    """One row per brand. `floor_saturated` is scored as unmeasured, not as zero."""
    rows = []
    for b in brands:
        n, note = page_one_count(fetcher, b)
        if n is None:
            conf = "unavailable"
        elif n >= PAGE_SIZE:
            conf = "floor_saturated"
        else:
            conf = "observed"
        rows.append({
            "source": "poshmark",
            "query": f"{b} women dresses",
            "brand": b,
            "listing_count": n,
            "confidence": conf,
            "note": note,
        })
    return rows
