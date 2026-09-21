# Usability and user flows

Accessibility and visual checks are largely element-level. This pass is about whether the
sequence works. Walk the actual flows rather than reviewing screens in isolation — most
serious usability defects live in the seams between screens.

## Flow walkthrough

Pick the 2–3 flows that matter most (signup, primary task, checkout, settings change) and
narrate each step as a user with no prior knowledge:

- **Entry.** Is it obvious what this screen is for and what to do first?
- **Progress.** In multi-step flows, does the user know how many steps remain?
- **Reversibility.** Can they go back without losing input? Losing form data on back
  navigation is a P1 that developers rarely notice because they don't make mistakes in
  their own flow.
- **Exit.** Is completion confirmed unambiguously? "Did that save?" is a design failure.

## Feedback and system status

- Every action produces a response within ~100ms, even if only a pressed state.
- Operations over ~1s show progress. Over ~10s, show what's happening and let the user
  leave.
- Async success is confirmed visibly *and* announced (see 4.1.3).
- Optimistic UI has a defined rollback path when the request fails.
- Double-submission is prevented, not just discouraged.

## Error handling and recovery

This is where audits find the most real damage:

- Errors appear next to the cause, not only in a banner at the top.
- Wording says what to do, not what the system feels. "Enter a date in DD/MM/YYYY format"
  beats "Invalid input".
- No blame, no jargon, no raw error codes as the primary message (codes can be secondary).
- Validation timing: on blur or submit, not on every keystroke while the user is mid-word.
- Destructive actions are confirmed *or* undoable — undo is usually the better design.
- Network failure is handled distinctly from validation failure.
- Partial failure in batch operations is communicated per-item.

## Cognitive load

- **Choice count.** More than ~7 peer options at one decision point needs grouping.
- **Required input.** Every field should justify itself. Optional fields marked as such.
- **Jargon.** Internal domain terms leaking into user-facing copy is extremely common in
  developer-built UI, and it's usually invisible to the person who built it.
- **Memory burden.** Don't make users carry information between screens. Show the value
  they entered rather than asking them to remember it.
- **Defaults.** Sensible defaults do more for completion rates than most visual polish.

## Forms specifically

Forms are where most task failure occurs, so give them a dedicated pass:

- Labels visible and persistent (not placeholder-only).
- Input types correct (`type="email"`, `type="tel"`) so mobile keyboards adapt.
- `autocomplete` present.
- Format requirements shown *before* the error, not after.
- Password managers not blocked; paste not disabled.
- No silent truncation of pasted values.
- Field order matches user expectation and real-world grouping.
- Submit button state reflects validity without disabling it outright — a disabled submit
  with no explanation of why leaves users stuck with no feedback path.

## Content and copy

- Button labels are verbs describing the outcome ("Create account", not "Submit").
- Headings describe content, not structure.
- Consistent terminology — one concept, one word, across the whole product.
- Empty states teach rather than apologize.
- Microcopy present where a decision is non-obvious.
