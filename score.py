"""Scoring: turn raw click counters into a ranked demand-supply gap.

Kept deliberately interpretable. A weighted, inspectable score that Ella can
argue with beats a model nobody can question, and every weight lives in WEIGHTS
below so disagreement is a config change rather than a rewrite.

The two momentum ratios come from the fact that ShopMy reports overlapping
cumulative windows:

    accel_short = daily_clicks / (weekly_clicks / 7)      today vs this week
    accel_mid   = (weekly_clicks / 7) / (monthly_clicks / 30)   week vs month

Two honest limitations, both handled rather than hidden:

1. Low-volume items produce wild ratios. A dress going from 1 to 7 clicks reads
   as 5x acceleration and means nothing. MIN_DAILY / MIN_WEEKLY gate this, and
   anything below the floor is classified `insufficient_volume`, never alerted.

2. `daily_clicks` is a single day and fashion traffic has day-of-week structure,
   so a weekend snapshot inflates accel_short across the board. A one-shot
   script cannot see this. The stored history can: `day_over_day` below compares
   like-for-like against the previous run, which is the correction.
"""

import math

MIN_DAILY = 5        # below this, accel_short is noise
MIN_WEEKLY = 20      # below this, the product is not meaningfully in play

WEIGHTS = {
    "heat": 0.25,             # how much is happening right now
    "momentum": 0.30,         # is it increasing
    "creator_breadth": 0.20,  # how many creators are pushing it
    "commerce_intent": 0.15,  # sustained click-through, not a one-day spike
    "recency": 0.10,          # how freshly creators are pinning it
}

RISING_THRESHOLD = 1.25
COOLING_THRESHOLD = 0.80
FADED_MID_THRESHOLD = 0.30


def _safe_div(a, b):
    if not a or not b:
        return None
    return a / b


def accel(p: dict) -> tuple[float | None, float | None]:
    d, w, m = p.get("daily_clicks"), p.get("weekly_clicks"), p.get("monthly_clicks")
    return _safe_div(d, (w / 7) if w else None), _safe_div((w / 7) if w else None,
                                                           (m / 30) if m else None)


def classify(p: dict) -> tuple[str, float | None, float | None]:
    """Label a product's current trajectory.

    Returns (label, accel_short, accel_mid). Labels map to what the brief asks
    us to distinguish: gaining momentum, at peak interest, or already past it.
    """
    a_short, a_mid = accel(p)
    daily = p.get("daily_clicks") or 0
    weekly = p.get("weekly_clicks") or 0

    if daily < MIN_DAILY or weekly < MIN_WEEKLY:
        return "insufficient_volume", a_short, a_mid
    if a_mid is not None and a_mid < FADED_MID_THRESHOLD:
        # Big monthly total, thin recent week: popular once, not now. This is
        # exactly the retrospective-report failure the brief warns against.
        return "faded", a_short, a_mid
    if a_short is not None and a_short >= RISING_THRESHOLD:
        return "rising", a_short, a_mid
    if a_short is not None and a_short < COOLING_THRESHOLD:
        return "cooling", a_short, a_mid
    return "peaking", a_short, a_mid


def _norm(v, lo, hi):
    if v is None:
        return 0.0
    return max(0.0, min(1.0, (v - lo) / (hi - lo))) if hi > lo else 0.0


def demand_score(p: dict, distinct_creators: int = 1, days_since_pin: float | None = None) -> float:
    """Composite 0-1 demand score. Log-scaled where counts are heavy-tailed."""
    a_short, a_mid = accel(p)
    heat = _norm(math.log1p(p.get("daily_clicks") or 0), 0, math.log1p(200))
    mom = _norm(((a_short or 0) + (a_mid or 0)) / 2, 0.5, 2.5)
    breadth = _norm(math.log1p(max(p.get("num_promoters") or 0, distinct_creators)),
                    0, math.log1p(1500))
    intent = _norm(math.log1p(p.get("monthly_clicks") or 0), 0, math.log1p(20000))
    rec = 1.0 if days_since_pin is None else _norm(-min(days_since_pin, 180), -180, 0)
    return round(
        WEIGHTS["heat"] * heat
        + WEIGHTS["momentum"] * mom
        + WEIGHTS["creator_breadth"] * breadth
        + WEIGHTS["commerce_intent"] * intent
        + WEIGHTS["recency"] * rec,
        4,
    )


def supply_pressure(listing_count: int | None) -> float:
    """0-1 where 1 means plenty of secondary supply already exists.

    Absence of data is not absence of supply. When we could not observe supply
    we return 0.5 rather than 0, so an unmeasured item cannot masquerade as a
    confirmed gap. That distinction is the whole point of the gap score.
    """
    if listing_count is None:
        return 0.5
    return _norm(math.log1p(listing_count), 0, math.log1p(500))


def gap_score(demand: float, listing_count: int | None) -> float:
    """High demand against thin secondary supply is TRACE's opportunity."""
    return round(demand * (1.0 - supply_pressure(listing_count)), 4)


def day_over_day(curr: dict, prev: dict | None) -> dict | None:
    """Real deltas between two stored runs.

    This is what persistence buys and a single snapshot cannot give: change in
    momentum, not just its level, plus a like-for-like comparison that is immune
    to the day-of-week confound in accel_short.
    """
    if not prev:
        return None
    out = {}
    for k in ("daily_clicks", "weekly_clicks", "monthly_clicks", "total_clicks",
              "num_promoters"):
        a, b = curr.get(k), prev.get(k)
        if a is not None and b is not None:
            out[f"d_{k}"] = a - b
    ca, _ = accel(curr)
    pa, _ = accel(prev)
    if ca is not None and pa is not None:
        out["d_accel_short"] = round(ca - pa, 3)
    return out or None
