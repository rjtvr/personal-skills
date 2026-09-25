# Responses API

OpenAI's current recommended interface for generating model output. It unifies what used to
be split across Chat Completions and the (now-sunset) Assistants API — see
[migration.md](migration.md).

**Default to it for new work.** Chat Completions still works and stays supported, but
OpenAI's own migration guidance cites a ~3% SWE-bench improvement and 40–80% better cache
utilization on equivalent prompts, plus native support for hosted tools (web search, file
search, code interpreter) and custom functions in a single request.

## Shape, vs. Chat Completions

| Aspect | Chat Completions | Responses |
|---|---|---|
| Input | `messages` array | `input` (string or item list) + separate `instructions` |
| Output | `choices[0].message.content` | typed `output` array of distinct item types |
| Conversation state | you resend the whole transcript | `previous_response_id`, or `store: true` to let OpenAI hold it server-side |
| Structured outputs | `response_format` | `text.format` |
| Function/tool defs | externally tagged | internally tagged, strict mode on by default |
| Streaming | delta-based chunks | typed server-sent events (see [streaming.md](streaming.md)) |

## Conversation state

Two ways to carry a multi-turn conversation instead of re-sending the whole transcript on
every call:

- **`previous_response_id`** — point the next call at the id of the prior response; OpenAI
  reconstructs context server-side.
- **`store: true`** — let OpenAI persist the response so it can be referenced later.

For **Zero Data Retention** requirements, Responses can run statelessly — set `store: false`
and use encrypted reasoning items to preserve reasoning-model performance without server-side
storage.

## When Chat Completions is still the right call

Existing code already built on Chat Completions that isn't touching agentic/tool-heavy
workflows has no urgent reason to migrate. New projects, and anything that needs hosted
tools or multi-step agent behavior, should start on Responses directly rather than migrate
later.
