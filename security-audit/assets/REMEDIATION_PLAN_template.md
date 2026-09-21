# Remediation Plan — [Application]

Generated from `SECURITY_AUDIT.md`. Finding IDs (`SEC-01`) reference that file.

**Ordering is not purely by severity.** Credential rotation comes first regardless of
rating, because exposure continues every hour the credential stays valid. After that,
order by risk, grouping changes that touch the same authorization or validation layer so
one review covers them.

---

## Phase 0 — Out of band, before anything else

Do these now. They don't wait for a branch or a review cycle.

- [ ] **Rotate** [credential, `SEC-0X`] — issue new, deploy, revoke old
- [ ] **Review access logs** for the exposure window, starting from the commit date rather
      than the discovery date
- [ ] [Disable the affected endpoint / add a temporary block, if a Critical is live]

---

## Phase 1 — Critical

### Task 1.1 — [Fix]

- **Closes:** SEC-01, SEC-04
- **Files:** `src/api/invoices.ts`, `src/middleware/authorize.ts`
- **Change:** [Specific. Where the check goes, what it compares, which existing helper to
  reuse.]
- **Do not:** [The plausible wrong fix. E.g. "do not filter in the response serializer —
  the record is still fetched, and other callers bypass the serializer."]
- **Verify:** [Test to write, plus the manual request that should now return 403]
- **Risk:** [What might break. Shared authorization code is high blast radius.]

---

## Phase 2 — High

## Phase 3 — Medium and below

[Group these. Many Mediums share a root cause and one fix.]

---

## Structural changes

Fixes that prevent the class rather than the instance. Usually the highest-value work in
the plan, and usually deferred because no single finding demands it:

- [ ] Centralize authorization in a helper every handler must call, so omission is visible
      in review rather than invisible
- [ ] Add gitleaks as a pre-commit hook and a CI gate
- [ ] Add semgrep to CI, failing on High and above
- [ ] Add dependency scanning to CI with an update cadence
- [ ] Add authorization test cases to the suite: for each protected route, assert that a
      non-owner receives 403

---

## Verification for the whole plan

- [ ] All scanners re-run clean, or every remaining finding is triaged with a reason
- [ ] Authorization tests pass for each fixed endpoint
- [ ] Rotated credentials confirmed working; old credentials confirmed revoked
- [ ] No secret values appear in this plan, the audit, or the commits produced from them

---

## Accepted risk

[Findings not being fixed, with the reason and who accepted it. Explicit acceptance is a
legitimate outcome; silent omission is not.]

## Open questions

[Decisions needed before a task can proceed — surface early rather than guessing.]
