# UI/UX Audit — [Product / Surface]

**Date:** [YYYY-MM-DD]
**Scope:** [which screens, flows, or components]
**Evidence used:** [screenshots | source at `path` | live URL | design file] — list only
what was actually inspected.
**Not covered:** [what was out of reach, and why it matters]

## Summary

[3–5 sentences. What's the overall state? What is the single highest-leverage fix? Lead
with the thing that, if only one change happens, should be that change.]

| Severity | Count |
|---|---|
| P0 Blocker | |
| P1 High | |
| P2 Medium | |
| P3 Low | |

**Highest-leverage fix:** [usually a shared component or token change that closes several
findings at once — name it and say how many findings it closes]

---

## P0 — Blockers

### [A-01] [Short title]

**Where:** `path/to/file.tsx:LINE` — or screenshot region if visual-only
**Evidence:** [what was actually observed, quoted or described — not inferred]
**Impact:** [which users, what they cannot do]
**Criterion:** [WCAG X.X.X Name (Level) — omit for non-a11y findings]
**Reach:** [how many screens/users this touches]
**Fix:** [concrete change]

---

## P1 — High

[same structure]

## P2 — Medium

[same structure — these may be grouped when they share a root cause, e.g. "17 hardcoded
greys across 9 files" as one finding rather than 17]

## P3 — Low

[can be a terse list; full structure is overkill here]

---

## Systemic observations

[Patterns rather than instances. "Focus styles are removed globally in `reset.css` and
never restored" explains a dozen findings and is more useful than the dozen. Process
observations belong here too — e.g. designs not specifying error states.]

## Unverified

[Findings suspected but not confirmable with available evidence, and what would confirm
each. Being explicit here is what makes the rest of the report trustworthy.]
