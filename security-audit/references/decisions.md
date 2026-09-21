# Decisions: what to gate, what to log

Two categories, handled differently — and in a security context the gate list is longer,
because the actions have consequences outside the report.

## Gates — stop and ask

Never self-authorize any of these:

1. **Starting the audit** — the brief must be approved (see `interview.md`).
2. **Running any scanner not ticked in the brief's authorized-actions list.** Approval for
   semgrep is not approval for trivy.
3. **Full git-history scanning** — separately, even if a working-tree secret scan was approved.
4. **Network access** — CVE lookups, `npm audit`, advisory fetches. The code may be under
   an agreement that restricts what leaves the machine.
5. **Scanning anything outside the brief's scope.** If something out of scope looks
   serious, name it and ask. Scanning a system you weren't asked to scan is a real problem,
   not scope creep.
6. **Any command that changes state.** This skill audits; it does not remediate. It never
   runs `git filter-repo`, never rotates a credential, never applies a dependency bump,
   never edits source. It recommends; you execute. The one thing worse than a leaked key is
   a leaked key plus a rewritten history nobody coordinated.
7. **Writing files anywhere other than the agreed output paths.**

## The log — decide, but show your work

Write `DECISIONS.md` alongside the report, using `assets/DECISIONS_template.md`.

**Threshold: log a decision when a reasonable reviewer might have made it differently.**
Not every action — every judgment. Expect 10–25 entries on a real audit; triage decisions
alone will account for most of them.

### What to log

- **Every triage call on scanner output.** Dismissing a semgrep hit as a false positive is
  a decision with consequences, and it's the one most likely to be wrong. Record the rule,
  the location, and why it was dismissed. This is the single most important category here.
- **Likelihood and impact ratings** — both axes, with the reasoning, per
  [risk-rating.md](risk-rating.md). Especially any Critical, and anything downgraded
  because of a compensating control.
- **Reachability conclusions** — "rated Medium because the vulnerable function isn't
  reachable from any route" is a decision that could be wrong and changes everything.
- **Inherited CVE adjustments** — where a published CVSS was not adopted, and why.
- **Secret triage** — classifying a hit as a placeholder, expired, or false positive. Getting
  this wrong in the dismissive direction is how breaches happen.
- **Exclusions** — anything noticed and not reported.
- **Assumptions about the application** that the interview didn't settle.

### Entry format

```markdown
### D-07 — Dismissed semgrep `dangerous-subprocess-use` at `scripts/build.py:22`

- **Decided:** not reported
- **Alternative:** report as A05 Injection, likely High
- **Because:** argument is a module-level constant, not attacker-reachable; script is
  build-time only and not deployed
- **Assumed:** `scripts/` is excluded from the runtime image
- **If that assumption is wrong:** this becomes command injection, High
- **Reverse it:** say "reinstate D-07" and I'll write it up as a finding
```

Note the extra field. In a security audit, a dismissal that rests on an assumption needs
the consequence of that assumption being wrong stated on its face — the reader may know
immediately that `scripts/` *does* ship, and that's exactly the correction the log exists
to invite.

### Mark them inline

Rated findings carry their decision IDs. Dismissed findings live in a **Dismissed** section
of the report, not only in the log — a dismissal buried in a separate file is close to a
silent one, and dismissals are where audits go wrong.

## When uncertain, don't quietly pick

Uncertainty in a security audit resolves toward reporting, not toward silence. If you can't
establish reachability, report the finding with reachability marked unknown and rate it
conservatively. Don't dismiss on an unverified assumption — log the question instead.

An over-reported finding costs someone ten minutes. An under-reported one can cost a breach.
The asymmetry should shape every close call.

## Present it

Lead the delivery with the counts: findings reported, findings dismissed, decisions logged.
Name the two or three dismissals most worth a second opinion — the ones resting on an
assumption you couldn't verify. Those are what the person is best placed to check and you
are least.
