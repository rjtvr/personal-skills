# Streaming

Set `stream=true` on a Responses call to start receiving output as it's generated, instead
of waiting for the full response.

## Event lifecycle

The Responses API emits **typed, semantic events**, not raw text deltas you have to parse
yourself:

- `response.created` — once, at the start
- `response.output_text.delta` — repeatedly, as text is generated
- `response.completed` — once, at the end
- `error` — on failure mid-stream

Plus specialized events for function calls, structured-output fields, and other tool use as
they stream in.

## Consuming the stream

- **SDK**: iterate the stream and branch on each event's `type` — the SDK gives you typed
  event objects, not raw JSON to parse.
- **Raw HTTP**: it's server-sent events (SSE) under the hood; filter on the `type` field if
  you're not using an SDK.

## Moderation implication

Streaming partial output makes content moderation harder — you're evaluating incomplete
text. If the application has moderation requirements, decide explicitly whether to moderate
the streamed deltas as they arrive (weaker signal, faster) or buffer and moderate the
complete response before showing it to a user (stronger signal, kills the latency benefit
streaming was for).
