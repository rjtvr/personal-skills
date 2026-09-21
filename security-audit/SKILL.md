---
name: security-audit
description: Audit a codebase for security vulnerabilities against the OWASP Top 10:2025, scan for leaked secrets in code and git history, check dependencies for known CVEs, and review configs and CI/CD for misconfiguration. Runs available scanners first, then reasons about what scanners structurally cannot find, and ranks findings by OWASP Risk Rating. Use whenever the user asks for a security review, security audit, vulnerability assessment, OWASP check, penetration-test-style review of their own code, secret scanning, dependency or CVE check, "is this code safe", "check for injection", "review auth before launch", or hands over a repo, config, or diff and asks about security risk. This skill is strictly defensive: it finds and fixes weaknesses in code the user owns. Do not use it to develop exploits, attack tooling, or techniques for compromising systems the user does not control.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/normalize_findings.py *)
---

# Security Audit

Find real, exploitable weaknesses in a codebase the user owns, rank them by actual risk,
and produce remediation work someone can execute.

## Scope boundary

This skill is defensive. It identifies vulnerabilities and describes how to fix them.

It does not produce working exploits, attack tooling, or techniques for compromising
systems the user doesn't own. When a finding needs a proof of concept, include only enough
to demonstrate that the path is reachable — the vulnerable request shape, not a weaponized
payload. That's sufficient for a developer to confirm and fix, and it's where the line sits.

If a request shifts from "find weaknesses in my code" toward "help me attack this target",
stop and say so plainly. The vocabulary overlaps almost completely; the intent doesn't.

## Workflow

0. **Interview and lock the brief** — nothing runs before approval
1. **Run authorized scanners** — see [references/scanners.md](references/scanners.md)
2. **Reason over the gaps** — see [references/reasoning-gaps.md](references/reasoning-gaps.md)
3. **Rate each finding** — see [references/risk-rating.md](references/risk-rating.md)
4. **Write the report and remediation plan**
5. **Log the judgment calls** — `DECISIONS.md`, see `references/decisions.md`

Threat context is gathered in step 0 and is not optional. "SQL injection in the admin export
endpoint" is Critical in a health records system and Medium in a local dev tool, and the
same finding text without that context is unrankable.

## Step 0 — Interview, then lock the brief

**This is a gate, not a preamble.** No scanner runs and no finding is written until the
person approves a written brief.

1. **Read-only recon.** Stack, file count, git history depth, lockfiles, CI config, which
   scanners are installed. Listing and reading only — running a scanner "just to see" is
   starting the audit.
2. **Interview.** Follow `references/interview.md`. The question that matters most is what
   data the application holds, because impact ratings derive from it and nothing in the
   code can tell you.
3. **Write `AUDIT_BRIEF.md`** from `assets/AUDIT_BRIEF_template.md`, including the
   authorized-actions checklist. Show it. **Stop.**
4. **Wait for explicit approval.** Do not run a scanner in the same turn that produces the
   brief.

Three actions need their own approval rather than being folded into a general yes: **full
git-history scanning** (slow, reads every object), **network access** (CVE lookups leave
the machine, which may breach an agreement covering the code), and **container image
scanning**.

The brief doubles as the record of what was authorized, against what, and when. In a
security context that record matters later.

**The one exception:** if recon incidentally surfaces what looks like a live credential,
report it immediately — before the brief, before approval — with location and redacted
fingerprint, never the value. Every hour a valid credential stays live is exposure. This
covers what you happened to see while reading file structure; it is not license to run a
secret scanner early.

Skip the interview only when scope, depth, and permissions are all already specified.

## Step 1 — Scanners first

Scanners are cheap, fast, and catch the patterns that are objectively detectable. Run what's
available rather than reasoning your way to conclusions a tool would settle in seconds.

Typical set: **semgrep** (code patterns), **gitleaks** (secrets, including git history),
**trivy** or **osv-scanner** (dependency CVEs), plus the ecosystem's own audit command
(`npm audit`, `pip-audit`, `govulncheck`, `bundle audit`).

[references/scanners.md](references/scanners.md) has invocations, what each tool is
actually good at, and the false-positive patterns worth knowing before you report anything.

`scripts/normalize_findings.py` merges scanner JSON into one deduplicated list and
**redacts secret values** so they never land in a report:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/normalize_findings.py \
  --semgrep semgrep.json --gitleaks gitleaks.json --trivy trivy.json
