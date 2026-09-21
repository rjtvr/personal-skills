# Evidence matrix

What each input type can and cannot tell you. This is the core of the skill: verdicts must
come from evidence the input actually contains.

## At a glance

| Input | Delegation | Description | Discernment | Diligence |
|---|---|---|---|---|
| Single prompt | Partial | **Full** | Not assessable | Minimal |
| Prompt + output | Partial | **Full** | Partial | Minimal |
| Full conversation | Good | **Full** | **Good** | Partial |
| System prompt / SKILL.md | **Good** | **Full** | **Good** (as designed-in) | **Good** (as designed-in) |

## Single prompt

- **Delegation — partial.** You can judge whether the task suits AI (does it need data the AI
  can't have?) and whether it's overloaded. You can't see the user's goal beyond what's written.
- **Description — full.** This is what a prompt *is*. Assess Product, Process, Performance.
- **Discernment — not assessable.** Discernment happens after the response. Don't infer it
  from prompt wording. You *can* note whether the prompt makes discernment easier later (asks
  for sources, confidence, stated assumptions) — but report that under Description, and mark
  Discernment itself as not assessable.
- **Diligence — minimal.** Visible only if the prompt shares sensitive data or signals
  intended use. Usually mark as not assessable, noting any red flag seen.

## Prompt + output

Everything above, plus:

- **Discernment — partial.** You can't see what the user *did* with the output, but you can
  identify what a discerning reader would need to check: unsupported claims, likely
  invented details, gaps against the request. Frame it as "here is what to scrutinize",
  never as "you failed to scrutinize this" — you have no evidence of their review.
- **Description — sharper.** The output reveals which gaps in the prompt actually mattered.
  An ambiguity the model resolved sensibly is lower priority than one it got wrong.

## Full conversation

The richest evidence for how someone *works* with AI.

- **Delegation — good.** The arc shows whether the task was scoped well, split sensibly, or
  thrashed.
- **Description — full**, including how it evolved across turns.
- **Discernment — good.** Follow-ups are the evidence. Did the user catch errors? Were
  corrections specific ("the date in paragraph 2 is wrong") or vague ("try again")? Did they
  accept an obviously shaky claim?
- **Diligence — partial.** Visible where the user discusses sharing, verifying, or using the
  result.

The key thing to look for is the **Description–Discernment loop**: did lessons from
evaluating outputs get folded back into better instructions? Count follow-ups that correct
the same class of problem — repeated corrections mean the loop never closed.

## System prompt / SKILL.md

These configure an agent, usually in Agency mode, so the Ds appear as designed-in behavior:

- **Delegation — good.** What's handed to the AI, what's reserved for the human, where the
  boundaries sit. Are irreversible actions gated?
- **Description — full.** Clarity of instructions, conflicts between them, whether the *why*
  is explained (instructions with reasons generalize better than bare rules).
- **Discernment — good, as designed-in.** Does the artifact build in verification — checking
  its own work, flagging uncertainty, asking when ambiguous, separating confirmed from
  unconfirmed?
- **Diligence — good, as designed-in.** Guardrails, data handling, what it must never do,
  transparency about being AI, how it handles harmful requests.

For SKILL.md specifically, also check the description field: it decides when the skill
triggers, so a vague description is a Delegation failure — the skill never gets handed the
work it was built for.

## Mixed or unclear input

If the input type is ambiguous — a pasted block that might be a prompt or a system prompt —
ask. Assessing a system prompt as a one-off prompt misses most of what matters about it.
