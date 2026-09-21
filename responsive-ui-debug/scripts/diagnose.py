#!/usr/bin/env python3
"""
Responsive UI overflow diagnostic.

Renders an HTML file at several viewport widths with Playwright, checks for
horizontal overflow (document wider than the window), and — when a CSS selector
for repeated interactive elements is given — clicks them one at a time to catch
overflow that only appears AFTER a state change (e.g. selecting a card).

For every width and every interaction step it reports whether the page overflows
and, when it does, lists the specific elements that exceed the viewport so you
fix the real culprit instead of guessing.

Usage:
    python diagnose.py <file-or-url> [--click SELECTOR] [--max-clicks N]
                       [--widths 320,390,768,1200] [--shots DIR]

Examples:
    python diagnose.py app.html
    python diagnose.py app.html --click ".src" --max-clicks 6 --shots /tmp/shots
    python diagnose.py https://example.com --widths 360,414

Exit code is 0 when no overflow is found at any width/step, 1 otherwise — so it
can double as a regression check.
"""
import argparse, pathlib, sys

MEASURE = """() => {
  const de = document.documentElement;
  const winW = window.innerWidth;
  const over = de.scrollWidth > winW + 1;
  const culprits = [];
  if (over) {
    document.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (r.right > winW + 1 || r.left < -1) {
        culprits.push({
          tag: el.tagName.toLowerCase(),
          cls: (typeof el.className === 'string' ? el.className : '') || '(no class)',
          left: Math.round(r.left), right: Math.round(r.right)
        });
      }
    });
  }
  // Keep the outermost offenders — inner elements usually inherit the overflow
  // from a parent that can't shrink, and the parent is what you fix.
  return { docW: de.scrollWidth, winW, over, culprits: culprits.slice(0, 6) };
}"""


def run(target, click, max_clicks, widths, shots):
    from playwright.sync_api import sync_playwright

    if "://" not in target:
        target = "file://" + str(pathlib.Path(target).resolve())
    if shots:
        pathlib.Path(shots).mkdir(parents=True, exist_ok=True)

    any_overflow = False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in widths:
            page = browser.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1)
            page.goto(target)
            page.wait_for_timeout(600)

            res = page.evaluate(MEASURE)
            _report(w, "initial", res)
            any_overflow |= res["over"]
            if res["over"] and shots:
                page.screenshot(path=f"{shots}/w{w}_initial.png")

            if click:
                els = page.query_selector_all(click)
                n = len(els) if max_clicks is None else min(max_clicks, len(els))
                if not els:
                    print(f"  [w={w}] no elements match '{click}'")
                for i in range(n):
                    # re-query each time — the DOM may have re-rendered
                    els = page.query_selector_all(click)
                    if i >= len(els):
                        break
                    els[i].click()
                    page.wait_for_timeout(150)
                    res = page.evaluate(MEASURE)
                    _report(w, f"click #{i+1}", res)
                    any_overflow |= res["over"]
                    if res["over"] and shots:
                        page.screenshot(path=f"{shots}/w{w}_click{i+1}.png")
            page.close()
        browser.close()

    print()
    if any_overflow:
        print("RESULT: overflow found. Fix the outermost culprit above, then re-run.")
        print("See ../SKILL.md 'Common fixes' for the rule that matches the culprit.")
    else:
        print("RESULT: no horizontal overflow at any width or interaction step. ✓")
    return 1 if any_overflow else 0


def _report(width, step, res):
    flag = "  <-- OVERFLOW" if res["over"] else ""
    print(f"[w={width}] {step}: docW={res['docW']} winW={res['winW']}{flag}")
    for c in res["culprits"]:
        print(f"        {c['tag']}.{c['cls']}  (left={c['left']} right={c['right']})")


def main():
    ap = argparse.ArgumentParser(description="Diagnose responsive horizontal overflow.")
    ap.add_argument("target", help="HTML file path or URL")
    ap.add_argument("--click", help="CSS selector for repeated elements to toggle one by one")
    ap.add_argument("--max-clicks", type=int, default=6, help="Max elements to click (default 6)")
    ap.add_argument("--widths", default="320,390,768,1200", help="Comma-separated viewport widths")
    ap.add_argument("--shots", help="Directory to save screenshots of overflowing states")
    args = ap.parse_args()

    widths = [int(x) for x in args.widths.split(",") if x.strip()]
    try:
        sys.exit(run(args.target, args.click, args.max_clicks, widths, args.shots))
    except ImportError:
        print("Playwright not installed. Run:")
        print("  pip install playwright --break-system-packages -q")
        print("  python -m playwright install chromium")
        sys.exit(2)


if __name__ == "__main__":
    main()
