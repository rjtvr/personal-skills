# Function calling and tools

## Defining a tool

Declared in the `tools` parameter as JSON schema:

- `type`: `"function"`
- `name`: the function identifier the model will emit
- `description`: when and how to use it — this is what the model reasons over, write it
  like documentation for a caller who's never seen the function
- `parameters`: JSON schema for the arguments
- `strict`: `true` is recommended — enforces schema compliance on the model's output

**Strict mode requirements**, since they trip people up:
- every object needs `additionalProperties: false`
- every field must be listed in `required`
- an optional field is expressed as a nullable type (`["string", "null"]`), not by omitting
  it from `required`

## Call → execute → return

1. Model returns one or more tool calls: function name + JSON-encoded arguments.
2. You execute the function(s) server-side — the API never runs your code.
3. Send results back as `function_call_output` items, each carrying the `call_id` it answers
   and an `output` (string — JSON, plain text, or a file/image object).
4. Resubmit; the model synthesizes a final answer using the results.

## Parallel calls

On GPT-5+ models the model can emit multiple tool calls in one turn, executed concurrently
by your code. Disable with `parallel_tool_calls: false` if your tool execution isn't safe to
run concurrently (shared mutable state, rate-limited downstream calls).

## Token cost of tool definitions

Every tool definition in `tools` consumes input tokens on every request, whether or not it
gets called. For large tool sets, either use **tool search** (lets the model load tool
definitions on demand rather than up front) or trim the initially available set below ~20
tools.

## Beyond simple function calling

- **Programmatic Tool Calling** — the model can generate a small program (JavaScript) that
  composes multiple tool calls together, returned as a `program` item alongside the
  individual `function_call` items it invokes.
- **Remote MCP servers** — Responses can call tools exposed by a remote MCP server directly,
  without you proxying each call through your own backend.
- **Built-in hosted tools** — web search, file search, and code interpreter are available as
  first-class tools alongside custom functions, in the same request.
