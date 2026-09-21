# Interview protocol

The audit does not start until the brief is approved. This file is the question set.

## Principle: never ask what you can observe

Read-only recon comes first — list the component directory, check for a token file, note
the framework, count the screens. Then ask only what recon can't answer.

Asking "what framework are you using?" when `package.json` is right there signals that the
skill isn't paying attention, and it burns the person's patience before the useful questions
arrive. Recon exists to earn the right to ask fewer, better questions.

Recon means listing and reading structure. It does not mean evaluating, and it produces no
findings. If you catch yourself forming an opinion about the code during recon, hold it
until the brief is approved.

## The questions

Ask in this order. Use `AskUserQuestion` where available — options are faster than prose on
any device. Group two or three per turn; a six-turn interrogation is worse than the problem
it solves. **Skip any question recon already answered**, and say what you found instead:
"I can see a token file at `src/tokens.css` — I'll check drift against it."

**1. Surface** — What exactly is in scope? Offer what recon found: all 34 components, the
8 shared primitives, the 3 screens in the screenshots, or one named component.

**2. Audience and context** — Who uses this, and in what setting? A consumer signup flow, an
internal admin tool, and a regulated healthcare interface get different severity weighting
for the same finding. Ask directly whether accessibility compliance is a stated requirement
— that single answer changes the ranking of half the findings.

**3. Evidence** — Which sources can you actually provide? Screenshots, repo access, a live
URL, design files. Name what recon already located and ask what's missing. Say plainly what
each absent source costs: without a live URL there's no keyboard-navigation or reflow check.

**4. Depth** — Full audit, P0/P1 only, or a single dimension (accessibility only, visual
consistency only)? Give a rough finding-count estimate for each so the choice is informed.

**5. Output** — Report only, report plus fix plan, or plus tickets. Default to report plus
fix plan; ask before generating tickets, since an unwanted `tickets/` directory is noise.

**6. Constraints** — Anything off-limits, mid-refactor, or already known? Existing design
system to measure against? Known issues not worth re-reporting? This question prevents the
most common wasted output: a careful finding about something they're already rewriting.

## Locking the brief

Write `AUDIT_BRIEF.md` from `assets/AUDIT_BRIEF_template.md`, show it, and stop.

The brief is a contract, not a summary. It exists so the person can correct a
misunderstanding before it becomes forty findings against the wrong scope, and so that
"you audited the wrong thing" is a two-line fix rather than a redo.

Ask for explicit approval. **Anything other than clear approval is not approval** —
"looks good but maybe also check the modals" is a revision. Update the brief and re-confirm.

Do not begin the checklists until approval arrives. Writing the brief and continuing in the
same turn defeats the entire mechanism.

## Once approved

The brief is the scope. If something outside it looks serious mid-audit, note it and ask
rather than silently widening — scope creep in an audit is how a two-hour review becomes a
two-day one.

If the audit diverges materially from the brief — findings far above the estimate, evidence
thinner than expected — stop and re-confirm rather than pressing on.
