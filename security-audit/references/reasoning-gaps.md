# Reasoning over the gaps

What's left after the scanners run. These classes share one property: they're defined by
missing or wrong logic rather than by a dangerous call, so there's no pattern to match.

Work from entry points inward. Enumerate every route, handler, message consumer, and
scheduled job, then ask the questions below of each.

## Access control — the highest-yield pass

For every endpoint that takes an identifier, ask two separate questions. Conflating them is
the single most common security defect in application code:

1. **Is the caller authenticated?** — usually handled by middleware, usually fine.
2. **Is this specific caller allowed to act on this specific object?** — usually per-handler,
   usually missing somewhere.

```
GET /api/invoices/:id
  → session valid?          ✓ middleware
  → invoice.ownerId == session.userId?   ← if absent, that's the finding
```

Build a matrix: routes down one axis, roles across the other. Fill in where enforcement
happens for each cell. Empty cells are findings. This is tedious and it's where the real
vulnerabilities are.

Also check:

- **Enforcement consistency.** If 19 handlers check ownership and one doesn't, the one is
  the vulnerability. Route lists and middleware registration order are worth reading in full.
- **Indirect access paths.** The list endpoint filters by owner correctly, but the export,
  the search, the webhook, or the GraphQL resolver for the same data doesn't.
- **Nested resources.** `/orgs/:orgId/projects/:projectId` — is `projectId` verified to
  belong to `orgId`, or only that the user belongs to the org?
- **Mass assignment.** Follow request bodies into model constructors and `update()` calls.
  Look for allowlists; their absence is the finding.

## Business logic

No tool knows your rules, so derive them from the code and test them adversarially:

- **Client-trusted values.** Price, quantity, discount, currency, role, or user ID accepted
  from the request and used without server-side revalidation.
- **Sequence assumptions.** Can step 3 be called without steps 1 and 2? Multi-step flows
  usually assume order that nothing enforces.
- **Negative and boundary values.** Negative quantity refunding money. Integer overflow.
  Zero-value edge cases.
- **Race conditions.** Check-then-act on balances, coupons, inventory, or rate limits.
  Concurrent requests between the read and the write is the whole attack. Look for
  transactions and row locks; note their absence.
- **Idempotency.** Can a payment or a state transition be replayed?

## Trust boundaries

Draw them explicitly, then check each crossing:

- Client → server, service → service, app → database, app → third-party.
- Data validated at the boundary or deep inside (or twice, inconsistently)?
- Internal services that trust a header like `X-User-Id` — is that header stripped at the
  edge, or can a client set it?
- Webhooks: is the signature verified, is replay prevented?

## Multi-tenancy

If the system is multi-tenant, this is the highest-impact class in the whole audit:

- Is the tenant identifier derived from the session, or accepted from the request?
- Is every query scoped by tenant, or does it rely on the developer remembering?
- Shared caches keyed without the tenant ID — a cross-tenant leak with no code change
  visible at the vulnerable site.
- Background jobs and admin tooling that run without tenant scoping.

## Authentication flows

Read the whole flow, not just the login handler:

- Password reset: token entropy, expiry, single-use, bound to the requesting user, and
  invalidating existing sessions on completion.
- Email or phone change: does it require the current password? Does it notify the old address?
- OAuth: `state` parameter validated (CSRF), redirect URI allowlisted exactly, tokens not
  logged.
- Session invalidation on password change, on role change, on logout.
- Is recovery weaker than login? Attackers use the weakest path.

## Data exposure

- API responses returning whole model objects — password hashes, internal flags, other
  users' data nested in an include.
- GraphQL: introspection in production, missing depth and complexity limits, resolvers that
  each re-fetch without authorization.
- Error messages differing between "user not found" and "wrong password" (enumeration).
- Verbose responses in production; source maps served; internal endpoints in client bundles.

## Practical method

Pick the two or three most sensitive operations the app performs — the ones where a
compromise actually costs something — and trace each end to end: entry point, authorization,
validation, data access, response, logging. Full-breadth review that never goes deep finds
less than depth on what matters.
