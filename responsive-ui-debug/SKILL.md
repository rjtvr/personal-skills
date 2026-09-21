---
name: responsive-ui-debug
description: Diagnose and fix responsive layout bugs in HTML/CSS pages — especially horizontal overflow (the page scrolls sideways or content sticks to the screen edge), content that breaks only after an interaction like selecting a card, layouts that look wrong on mobile or stretched on desktop, and side padding that silently disappears. Use this whenever a user reports a UI that "breaks", "overflows", "scrolls sideways", "looks off on mobile/desktop", "sticks to the edge", or shares a screenshot of a broken layout — and ALWAYS measure the rendered page before changing any CSS, rather than guessing at fixes. Applies to artifacts, static HTML, and any web page you can open in a browser.
---

# Responsive UI Debugging

The single most important rule: **measure the rendered page, don't reason about the CSS blind.** Reading the stylesheet and guessing which rule is wrong wastes turns and often "fixes" a rule that was already correct while the real culprit sits elsewhere. Render the page, measure it, find the exact offending element, then fix that one thing and re-measure to confirm.

## When to use this

Any report that the layout is broken: sideways scrolling, content flush to the screen edge with no gutter, cards/text overflowing, "looks fine on desktop but breaks on mobile" (or vice versa), or a bug that only appears after the user interacts (selects an option, expands a panel). Screenshots are a strong trigger. If the user has already told you the exact symptom, still measure first — the symptom tells you *what* they see, not *which element* causes it.

## The workflow

### 1. Reproduce and measure (before touching any CSS)

Use the bundled `scripts/diagnose.py`. It renders the page at several widths, checks whether the document is wider than the window (horizontal overflow), and lists the specific elements that exceed the viewport. If the bug only shows after an interaction, pass a selector and it clicks those elements one at a time, measuring after each — this is how you catch "breaks when I select the second option" bugs.

```bash
# one-time setup if Playwright isn't present
pip install playwright --break-system-packages -q
python -m playwright install chromium

# measure a static page across widths
python scripts/diagnose.py path/to/page.html

# reproduce an interaction bug: toggle each ".src" card one by one
python scripts/diagnose.py path/to/page.html --click ".src" --max-clicks 6 --shots /tmp/shots
```

The output names the culprit, e.g. `main.(no class) (left=0 right=491)` on a 390px screen means `<main>` is 101px too wide. Fix the **outermost** culprit listed — inner elements usually just inherit overflow from a parent that refuses to shrink.

For anything visual (spacing, alignment, "sticks to the edge"), also take a screenshot and **look at it** with the view tool — measuring catches overflow, but only your eyes catch a missing gutter or bad alignment. A quick inline Playwright snippet:

```python
from playwright.sync_api import sync_playwright
import pathlib
url = "file://" + str(pathlib.Path("page.html").resolve())
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg.goto(url); pg.wait_for_timeout(800)
    pg.screenshot(path="/tmp/m.png")   # then view /tmp/m.png
    # measure anything specific:
    print(pg.evaluate("""() => {
      const el = document.querySelector('.thing');
      const r = el.getBoundingClientRect();
      return { left: r.left, right: r.right, padL: getComputedStyle(el).paddingLeft };
    }"""))
    b.close()
```

### 2. Identify the cause