```

Two rules about scanner output. **Triage before reporting** — raw SAST output has a high
false-positive rate, and a report padded with unverified tool output is worse than no
report, because it trains the reader to ignore all of it. **A clean scan is not a secure
application** — say so explicitly rather than implying safety you haven't established.

## Step 2 — Reason over the gaps

This is where the audit earns its keep. Scanners match patterns; the most damaging web
vulnerabilities are absent logic, and absent code has no pattern to match.

Broken access control is the clearest case, and it has been the #1 OWASP category for four
consecutive editions. To a pattern matcher, an endpoint that fetches a record by ID and
returns it looks identical whether or not it checks that the requester owns that record.
Only reading the code with the question "who is allowed to do this, and where is that
enforced?" finds it.

Work through [references/owasp-top10-2025.md](references/owasp-top10-2025.md) category by
category, and [references/reasoning-gaps.md](references/reasoning-gaps.md) for the specific
classes scanners miss. For secrets, [references/secrets-and-history.md](references/secrets-and-history.md)
covers history scanning and — more importantly — the remediation ordering people get wrong.

## Step 3 — Rate by OWASP Risk Rating

Risk = Likelihood × Impact, each rated Low / Medium / High, combined via the matrix in
[references/risk-rating.md](references/risk-rating.md) to give Note / Low / Medium / High /
Critical.

Score the two axes independently and write down the reasoning for each. The discipline
matters more than the arithmetic: it forces the question "how hard is this actually to
exploit, and what happens if someone does" instead of defaulting to the scanner's severity
label, which knows nothing about the application.

Two habits to hold:

- **Reachability gates everything.** A vulnerable function nobody can call is not a
  vulnerability, it's a latent one. Trace from an attacker-reachable entry point before
  rating anything High. If you can't establish reachability, say so and rate accordingly.
- **Don't inherit CVE scores blindly.** A CVSS 9.8 in a transitive dependency whose
  affected code path your app never invokes is not a 9.8 for you. Note the base score,
  rate your own exposure separately.

## Step 4 — Write the artifacts

**`SECURITY_AUDIT.md`** — findings, using [assets/SECURITY_AUDIT_template.md](assets/SECURITY_AUDIT_template.md).
Every finding carries: location, evidence, OWASP category, CWE ID, likelihood and impact
with reasoning, and remediation. Findings you suspect but can't confirm go in a separate
section marked unverified — never mixed in with confirmed ones.

**`REMEDIATION_PLAN.md`** — ordered work, using [assets/REMEDIATION_PLAN_template.md](assets/REMEDIATION_PLAN_template.md).
Ordering here is not by severity alone. Leaked credentials get rotated first regardless of
rating, because every hour they remain valid is exposure. After that, order by risk, and
group changes that touch the same auth or validation layer.

Never put a live secret value in either artifact. Reference it by location and by a redacted
fingerprint. A security report that leaks the credentials it found is a new incident.

## Decision discipline

Judgment calls get **logged**; a fixed list of actions gets **gated**. The gate list is
longer here than in a UX review because these actions have consequences outside the report.
Full protocol in `references/decisions.md`.

**Gates — never self-authorize:** starting without an approved brief; running any scanner
not ticked in the brief; full git-history scanning; network access; scanning outside scope;
**any command that changes state**; writing outside the agreed output paths.

That sixth one is absolute. This skill audits, it does not remediate. It never runs
`git filter-repo`, never rotates a credential, never bumps a dependency, never edits source.
It recommends; the person executes. The only thing worse than a leaked key is a leaked key
plus an uncoordinated history rewrite.

**Log — decide, but show your work.** Write `DECISIONS.md` from
`assets/DECISIONS_template.md`. The most important category is **triage**: every scanner hit
dismissed as a false positive is a decision with consequences and the one most likely to be
wrong. Record the rule, the location, the reasoning, and — on any dismissal — what happens
if the assumption behind it is wrong.

Dismissed findings also appear in a **Dismissed** section of the report itself, not only in
the log. A dismissal buried in a separate file is close to a silent one, and dismissals are
where audits go wrong.

Uncertainty resolves toward reporting. An over-reported finding costs ten minutes; an
under-reported one can cost a breach.

## Working with the person

Security findings land differently from other code review. Two things to hold:

- **Don't inflate.** Reporting everything at Critical destroys the signal that makes the
  real Critical actionable. Most findings are Medium. That's a normal, healthy result.
- **Don't moralize.** The code has vulnerabilities because all code does. State the finding
  and the fix without commentary about how it got there.

If the scan surfaces a live leaked credential or an actively exploitable Critical, say that
first and separately, before the rest of the report. It shouldn't be item 14 in a list.
