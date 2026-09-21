# Audit Brief — [Application]

**Status:** ⏸ AWAITING APPROVAL
**Date:** [YYYY-MM-DD]

> No scanner runs and no finding is written until this brief is approved. This document is
> also the record of what was authorized, by whom, and when.

## What I found in recon

[Read-only observations only — stack, file count, git history depth, lockfiles, CI config,
which scanners are installed. No evaluation, no findings.]

## Threat context

**Application:** [what it does]
**Data held:** [PII / payment / health / credentials / nothing sensitive]
**Compliance regime:** [GDPR / HIPAA / PCI-DSS / SOC 2 / none]
**Exposure:** [internet-facing / internal / VPN-only]
**Auth model:** [public / authenticated / role-based]
**Tenancy:** [single-tenant / multi-tenant]

> Impact ratings derive from this section. If it's wrong, every severity in the report is wrong.

## Scope

**In scope:** [repos, directories, branches, commit SHA]
**Out of scope:** [excluded paths, vendored code, generated code, test fixtures]

## Authorized actions

Each of these needs explicit approval — check only what was granted:

- [ ] Static analysis (semgrep) on in-scope source
- [ ] Dependency CVE scan (trivy / osv-scanner / ecosystem audit)
- [ ] Secret scan, working tree only
- [ ] **Secret scan across full git history** — slow, reads every object
- [ ] **Network access** — CVE database lookups, `npm audit`
- [ ] Container image scan
- [ ] IaC / CI config review
- [ ] Manual authorization review of routes

**Not authorized:** [anything explicitly declined]

## Depth

**Level:** [dependency+secrets sweep / full scanner pass + triage / full audit with manual
authorization review]
**Estimated time:** [rough]
**Estimated findings:** [rough count]

## Prior context

**Previous audits:** [when, what was found]
**Accepted risks:** [known, consciously accepted — will not be re-reported as new]
**Compensating controls:** [WAF, segmentation, monitoring — these lower likelihood ratings]

## Deliverables

- [ ] `SECURITY_AUDIT.md` — findings, rated by OWASP Risk Rating
- [ ] `REMEDIATION_PLAN.md` — ordered work, rotation first

## Open questions

[Unresolved items that would change the approach.]

---

**To proceed:** approve this brief, or say what to change.

*Exception: a live credential found incidentally during recon is reported immediately,
without waiting for approval.*
