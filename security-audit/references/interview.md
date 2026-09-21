# Interview protocol

No scanner runs and no finding is written until the brief is approved. This file is the
question set.

## Principle: never ask what you can observe

Read-only recon first — identify the stack, count source files, check which scanners are
installed, note how much git history exists, look for lockfiles and CI config. Then ask
only what recon can't answer.

Recon means listing and reading. It does not mean scanning, and it produces no findings.
Running `semgrep` "just to see" is starting the audit.

## The questions

Ask in this order, grouped two or three per turn. Use `AskUserQuestion` where available.
**Skip anything recon settled** and state what you found instead.

**1. What is this application, and what does it hold?**

The single most important question, and the one that can't be inferred from code. User PII,
payment data, health records, credentials, or nothing sensitive — this determines impact
ratings for every finding in the audit. Ask whether any compliance regime applies (GDPR,
HIPAA, PCI-DSS, SOC 2). Without this answer, risk ratings are guesses dressed as analysis.

**2. Exposure and authentication model**

Internet-facing or internal? Authenticated users only, or public endpoints? Single-tenant
or multi-tenant? Multi-tenancy in particular changes where the review concentrates, because
tenant isolation failures are usually the highest-impact class present.

**3. Scope**

Which repos, directories, and branches. What's explicitly out of scope. Whether generated
code, vendored dependencies, and test fixtures should be included — usually not, and they
generate most of the false-positive volume when they are.

**4. Permission to run tools** — ask each separately, don't bundle:

- Which scanners may run (name the ones recon found installed).
- **Full git-history scanning?** Slow on large histories, and it reads every object.
- **Network access?** CVE database lookups and `npm audit` leave the machine. Flag this
  explicitly — the code may be under an agreement that restricts it.

**5. Depth**

Options worth offering: dependency and secret sweep only (fast, mechanical); full scanner
pass plus triage; or full audit including manual authorization review of every route. Give
a rough time and finding-count estimate for each. The manual authorization review is where
the real findings are and also where the time goes — make that tradeoff visible rather than
deciding it for them.

**6. Prior context**

Previous audit findings, already-accepted risks, known issues, compensating controls like a
WAF or network segmentation. Re-reporting a consciously accepted risk as a new Critical
wastes their time and costs the report credibility.

## Locking the brief

Write `AUDIT_BRIEF.md` from `assets/AUDIT_BRIEF_template.md`, show it, and stop.

The brief is a contract. For a security audit it's also the record of what was authorized —
which tools ran, against what, with whose approval. That matters if anyone asks later.

Ask for explicit approval. **Anything short of clear approval is a revision**, not a yes.
Do not run a scanner in the same turn that produces the brief.

## The one exception

If read-only recon incidentally surfaces what appears to be a **live credential** — a key
visible in a file you listed — report it immediately, before the brief, before approval.

Every hour a valid credential stays live is exposure, and a process gate is the wrong thing
to be observing at that moment. Report the location and a redacted fingerprint, never the
value, and recommend rotation first. Then return to the interview.

This exception covers live credentials only. It is not a general license to surface findings
early, and it does not extend to running a secret scanner before approval — it applies to
what you happened to see while looking at file structure.

## Once approved

The brief defines what was authorized. Don't scan outside it. If something outside scope
looks serious, name it and ask rather than expanding on your own judgment — in a security
context, scanning a system you weren't asked to scan is a real problem, not just scope creep.
