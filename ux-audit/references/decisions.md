# Decisions: what to gate, what to log

Two categories, handled differently. Confusing them produces either an unusable
interrogation or silent assumptions — both failures.

## Gates — stop and ask

A short, fixed list. These are irreversible, scope-defining, or produce artifacts the
person didn't ask for. Never self-authorize one:

1. **Starting the audit** — the brief must be approved (see `interview.md`).
2. **Expanding scope beyond the brief** — including "while I was in there" findings from
   files outside the agreed scope. Note them, ask, don't absorb them.
3. **Creating `tickets/`** — never generated unless explicitly requested.
4. **Modifying any source file.** This skill audits; it does not fix. Even an obviously
   correct one-line fix waits for a separate request. A review that edits code while
   reviewing it destroys the reviewability of both.

That's the whole list. Everything else gets logged instead.

## The log — decide, but show your work

Write `DECISIONS.md` alongside the audit, using `assets/DECISIONS_template.md`.

**Threshold: log a decision when a reasonable reviewer might have made it differently.**
That's the whole test. Don't log "read `Button.tsx`" — that's a step, not a decision. Do
log "treated the three near-identical greys as one finding rather than three".

A log that records every action is as useless as no log, because the reviewable decisions
disappear into the noise. Expect roughly 5–15 entries on a normal audit.

### What to log

- **Severity calls**, particularly anything rated P0/P1, and anything you dropped a level
  because it looked like taste.
- **Aggregation** — collapsing many instances into one finding, or splitting one into many.
- **Exclusions** — something noticed and deliberately not reported, and why.
- **Assumptions about intent** — "assumed the muted grey on the secondary label is
  deliberate rather than an error".
- **Ambiguous evidence** — where two readings were possible and you picked one.
- **Anything where you nearly asked but didn't.** That hesitation is the signal.

### Entry format

```markdown
### D-03 — Merged 17 hardcoded greys into one finding

- **Decided:** one finding (V-04) listing 17 locations
- **Alternative:** 17 separate findings
- **Because:** single root cause; one token fix closes all 17
- **Assumed:** you want findings shaped like fixes, not like instances
- **Reverse it:** say "split V-04" and I'll expand it
```

**Reverse it** is the field that makes the log worth writing. A decision you can see but
can't easily undo isn't really under your control.

### Mark them inline

Findings that rest on a logged decision carry the ID: `### [P2] Inconsistent greys [D-03]`.
Without this you'd have to cross-reference the whole log against the whole report to find
what a given decision affected.

## When uncertain, don't quietly pick

If a decision could go either way and it materially changes the output, mark the finding
`[unresolved]` and state both readings rather than choosing and logging. The log is for
decisions you're confident in; genuine ambiguity should surface, not be recorded as settled.

## Present it

When delivering the audit, say how many decisions were logged and name the two or three
most consequential. A log nobody knows to read is the same as no log.
