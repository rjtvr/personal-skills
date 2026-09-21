# Entry template

## File-level frontmatter — written once when the file is created

```yaml
---
date: 2026-09-08
repo: my-api
account: work
tasks:
  - PAY-412 partial refunds
---
```

Append to `tasks` on each subsequent run against the same file.

`account` appears only when `accountLabels` is configured and the account resolved. Omit
the field rather than writing a guessed value. It gives a greppable index
of what a day and repo covered without reading the bodies.

## Session section — appended on every run

```markdown
## 14:32 — PAY-412 partial refunds

`feature/PAY-412-refunds` · in-progress

### Summary
Added partial refund support to the payments service. Refunds now accept an
amount rather than assuming the full charge.

### Changes
- `src/payments/refund.ts` — new `createPartialRefund()`; validates amount
  against remaining refundable balance
- `src/payments/schema.ts` — added `amount_cents` to the refund request schema
- `migrations/0042_refund_amount.sql` — nullable column, backfilled to charge total
- Commits: `a1b2c3d`, `e4f5g6h`
- PR: https://github.com/acme/my-api/pull/318

### Next steps
- Idempotency key handling is not done — a retried request creates a second refund
- Needs a decision on whether partial refunds are allowed after a chargeback

### Notes
Chose a nullable column with a backfill rather than a default, so existing rows
stay distinguishable from genuine full-amount refunds. Stripe caps partial refunds
at the original charge minus prior refunds; we mirror that server-side rather than
trusting the client value.
```

## Rules

**Status** is `complete`, `in-progress`, or `blocked`. It sits on the section rather than in
file frontmatter, because it varies between sessions in the same file.

**Summary** — two or three sentences covering what changed and why. Not "worked on refunds."

**Changes** — file paths with a short note on what each one does. Short-form commit hashes.
Links only when they can be constructed from real evidence.

**Next steps** — real remaining work. Omit the section entirely rather than writing "none".

**Notes** — genuinely optional. Include it for a technical decision, a discovery, or a
problem hit. This is the section future-you cannot reconstruct from the diff, which is
exactly why it shouldn't be padded with things that can be.

**Time** in the heading is local 24-hour, so multiple sessions in a day sort naturally.

## What this is not

Not a transcript, and not a changelog — git already has that. It should be readable in
thirty seconds and answer "what was I doing, and what was I about to do next?"