Match the culprit to the fixes below. Overflow almost always traces to one of two roots: a **grid or flex child that won't shrink** below its content's width, or a **fixed/intrinsic width** (a long unbreakable string, a form control's default size, a hardcoded px width) that props a container open.

### 3. Fix the one culprit

Apply the matching fix from the next section. Change one thing.

### 4. Re-measure to confirm

Run `diagnose.py` again with the same arguments. It exits 0 when clean, 1 when overflow remains — so it doubles as a regression check. **Do not publish or hand back the fix until the measurement confirms it.** Verifying before publishing is the whole point; skipping it is how you end up "fixing" the same bug repeatedly.

## Common fixes

These are the recurring causes, roughly in order of how often they're the real problem.

### Grid/flex child won't shrink → `min-width: 0` / `minmax(0, 1fr)`

The most common overflow cause. Grid and flex items default to `min-width: auto`, meaning they refuse to shrink below their content's intrinsic size. A long URL or unbreakable string in a child then forces the whole track wider than the screen.

- **Flex child:** add `min-width: 0` to the flex item (and often `width: 0; flex: 1 1 0` on the specific column that holds the long text, so it takes available width rather than content width).
- **Grid track:** `1fr` is really `minmax(auto, 1fr)`. Replace it with `minmax(0, 1fr)` so the cell can shrink. Do this on every track that holds variable content: `grid-template-columns: minmax(0, 1fr) 340px`. Add `min-width: 0` to the grid items too.

This bug frequently appears **only after an interaction** (selecting a card adds content or a wider state), which is why step 1 clicks through states.

### Long unbreakable strings (URLs) → `word-break: break-all`

A monospace URL with no spaces won't wrap with `overflow-wrap: anywhere` alone. Use `word-break: break-all` for URL-like strings so they break at any character and wrap to the next line instead of extending the container. Pair with a shrunk container (above) so there's a boundary to wrap against. To make the card grow taller instead of wider, make the URL a block: `display: block; width: 100%`.

### Form controls have intrinsic width → `cols`/`size` + `min-width: 0`

`<textarea>` has a default `cols="20"` and `<input>` a default `size`, both of which set an intrinsic width from an HTML attribute that CSS `width: 100%` doesn't reliably override on mobile. A wide textarea then scrolls the whole page. Fix: set `cols="1"` (or `size="1"`) so CSS owns the width, plus `max-width: 100%; min-width: 0` on the element. A long single-line placeholder can also prop it open — keep placeholders short or wrapped.

### Side padding silently disappears → shorthand vs long-hand collision

If content sticks to the screen edge with no gutter, a `padding` **shorthand** is likely overriding a `padding-left`/`padding-right` set on the same element by another class. When one class sets `padding: 20px 0` (top/bottom, and **0** left/right) and another sets the side padding, the shorthand wins for all four sides if it comes later with equal specificity — zeroing the gutter. Fix: in the class that only means to set vertical spacing, use `padding-top`/`padding-bottom` (long-hand) so it doesn't touch left/right. Generally, when two classes on one element each own part of the spacing, use long-hand properties so they can't clobber each other. `padding-inline` + `clamp()` occasionally fail to apply in some renderers too — if a gutter is missing despite looking correct in the CSS, fall back to explicit `padding-left`/`padding-right` with a media query to tell whether the problem is your value or the property being honored.

### Desktop too wide / stretched → cap the measure

Not overflow, but a common "looks wrong on desktop" complaint. Full-width text gives unreadably long lines. Cap the container (`max-width`) to something appropriate for the content, and cap text blocks with `max-width: 62ch` (or ~60–75ch) so lines wrap at a comfortable reading measure. `ch` units cap by character count, the proper way to set a text measure.

### Whole-page safety nets

- `overflow-x: hidden` on `html` and `body` stops the page scrolling sideways — but treat it as a backstop, not the fix. It hides the symptom; still find and fix the element that overflows, or content gets clipped.
- Mobile text looks huge and overflows on iOS only: add `-webkit-text-size-adjust: 100%` to `html` to stop Safari inflating text past the size you set.
- Use the correct viewport tag: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`. Use `100dvh` rather than `100vh` so mobile browser toolbars don't cause layout jumps.

## Responsive layout defaults (when building, not just fixing)

- Fluid type and spacing with `clamp(min, preferred-vw, max)` so sizes scale smoothly between phone and desktop instead of jumping at breakpoints.
- One grid that reflows: single column on mobile, multi-column above a breakpoint (`@media (min-width: 820px)`), using `minmax(0, …)` tracks from the start.
- Touch targets ≥ 44px tall on interactive elements.
- Respect `prefers-reduced-motion` and keep visible keyboard focus.

## Pitfalls

- **Don't guess from the stylesheet.** If you haven't measured, you don't know the culprit. The rule you're staring at may already be correct.
- **Don't fix the symptom's element — fix the outermost culprit.** Inner elements inherit overflow from a parent that can't shrink.
- **Don't publish before re-measuring.** The confirm step is not optional.
- **Cached views mislead.** If the user still sees the old layout after a real fix, consider that they may be viewing a cached/old version — but only conclude that after your own measurement shows the fix is genuinely applied.
