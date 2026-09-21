# Rewriting

The rewrite is where the analysis becomes useful. It's also where it's easiest to do harm —
by bloating a good prompt, changing its intent, or polishing something that needed splitting.

## Rules

**Preserve intent.** The rewrite asks for the same thing. If you think the user should want
something different, say so in the feedback; don't smuggle it into the rewrite.

**Fix only what the analysis found.** Every change traces to a specific finding. If a D was
Strong, leave that part alone. A rewrite that changes everything teaches nothing about which
changes mattered.

**Stay proportionate.** Match length to task. A quick lookup stays short. A good rule: if the
rewrite is more than about three times the original, check that each addition earns its
place. Over-specification is a Description failure too — it buries the parts that matter.

**Mark every change.** After the rewrite, list what changed and why, naming the D and
sub-competency. Without this, the user gets a better prompt once and learns nothing.

**Explain rather than command.** Prefer "the reader is a new hire, so avoid jargon" over "DO
NOT USE JARGON". Reasons help the model generalize to cases the prompt didn't anticipate, and
all-caps rules tend to be over-applied.

**Build in discernment hooks where they help.** Ask the AI to state assumptions, flag
uncertainty, or cite sources when the task involves facts. This makes the *next* step —
evaluating the output — easier, which is how a prompt can serve Discernment even though it
can't demonstrate it.

## By input type

**Single prompt** — rewrite the prompt.

**Prompt + output** — rewrite the prompt, prioritizing the gaps the output exposed.

**Full conversation** — rewrite the *opening* prompt so the follow-ups wouldn't have been
needed. Note which follow-ups the rewrite absorbs. This closes the Description–Discernment
loop the conversation left open — the lessons learned mid-conversation become part of the
starting instructions.

**System prompt / SKILL.md** — produce a revised version as a separate artifact. Preserve its
structure where it works. For SKILL.md, keep the frontmatter valid, and treat the description
field as a first-class target: it decides when the skill triggers. Never overwrite the
original file; in Claude Code, only write the revision to disk when asked, and to a new path.

## When not to rewrite

- **Delegation says the task should be split or not given to AI.** Offer the split — often
  two or three smaller prompts — or the alternative, instead of a polished single prompt.
- **The prompt is already Strong across what's assessable.** Say so. Offer at most a small
  optional tweak. Manufacturing changes to justify the analysis is dishonest.
- **The prompt seeks harmful output.** The analysis stops at the Diligence finding.
