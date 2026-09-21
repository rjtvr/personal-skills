# Fix Plan — [Product / Surface]

Generated from `UX_AUDIT.md`. Read that file for the reasoning behind any finding ID.

**How to use this:** work batches in order. Batches are ordered so that earlier ones
cascade into later ones — fixing a shared primitive often closes several page-level
findings, so re-check the audit after each batch before doing redundant work. Verify
each batch before moving on.

**Assumed stack:** [framework, styling approach, test runner]
**Branch suggestion:** `fix/ux-audit-p0-p1`

---

## Batch 1 — [Name, e.g. "Restore focus indicators"]

**Closes:** A-01, A-04, A-09
**Why first:** [cascade reasoning — e.g. "global reset removes outlines; restoring here
fixes every downstream component, so do this before touching individual components"]
**Blast radius:** [Low | Medium | High] — [what else this touches]

### Task 1.1 — [Specific change]

- **Files:** `src/styles/reset.css`, `src/styles/tokens.css`
- **Change:** [Concrete. Name the property, the value, the pattern to follow. Reference an
  existing convention in the codebase if one exists, so the fix looks native rather than
  bolted on.]
- **Do not:** [guardrails — e.g. "do not add outlines to `:focus`; use `:focus-visible` so
  mouse users don't see rings"]
- **Verify:** [Observable check — "Tab through the login form; every control shows a ring
  meeting 3:1 against its background"]

### Task 1.2 — [...]

---

## Batch 2 — [Name]

[same structure]

---

## Verification for the whole plan

Run after all batches:

- [ ] Keyboard-only pass through [primary flow] — no traps, focus always visible
- [ ] Zoom to 200% — no clipping or overlap
- [ ] Narrow to 320px — no horizontal scroll
- [ ] Automated a11y sweep (`axe`/Lighthouse) shows no new violations
- [ ] Existing test suite passes
- [ ] [product-specific check]

---

## Explicitly out of scope

Do not do these in this pass:

- [Item] — [reason: deferred, needs design input, needs a product decision]

If a task in this plan seems to require work listed here, stop and ask rather than
expanding scope.

---

## Open questions

Things that need a human decision before the relevant task can proceed. Surface these
early rather than guessing:

- [Question] — blocks Task X.Y
