"""Measured precision of the radar's own hypotheses.

The system's job is not to rank dresses. It is to identify presale
opportunities: accelerating demand where secondary supply has NOT yet formed.
So the claim to evaluate is that one, and the only way to check it is a manual
product-level supply check on platforms the radar cannot reach.

This is deliberately the same discipline as verifying an agent against ground
truth rather than against its own report. The radar "reports success" by ranking
an item into its actionable board; this script checks that against what a human
actually found.

The honest headline is that precision is 1 of 3. Two of the system's three
hypotheses were refuted by manual checks. That number is small enough to be
directional and nothing more, and the script prints that caveat rather than
letting the figure stand alone.

Run:  python eval/precision.py
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MIN_N_FOR_CONFIDENCE = 20


def load() -> dict:
    return yaml.safe_load((Path(__file__).parent / "labels.yaml").read_text())


def main() -> int:
    data = load()
    labels = data.get("labels") or []
    taxonomy = data.get("taxonomy") or {}

    if not labels:
        print("No labels yet.")
        return 0

    confirmed = [l for l in labels if l["manual_verdict"] == "CONFIRMED"]
    refuted = [l for l in labels if l["manual_verdict"] == "REFUTED"]
    n = len(labels)
    precision = len(confirmed) / n if n else 0.0

    print("=" * 78)
    print("PRECISION ON THE SYSTEM'S OWN HYPOTHESES")
    print("=" * 78)
    print(f"\n  Hypotheses checked : {n}")
    print(f"  Confirmed          : {len(confirmed)}")
    print(f"  Refuted            : {len(refuted)}")
    print(f"  Precision          : {len(confirmed)}/{n} = {precision:.0%}")

    print(f"\n{'RANK':<6}{'PRODUCT':<30}{'VERDICT':<12}{'FAILURE MODE'}")
    print("-" * 78)
    for l in sorted(labels, key=lambda x: x.get("system_rank") or 99):
        print(f"#{str(l.get('system_rank')):<5}{str(l['title'])[:29]:<30}"
              f"{l['manual_verdict']:<12}{l.get('failure_category') or '-'}")

    print("\n" + "-" * 78)
    print("WHAT FAILED, AND WHY IT IS DIAGNOSABLE RATHER THAN VAGUE")
    print("-" * 78)
    seen = []
    for l in refuted:
        cat = l.get("failure_category")
        if cat in seen:
            continue
        seen.append(cat)
        t = taxonomy.get(cat, {})
        print(f"\n  [{cat}]  severity: {t.get('severity', '?')}")
        print(f"    what      : {' '.join(str(t.get('description', '')).split())}")
        print(f"    root cause: {t.get('root_cause', '?')}")
        print(f"    fix       : {t.get('fix', '?')}")

    mitigated = [k for k, v in taxonomy.items() if "Already handled" in str(v.get("fix", ""))]
    if mitigated:
        print("\n  Already mitigated in code: " + ", ".join(mitigated))

    print("\n" + "=" * 78)
    print("READ THIS BEFORE QUOTING THE NUMBER")
    print("=" * 78)
    print(f"""
  n = {n}. A precision figure on three labels is directionally useful and
  statistically meaningless. It is reported because the direction matters:
  the system's demand detection held up under three independent corroborations
  (click acceleration, TikTok volume and recency, Poshmark price retention),
  while its OPPORTUNITY claims failed twice out of three.

  That is a specific, locatable defect rather than a general unreliability. The
  demand half works. The supply half is blind, because the platform that decides
  the answer is the one that cannot be scraped.

  The practical consequence: this system should be used to generate candidates
  for a human to qualify, and should NOT be trusted to rank opportunities on its
  own. Anything above {MIN_N_FOR_CONFIDENCE} labels would be needed before the
  precision figure carried real weight.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
