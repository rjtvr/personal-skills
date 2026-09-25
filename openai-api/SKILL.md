---
name: openai-api
description: Reference for the OpenAI API — model ids and pricing (GPT-6, GPT-5.x, o-series reasoning models), the Responses API, function/tool calling, streaming, prompt caching, structured outputs, and migrating off Chat Completions or the sunset Assistants API. Use whenever the user names OpenAI, GPT, ChatGPT API, o1/o3/o4-mini, Codex, "Responses API", or "Assistants API"; asks about OpenAI model choice, pricing, rate limits, or caching; or the task is LLM-shaped (agent, tool-calling, RAG, LLM-as-judge, summarize/extract/classify/rewrite/converse) and OpenAI is the stated or evident provider (an `openai` SDK import, `OPENAI_API_KEY`, or a `gpt-*` / `o*-mini` model string in the code). Skip when the user is working with Claude/Anthropic, Gemini, Llama, Mistral, Cohere, or another named provider instead.
---

# OpenAI API

Reference material for building against the OpenAI API — model selection, pricing, the
Responses API, tool calling, streaming, and caching.

## Before quoting a price or model id

Model lineups and prices change often — [references/models-and-pricing.md](references/models-and-pricing.md)
is a snapshot taken 2026-09-25. Treat it as a starting point, not ground truth: if the answer
matters (the user is about to commit to a model in code, or asks "what does X cost"), verify
against https://developers.openai.com/api/docs/pricing with WebFetch before answering, the
same way you would for a Claude/Anthropic pricing question.

## Reference files

- [references/models-and-pricing.md](references/models-and-pricing.md) — model families
  (flagship, reasoning/o-series, mini, nano), per-million-token pricing, cached-input and
  batch discounts.
- [references/responses-api.md](references/responses-api.md) — the Responses API's shape,
  how it differs from Chat Completions, and conversation-state options.
- [references/function-calling-and-tools.md](references/function-calling-and-tools.md) —
  defining tools, strict mode, parallel calls, returning results, remote MCP servers.
- [references/streaming.md](references/streaming.md) — enabling streaming, the typed SSE
  event lifecycle, and moderation implications.
- [references/prompt-caching.md](references/prompt-caching.md) — automatic prefix caching,
  minimum prefix length, and what counts as cacheable content.
- [references/migration.md](references/migration.md) — moving from Chat Completions to
  Responses, and off the Assistants API (sunset 2026-08-26).

## Model choice, at a glance

- **Cheapest / highest-volume**: a nano or `luna`-tier model — classification, extraction,
  short rewrites.
- **General-purpose default**: a mid-tier GPT-5.x/6 model (`terra`/`sol`-class) — most
  agent and chat work.
- **Hard reasoning, math, multi-step planning**: an o-series model (`o3`, `o4-mini`) or a
  `-pro` variant, at a steep cost premium — reserve for tasks that actually need it.
- **Cost-insensitive batch/offline jobs**: any model via the Batch API for a 50% discount,
  if a 24-hour turnaround is acceptable.

Recommend a tier based on what the task needs, not the newest model by default — the price
gap between nano and a `-pro` reasoning model is two to three orders of magnitude.
