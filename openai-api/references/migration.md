# Migration notes

## Chat Completions → Responses

Chat Completions remains supported — this isn't a forced migration for existing code that
isn't touching agentic or tool-heavy workflows. But **Responses is what OpenAI recommends for
all new projects**, per their own guidance, citing:

- ~3% SWE-bench improvement at equivalent prompt/setup
- 40–80% better cache utilization
- native multi-tool agentic requests (web search, file search, code interpreter, custom
  functions, all in one call) instead of manual orchestration
- better tool-use behavior specifically on reasoning models (o-series, GPT-5+)

See [responses-api.md](responses-api.md) for the structural differences (`input` vs.
`messages`, typed `output` items vs. `choices[0].message`, `previous_response_id`/`store`
for state instead of resending the transcript).

## Assistants API → Responses (mandatory)

**The Assistants API was sunset 2026-08-26.** Any code still targeting it needs to move to
Responses — this is not optional, unlike the Chat Completions migration. Responses absorbed
the Assistants API's persistent-thread and tool-orchestration capabilities via
`previous_response_id`/`store` plus the built-in hosted tools.

If you find a codebase still calling `/v1/threads` or the Assistants endpoints, flag that
it's on a sunset API before doing anything else with it.
