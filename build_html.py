"""Render FINDINGS.md to a print-ready HTML file for PDF export.

macOS has no HTML-to-PDF filter available (cupsfilter refuses text/html), so the
workflow is: run this, open FINDINGS.html in a browser, Cmd+P, Save as PDF.

Run:  python build_html.py
"""

import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).parent

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
       font-size: 10.5pt; line-height: 1.55; color: #1a1a1a; }
h1 { font-size: 20pt; border-bottom: 2px solid #1a1a1a; padding-bottom: 6px; margin-bottom: 4px; }
h2 { font-size: 14pt; margin-top: 26px; border-bottom: 1px solid #ccc; padding-bottom: 4px;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; margin-top: 20px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 9.5pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #d0d0d0; padding: 5px 8px; text-align: left; vertical-align: top; }
th { background: #f4f4f4; font-weight: 600; }
code { font-family: "SF Mono", Menlo, monospace; font-size: 9pt; background: #f4f4f4;
       padding: 1px 4px; border-radius: 3px; }
pre { background: #f7f7f7; border: 1px solid #e2e2e2; padding: 10px; overflow-x: auto;
      font-size: 8.5pt; line-height: 1.35; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3px solid #888; margin-left: 0; padding-left: 14px; color: #333; }
hr { border: none; border-top: 1px solid #ddd; margin: 22px 0; }
strong { font-weight: 650; }
li { margin-bottom: 4px; }
"""


def main() -> None:
    src = (ROOT / "FINDINGS.md").read_text()
    # Repo-relative links mean nothing in a standalone PDF.
    src = re.sub(r"\[`PROBE_LOG\.md`\]\([^)]*\)", "`PROBE_LOG.md` (included in the repo)", src)
    body = markdown.markdown(src, extensions=["tables", "fenced_code", "sane_lists"])
    html = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>TRACE Demand Radar: Findings</title>"
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )
    out = ROOT / "FINDINGS.html"
    out.write_text(html)
    print(f"wrote {out.name} ({len(html):,} bytes) from FINDINGS.md")
    print("Now: open it in a browser, Cmd+P, Save as PDF.")


if __name__ == "__main__":
    main()
