# Secrets and git history

## The ordering people get wrong

When a live credential is found in a repository, the instinct is to remove it from git
history first. That's the wrong order, and the mistake is costly.

**Rotate first. Scrub second. Scrubbing is cleanup, not remediation.**

The credential was exposed the moment it was pushed. Anyone with repo access — every
current and former collaborator, every CI job, every fork, every clone, every cached copy
on a laptop or a build server — has had it. Rewriting history removes it from the canonical
repo; it does not un-disclose it. Until the credential is rotated, it is compromised, and
if the repository was ever public, assume automated scrapers found it within minutes.

The full sequence:

1. **Rotate the credential.** Issue a new one, deploy it, revoke the old one.
2. **Check for abuse.** Review access logs for the exposure window — from the commit date,
   not the discovery date. This step gets skipped and it's the one that finds the breach.
3. **Scrub history**, if the repo is shared or public: `git filter-repo` (preferred) or BFG
   Repo-Cleaner. This rewrites hashes, so every collaborator must re-clone. Coordinate it.
4. **Prevent recurrence.** Pre-commit hook with gitleaks, move the value to a secrets
   manager or environment variable, add the pattern to CI.

For a private repo with a small, trusted, unchanged collaborator set, rotating and deleting
forward is often a reasonable call — the history rewrite is disruptive and buys little. Say
so rather than reflexively recommending a rewrite. State the tradeoff and let the person
decide.

## Never print the secret

A security report containing the credential it found is a new copy of the leak, in a file
that will be pasted into chat, committed, and emailed.

Reference secrets by **location and fingerprint**:

```
AWS access key — src/config/prod.js:14, introduced in a1b2c3d (2024-03-12)
fingerprint: AKIA…7f2c (20 chars, sha256:9e4a1b…)
```

Enough for the owner to identify which credential it is. Not enough to use it.
`scripts/normalize_findings.py` applies this redaction automatically to gitleaks output.

## Where to look beyond the obvious

Scanners cover the common paths. These get missed:

- **Git history**, including deleted files, and **branches that were never merged**.
- `.env` files committed early in a project's life, before the `.gitignore` was added.
- CI/CD config — secrets inline in workflow YAML rather than referenced from a store.
- Build artifacts and Docker layers. A secret used in an intermediate layer persists in the
  image even if a later layer deletes the file. `docker history` and `trivy image` find these.
- Client bundles and source maps — API keys that were meant for server-side use.
- Test fixtures with real credentials against a real staging environment.
- Log output, error tracking payloads, and analytics events carrying tokens.
- Config committed to the repo for local convenience: database URLs with embedded passwords,
  internal hostnames, service account JSON.

## Triaging a hit

Before escalating, establish which of three cases applies:

- **Live credential.** Rotate immediately, out of band, before finishing the audit. This is
  the one finding that shouldn't wait for the report.
- **Expired, revoked, or placeholder.** Still worth a low-severity finding, since the
  practice will recur. Don't treat it as an incident.
- **False positive.** High-entropy string that isn't a credential — a hash, UUID, lockfile
  integrity value, minified filename. Verify by shape and location, and drop it silently
  rather than reporting it as "probably fine".

The failure mode in both directions is real: reporting UUIDs as leaked keys destroys trust
in the report, and dismissing a live key as a test fixture is how breaches happen. When
uncertain, ask the owner whether the value is live rather than guessing.
