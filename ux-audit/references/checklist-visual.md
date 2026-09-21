# Visual consistency and design-system drift

The goal here is to separate **inconsistency** (objective, fixable, worth reporting) from
**taste** (subjective, usually not your call). Report the former. Raise the latter only
when it demonstrably costs comprehension, and mark it as opinion.

## Token drift

The highest-value visual findings, because they're objective and fix once/apply everywhere.

- **Color.** Count distinct color values in the codebase. If a token file defines 12 greys
  and the code uses 30 hex values, that's the finding — quantify it. Look for near-duplicates
  (`#333` and `#343434` in the same view) which indicate copy-paste rather than intent.
- **Spacing.** Extract every margin/padding value. A healthy system clusters on a scale
  (4/8/12/16/24/32). Values like `13px`, `27px`, `7px` are eyeballed one-offs. Report the
  distribution, not each instance.
- **Typography.** Count font sizes, weights, and line-heights in use. More than ~7 sizes
  usually means no scale. Check line-height on body copy — under 1.4 hurts readability at
  paragraph length.
- **Radii, borders, shadows.** Three shadow definitions is a system; eleven is drift.
  Inconsistent radii between a card and the button inside it reads as sloppy even when
  nobody can name why.

Frame each as: *N distinct values where the system defines M*, with the file locations of
the worst offenders and one canonical replacement.

## Layout and hierarchy

- **Primary action clarity.** One dominant action per view. If nothing dominates, the user
  hesitates; if everything dominates, the same.
- **Proximity and grouping.** Related elements closer than unrelated ones. Label-to-input
  gap should be smaller than the gap between fields — a very common inversion.
- **Alignment.** Minimize distinct alignment edges. Mixed centered and left-aligned content
  in one block rarely survives real content lengths.
- **Optical vs mathematical centering.** Icons inside circular buttons, text in pills, and
  triangular glyphs often need a nudge. P3, but it's the difference between "fine" and
  "considered".
- **Content-length resilience.** Does the layout hold with a 60-character name? An empty
  list? 10,000 rows? Designs are drawn with convenient data; builds meet real data.

## State coverage

Enumerate for each significant component, and report *missing* states as findings — an
unhandled state is a real defect that surfaces at the worst moment:

- default / hover / focus / active / disabled
- loading (and does it prevent double-submit?)
- empty (does it explain what to do, or just show nothing?)
- error (recoverable? does it say how?)
- partial / stale data
- long-content and overflow

Empty and error states are the two most commonly missing and the two that most affect
perceived quality.

## Motion

- Transitions in the 150–300ms range for UI feedback; longer reads as sluggish.
- Nothing animates that blocks input.
- `prefers-reduced-motion` is respected — this is an accessibility requirement (2.3.3 at
  AAA, but vestibular-disorder impact makes it a real P1/P2 in practice, not a nicety).
- Consistent easing. Mixed `linear` and `ease-out` across sibling components is drift.

## Cross-platform and responsive

- Breakpoint behaviour: does anything become unusable *between* designed breakpoints?
- Touch targets on mobile viewports (44×44 practical minimum).
- Hover-dependent functionality has a touch equivalent — hover-only menus and tooltips
  strand touch users entirely.
- Dark mode, if present: check contrast independently. Ratios that pass in light mode
  routinely fail inverted, and pure `#000` backgrounds with pure `#fff` text cause halation.
