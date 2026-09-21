---
id: A-01
title: "Search input has no programmatic label"
type: bug              # bug | task | chore | improvement
priority: P1           # P0 | P1 | P2 | P3
area: accessibility    # accessibility | visual | usability | performance
component: SearchBar
files:
  - src/components/SearchBar.tsx:24
criterion: "WCAG 4.1.2 Name, Role, Value (Level A)"
reach: global-header   # single-screen | flow | shared-component | global
estimate: S            # XS | S | M | L | XL
blocked_by: []
closes_findings: [A-01, A-07]
labels: [a11y, forms, wcag-a]
---

## Problem

[One paragraph, written for someone who did not read the audit. State what is wrong and
what a user experiences — not what the code looks like. The code detail goes in Context.]

## Impact

[Who is affected and what they cannot do. Quantify reach if known: "every screen, since
this sits in the global header."]

## Context

**Observed:** [the actual evidence — the line of code, the measured contrast ratio, the
screenshot region. Concrete, quoted where possible.]

**Root cause:** [if known. If several tickets share a root cause, say so and link them —
whoever picks this up should know they might be fixing three tickets at once.]

## Proposed fix

[Specific enough to implement, loose enough to respect existing patterns. Point at an
existing convention in the codebase if one exists.]

**Do not:** [guardrails — the wrong fixes that look right]

## Acceptance criteria

- [ ] [Observable, testable outcome — not "label added" but "screen reader announces the
      field name on focus"]
- [ ] [Regression guard — what must still work]
- [ ] [Verification step someone can actually perform]

## Notes

[Open questions, decisions needed from design or product, links to related tickets.]
