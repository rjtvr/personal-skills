# Security Audit — [Application]

**Date:** [YYYY-MM-DD]
**Scope:** [repos, branches, commit SHA, services covered]
**Threat context:** [what the app does, who uses it, what data it holds, internet-facing or not]
**Tools run:** [semgrep vX / gitleaks vX / trivy vX — and which were unavailable]
**Not covered:** [runtime testing, infrastructure, third-party services, etc.]

> A clean result for any tool means known patterns were not matched. It is not evidence
> that the application is secure.

---

## Immediate action required

[Live credentials and actively exploitable Criticals only. If none, write "None." Do not
bury an urgent item in the table below.]

---

## Summary

| Severity | Count |
|---|---|
| Critical | |
| High | |
| Medium | |
| Low | |
| Note | |

[3–5 sentences: overall posture, the dominant weakness class, the single change that
reduces the most risk.]

---

## Findings

### [SEC-01] [Short title]

| | |
|---|---|
| **Severity** | Critical |
| **Likelihood** | High — unauthenticated, internet-reachable, public tooling exists |
| **Impact** | High — full read access to all customer records |
| **OWASP** | A01:2025 Broken Access Control |
| **CWE** | CWE-639 Authorization Bypass Through User-Controlled Key |
| **Location** | `src/api/invoices.ts:42` |
| **Reachability** | Confirmed — `GET /api/invoices/:id` with any valid session |

**Description**
[What the weakness is, in terms of the application. Not a generic definition of the
vulnerability class.]

**Evidence**
[The actual code, config, or observed behavior. Quote the relevant lines. For secrets, use
location and fingerprint only — never the value.]

**Attack scenario**
[How an attacker reaches and uses this, at the level of detail a developer needs to confirm
it. The vulnerable request shape, not a weaponized payload.]

**Remediation**
[Concrete fix. Name the pattern or library. Reference an existing correct implementation in
the codebase where one exists — consistency with what's already there is more likely to be
adopted than a novel approach.]

**Verification**
[How to confirm the fix works — the test to write, the request to replay.]

---

## Unverified

[Suspected but not confirmed, with what would confirm each. Kept separate so the confirmed
findings stay trustworthy.]

## Systemic observations

[Patterns rather than instances. "Authorization is enforced per-handler with no shared
helper, so coverage depends on each author remembering" explains a dozen findings and is
more actionable than the dozen.]

## Positive controls

[What's done well. Not politeness — it tells the reader which existing patterns to copy
when fixing the rest, and prevents a fix from removing a control that was working.]
