# Evidence gathering

How to inspect each source. Use whatever is available; state in the report which sources
were used, because that determines what the audit could possibly have caught.

## Screenshots and recordings

Look at the image before reading any code, and describe what you see in structural terms
first — where the eye lands, what competes for attention, what groups together. Reading
code first biases you toward the developer's mental model rather than the user's.

Check for:

- **Hierarchy** — is the primary action visually dominant? If three buttons have equal
  weight, the user has no default.
- **Spacing rhythm** — do gaps look like a system (4/8/12/16) or arbitrary? Related items
  should sit closer than unrelated ones (proximity is the strongest grouping signal).
- **Alignment** — count vertical edges. More than 2–3 distinct left edges in one column
  usually reads as messy.
- **Density and breathing room** — is anything crammed against a container edge?
- **Contrast, judged in situ** — placeholder grey on white, disabled states, text over
  images, secondary labels. Flag suspects for measurement rather than guessing ratios.
- **Truncation and overflow** — ellipses, clipped text, wrapping that breaks layout.
- **State coverage** — do you have screenshots of loading, empty, error, and success? If
  only the happy path was provided, that absence is itself a finding to raise.

For recordings, additionally watch: how long the user hesitates, where they backtrack,
what has no feedback on interaction, and whether transitions obscure content.

## Source code

Grep-driven passes are efficient. Useful starting patterns (adjust per framework):

```bash
# Interactive elements built from non-interactive tags
grep -rn "onClick" --include=*.tsx --include=*.jsx src | grep -E "<(div|span|li|p)"

# Images without alt
grep -rn "<img" --include=*.tsx src | grep -v "alt="

# Hardcoded colors instead of tokens
grep -rEn "#[0-9a-fA-F]{3,8}|rgba?\(" --include=*.css --include=*.tsx src

# Focus indicators being removed
grep -rn "outline:\s*none\|outline: 0\|focus:outline-none" src

# Positive tabindex (almost always a bug)
grep -rn "tabIndex={[1-9]" src

# Suppressed or absent form labels
grep -rn "<input" --include=*.tsx src | grep -v -E "aria-label|id="
```

Then read the shared primitives — `Button`, `Input`, `Modal`, `Select`, `Table` — in full.
Defects there have the widest reach and the best fix-to-benefit ratio.

Framework notes:

- **React** — check `useEffect` focus management on route change and modal open, whether
  modals trap focus and restore it on close, and whether list items use stable keys
  (unstable keys cause focus loss mid-interaction).
- **Angular** — check `[attr.aria-*]` bindings actually resolve, `ngIf` vs `hidden` (the
  latter keeps elements in the accessibility tree), and CDK `A11yModule` usage for focus
  trapping and live announcements.
- **Either** — a design-token file that exists but is bypassed by inline styles is one of
  the highest-yield findings available. Compare token definitions against actual usage.

## Live URL

Manual passes, in this order, because early failures make later tests moot:

1. **Keyboard only.** Tab from the top. Can you reach every interactive element? Can you
   see where you are at every step? Can you escape every modal and menu? Does focus order
   follow visual order? A trap or an invisible focus ring is P0/P1 territory.
2. **Zoom to 200%** (browser zoom). Does anything overlap, clip, or become unreachable?
3. **Narrow to 320px width.** Is there horizontal scrolling? WCAG 1.4.10 Reflow.
4. **Contrast sampling.** Measure real rendered values for body text, secondary text,
   placeholders, disabled states, focus rings, borders, and icons.
5. **Break something on purpose.** Submit an empty form. Enter an invalid value. Kill the
   network. Error handling is where UX quality actually shows, and it's the part most
   audits skip.
6. **Automated sweep**, if tooling is available (`axe-core`, Lighthouse). Treat results as
   a starting point — automated tools catch roughly a third of accessibility issues and
   catch none of the usability ones. Never present a Lighthouse score as an audit.

## Design files

You're looking for **drift**, not for whether the design is good.

- Extract the intended token set: color ramp, type scale, spacing scale, radii, elevation.
- Compare against what the code defines and what the screenshots render.
- Note which states the design actually specifies. Designs that omit error, empty,
  loading, and disabled states usually produce builds that improvise them inconsistently —
  worth naming as a process finding, not just a code one.
- Where build and design disagree, don't assume the design is right. Sometimes the
  developer fixed a real problem. Flag the divergence and ask.
