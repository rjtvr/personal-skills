# OWASP Top 10:2025

The current edition, announced November 2025 and finalized January 2026 — the first
revision since 2021. Next revision expected around 2028–2029, so this is the working
baseline.

**If you have a checklist predating 2025, it's wrong in two structural ways:** Software
Supply Chain Failures is a new category at A03, and SSRF is no longer standalone — it was
folded into A01 Broken Access Control (CWE-918).

| | Category | Was in 2021 |
|---|---|---|
| A01 | Broken Access Control | A01 — now absorbs SSRF |
| A02 | Security Misconfiguration | A05, up three |
| A03 | Software Supply Chain Failures | **new**, expands A06 Vulnerable and Outdated Components |
| A04 | Cryptographic Failures | A02, down two |
| A05 | Injection | A03, down two |
| A06 | Insecure Design | A04, down two |
| A07 | Authentication Failures | A07, renamed |
| A08 | Software and Data Integrity Failures | A08 |
| A09 | Security Logging and Alerting Failures | A09, renamed — alerting, not just monitoring |
| A10 | Mishandling of Exceptional Conditions | **new** |

---

## A01 — Broken Access Control

Top of the list for four consecutive editions, and the category scanners are worst at.
Now explicitly covers API authorization failures (BOLA/BFLA) and SSRF.

- **Object-level authorization (BOLA/IDOR).** Every endpoint taking an ID from the request:
  is ownership checked, or only authentication? `GET /api/orders/:id` that verifies a valid
  session but not that the order belongs to the session's user is the archetype.
- **Function-level authorization (BFLA).** Admin-only actions reachable by a normal user
  who guesses the route. Check that authorization is enforced server-side, not by hiding
  the UI button.
- **Enforcement location.** Authorization decided in the client, in middleware that's easy
  to bypass, or duplicated per-route (which means one route will miss it).
- **Mass assignment.** Request bodies bound directly to models, letting a user set
  `role: admin` or `isVerified: true`.
- **SSRF (CWE-918).** User-controlled URLs fetched server-side. Check for allowlists, and
  for blocks on internal ranges and cloud metadata endpoints (`169.254.169.254`).
- **CORS.** `Access-Control-Allow-Origin` reflecting the request origin, or `*` alongside
  credentials.
- Path traversal in file access; forced browsing to authenticated pages.

## A02 — Security Misconfiguration

Rose from #5 to #2 — continuous deployment without continuous review opens exposure windows.

- Default credentials, sample apps, admin consoles reachable in production.
- Debug mode, stack traces, or verbose errors exposed to users (see also A10).
- Missing security headers: CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`.
- Overly permissive cloud storage, database bound to `0.0.0.0`, management ports open.
- Directory listing on; source maps and `.git` served in production.
- Unnecessary features, ports, services, and accounts enabled.

## A03 — Software Supply Chain Failures (new)

Expands beyond vulnerable dependencies to the whole ecosystem — dependencies, build
systems, distribution. Fewest occurrences in test data but the highest average exploit and
impact scores, which is exactly the profile that makes it dangerous.

- Direct and transitive dependencies with known CVEs.
- Unpinned versions, missing lockfiles, floating tags in container images.
- Build pipeline integrity: who can modify CI config, are secrets scoped, are third-party
  actions pinned to a commit SHA rather than a mutable tag.
- Typosquatting and dependency confusion — internal package names resolvable from a public
  registry.
- Install-time scripts (`postinstall`) from untrusted packages.
- Unverified artifacts; no SBOM; no provenance.

## A04 — Cryptographic Failures

- Sensitive data transmitted or stored in cleartext; missing TLS enforcement.
- Weak or misused algorithms: MD5/SHA1 for security purposes, ECB mode, static IVs.
- Passwords stored with fast hashes. Use bcrypt, scrypt, or Argon2 — a general-purpose
  hash is a defect even when salted.
- Hardcoded keys, keys committed to the repo, keys never rotated.
- Weak randomness for tokens and IDs (`Math.random()`, unseeded PRNGs) where a CSPRNG is
  required.
- Certificate validation disabled — a very common "fix" for a local dev error that ships.

## A05 — Injection

Dropped two places but still fundamental. Note that XSS lives here.

- SQL/NoSQL: string-concatenated queries. Parameterized queries or an ORM's binding are
  the fix; escaping is not.
- Command injection: user input reaching `exec`, `system`, `subprocess` with `shell=True`.
- XSS: reflected, stored, and DOM-based. Check `innerHTML`, `dangerouslySetInnerHTML`,
  Angular `bypassSecurityTrust*`, and template auto-escaping being disabled.
- LDAP, XPath, template injection (SSTI), header injection.
- ORM escape hatches — raw query methods that bypass the safety the ORM otherwise gives.

## A06 — Insecure Design

Flaws in what was designed, not how it was built. A perfect implementation of a flawed
design is still vulnerable — these can't be patched, only redesigned.

- Missing rate limiting on authentication, password reset, OTP, and expensive endpoints.
- Business logic that trusts client-supplied values: price, quantity, discount, user ID.
- Race conditions in balance checks, coupon redemption, inventory (TOCTOU).
- Recovery flows weaker than the login they protect.
- No tenant isolation model in a multi-tenant system.

## A07 — Authentication Failures

Renamed for precision.

- Credential stuffing possible: no rate limiting, no lockout, no breach-password check.
- Session tokens: predictable, not rotated on privilege change, not invalidated on logout,
  excessive lifetime.
- Cookies missing `HttpOnly`, `Secure`, or a sane `SameSite`.
- JWT: `alg: none` accepted, algorithm confusion (HS256 verified with an RSA public key),
  signature unverified, expiry unchecked, sensitive claims trusted from the client.
- Weak or absent MFA on privileged accounts; MFA bypassable via a recovery path.
- User enumeration through differing responses or timing on login and reset.

## A08 — Software and Data Integrity Failures

- Deserialization of untrusted data — Java, Python `pickle`, PHP `unserialize`, .NET.
- Auto-update or plugin mechanisms without signature verification.
- CI/CD that deploys unreviewed code, or lets a PR from a fork access secrets.
- CDN-loaded scripts without Subresource Integrity.

## A09 — Security Logging and Alerting Failures

Renamed to emphasize *alerting* — logs nobody acts on are not a control.

- Auth failures, access-control denials, and high-value actions not logged.
- Logs with no alerting path, or alerts nobody owns.
- Insufficient detail to reconstruct an incident; no correlation ID.
- **Logs containing what they shouldn't**: passwords, tokens, full PII, card data. This is
  itself a finding, and often a compliance one.
- Logs mutable by the application, or not retained long enough to investigate.

## A10 — Mishandling of Exceptional Conditions (new)

Covers failing to prevent, detect, or respond to abnormal conditions.

- **Failing open**: an auth check that returns "allowed" when the auth service is
  unreachable, or a `catch` that swallows a permission error and continues.
- Errors exposing stack traces, SQL, file paths, or library versions to the user.
- Unhandled promise rejections and unchecked error returns leaving inconsistent state.
- Resource exhaustion: unbounded uploads, unpaginated queries, no timeouts, ReDoS.
- Partial failure in multi-step operations with no rollback — money moved, record not written.
- Empty `catch` blocks. Grep for them directly; they're where failures go to hide.
