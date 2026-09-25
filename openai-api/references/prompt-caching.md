# Prompt caching

Automatic on OpenAI's side — there's no cache-control parameter to set, unlike Anthropic's
explicit cache breakpoints. When a request's prefix matches something OpenAI recently
processed, it can route to a server that already has that prefix computed.

## What triggers a cache hit

- The prefix must be **longer than 1,024 tokens**.
- Cache hits happen in **128-token increments** — the matching prefix has to align to that
  granularity, not just share the same leading text.
- The prefix has to be **exact, repeated content**: system/developer instructions, tool
  definitions, and structured-output schemas held constant across calls are what make this
  work. Anything that varies per-request (the live user message, injected timestamps) should
  come *after* the stable prefix, not interleaved with it.

## What's cacheable

The entire request prefix: message arrays (system, user, assistant turns), both URL-linked
and base64-encoded images in user messages, the tools list, and structured-output schemas
(a schema acts as a prefix to the system message).

## Payoff

Up to ~80% lower time-to-first-token and ~90% lower cost on the cached portion of input
tokens (see per-model cached-input pricing in
[models-and-pricing.md](models-and-pricing.md) — routinely ~10% of standard input price).

## Streaming interaction

Caching and streaming are independent — caching only affects how fast the *first* token
comes back; once generation starts, streaming behaves the same whether or not the prefix was
cached.

## Practical implication for prompt design

Put everything stable (system instructions, tool schemas, few-shot examples) first, and
anything that changes per-call last. A prompt that interleaves stable and variable content
throughout defeats caching even if the total token overlap across calls is high.
