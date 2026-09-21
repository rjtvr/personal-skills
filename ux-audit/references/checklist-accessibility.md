# Accessibility checklist (WCAG 2.2 A / AA)

Each item cites its success criterion so findings survive a compliance conversation.
Level A failures default to P0 on primary flows; Level AA failures default to P1.

## Contents
- Perceivable
- Operable
- Understandable
- Robust
- Common false positives

## Perceivable

- **1.1.1 Non-text Content (A)** — Every `<img>` has `alt`. Decorative images use `alt=""`,
  not a missing attribute. Icon-only buttons have an accessible name. Charts have a text
  alternative conveying the data, not just "chart".
- **1.3.1 Info and Relationships (A)** — Headings are real headings in order (no `<div
  class="h2">`, no skipping h1→h3). Lists are `<ul>/<ol>`. Tables use `<th>` with `scope`.
  Form controls associate with labels via `for`/`id`. Grouped radios sit in `<fieldset>`
  with `<legend>`.
- **1.3.5 Identify Input Purpose (AA)** — Fields collecting user data have appropriate
  `autocomplete` (`email`, `name`, `tel`, `street-address`).
- **1.4.1 Use of Color (A)** — Color is never the only carrier of meaning. Required fields,
  errors, and status indicators need a second signal: icon, text, or pattern.
- **1.4.3 Contrast Minimum (AA)** — 4.5:1 for normal text, 3:1 for large text (≥24px, or
  ≥19px bold). Check secondary text, placeholders, and text over images specifically —
  that's where failures cluster.
- **1.4.4 Resize Text (AA)** — Content usable at 200% zoom without loss. Fixed-height
  containers with text inside are the usual culprit.
- **1.4.10 Reflow (AA)** — No horizontal scrolling at 320px equivalent width.
- **1.4.11 Non-text Contrast (AA)** — 3:1 for UI component boundaries, focus indicators,
  icons, chart elements, and input borders. Frequently missed on subtle grey borders.
- **1.4.12 Text Spacing (AA)** — Layout survives increased line-height and letter-spacing.

## Operable

- **2.1.1 Keyboard (A)** — Every function reachable and operable by keyboard. Custom
  dropdowns, sliders, drag-and-drop, and canvas interactions are the usual gaps. Note that
  a `<div onClick>` is keyboard-inaccessible by default even with `role="button"` — it also
  needs `tabIndex={0}` and an Enter/Space handler, which is why native elements are the fix.
- **2.1.2 No Keyboard Trap (A)** — Focus can always leave. Modals must trap deliberately
  and release on Escape.
- **2.4.1 Bypass Blocks (A)** — A skip link, or landmarks (`<nav>`, `<main>`, `<header>`).
- **2.4.3 Focus Order (A)** — Tab order matches visual order. Positive `tabindex` values
  break this; CSS reordering (`flex-direction: row-reverse`, `order`) breaks it silently.
- **2.4.4 Link Purpose (A)** — Link text makes sense alone. "Read more" ×8 on one page is
  a failure.
- **2.4.7 Focus Visible (AA)** — Visible indicator on every focusable element.
  `outline: none` without a replacement is one of the most common serious defects in
  production frontends.
- **2.4.11 Focus Not Obscured (AA, 2.2)** — Sticky headers and footers must not cover the
  focused element.
- **2.5.3 Label in Name (A)** — Accessible name contains the visible label text, so voice
  control works.
- **2.5.8 Target Size Minimum (AA, 2.2)** — 24×24 CSS px minimum, with spacing exceptions.
  Aim for 44×44 on touch interfaces regardless — it's a usability floor, not just a
  compliance one.

## Understandable

- **3.1.1 Language of Page (A)** — `<html lang>` is set.
- **3.2.1 On Focus (A)** / **3.2.2 On Input (A)** — Focusing or changing a field doesn't
  trigger navigation or unexpected context change. Auto-submitting selects fail this.
- **3.2.6 Consistent Help (A, 2.2)** — Help mechanisms appear in consistent locations.
- **3.3.1 Error Identification (A)** — Errors described in text, tied to the offending
  field, programmatically associated via `aria-describedby`, and announced (live region).
- **3.3.2 Labels or Instructions (A)** — Visible labels. Placeholder-as-label is a failure:
  it disappears on input, often fails contrast, and isn't reliably announced.
- **3.3.3 Error Suggestion (AA)** — Say how to fix it, not just that it's wrong.
- **3.3.7 Redundant Entry (A, 2.2)** — Don't ask for the same information twice in a flow.
- **3.3.8 Accessible Authentication (AA, 2.2)** — No cognitive function test without an
  alternative. Blocking password managers from pasting fails this.

## Robust

- **4.1.2 Name, Role, Value (A)** — Custom components expose correct role, accessible name,
  and state. Toggles need `aria-pressed` or `aria-checked`; expandables need
  `aria-expanded`; comboboxes need the full pattern.
- **4.1.3 Status Messages (AA)** — Async results (search counts, save confirmations, cart
  updates, toasts) announce via `aria-live` without stealing focus.

## Common false positives

Flagging these erodes trust in the rest of the report:

- `aria-label` on an element that already has a visible label — redundant, not a defect,
  unless the two disagree (then it's 2.5.3).
- Missing `role` on native semantic elements. `<button>` doesn't need `role="button"`.
- Contrast on genuinely disabled controls — WCAG 1.4.3 exempts them. Still worth a P3
  usability note if users can't tell what's disabled.
- Low contrast on purely decorative elements carrying no information.
- `tabindex="-1"` — legitimate for programmatic focus targets like modal containers and
  error summaries.
