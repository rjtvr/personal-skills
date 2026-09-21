# The AI Fluency Framework

Anthropic's AI Fluency Framework, developed with Prof. Rick Dakan (Ringling College of Art
and Design) and Prof. Joseph Feller (University College Cork). Four interconnected
competencies for working with AI effectively, efficiently, ethically, and safely.

Source material: https://aifluencyframework.org/ and the free course *AI Fluency: Framework
& Foundations* on Anthropic Academy. The summaries below are paraphrased for analysis use.

## Three modes of working with AI

Identify the mode first — what "good" looks like differs across them.

- **Automation** — the AI performs a defined task from instructions. Good Description here
  is precise and complete; there's little room for the AI to ask back.
- **Augmentation** — human and AI work together as creative or thinking partners. Good
  practice is iterative; an underspecified first prompt can be fine if the conversation
  refines it.
- **Agency** — the human configures the AI to act independently, often for other people.
  System prompts and skills live here. Gaps matter most, because nobody is watching each
  output as it's produced.

## Delegation

Setting goals and deciding whether, when, and how to engage AI at all.

- **Problem Awareness** — understanding the goal and the work before involving AI. Is the
  objective clear? Is the prompt solving the actual problem, or a symptom of it?
- **Platform Awareness** — knowing what the AI system can and can't do. Does the task need
  current information, private data, or tools the AI doesn't have? Is the model being asked
  to be certain about something it can only estimate?
- **Task Delegation** — dividing work sensibly between human and AI. Is the whole task handed
  over when parts need human judgment? Would splitting it into steps work better?

**Weak signals:** asking for facts the AI can't know; one giant prompt doing five jobs;
handing over a decision that needs human accountability.

## Description

Communicating clearly with AI.

- **Product Description** — what output is wanted: content, format, length, audience, style,
  examples of good output.
- **Process Description** — how the AI should approach it: steps, reasoning, sources to use
  or avoid, what to consider.
- **Performance Description** — how the AI should behave in the interaction: role, tone,
  whether to ask clarifying questions, whether to push back, how concise to be.

**Weak signals:** no audience; no format; ambiguous success criteria; context the AI needs
left in the user's head; instructions that contradict each other.

## Discernment

Evaluating AI outputs, processes, and behavior critically. Mirrors Description:

- **Output** — is the result accurate, complete, fit for purpose?
- **Process** — did the AI reason soundly, or reach the right answer by a shaky route?
- **Behavior** — did the AI act as asked — tone, scope, honesty about uncertainty?

**The Description–Discernment loop:** evaluating an output reveals what the description
was missing, which feeds a better description. In a conversation, follow-ups are the visible
trace of this loop — their quality is direct evidence of Discernment.

**Weak signals:** accepting a confident answer without checking; follow-ups that only say
"try again"; not noticing an invented citation; correcting the output but not the prompt
that caused it.

## Diligence

Taking responsibility for AI-assisted work.

- **Creation Diligence** — choosing AI systems and ways of working thoughtfully; considering
  what data is shared and what could go wrong.
- **Transparency Diligence** — being honest about AI's role with the people who need to know.
- **Deployment Diligence** — verifying and owning the output before it's used or shared.

**Weak signals:** pasting sensitive data without thought; shipping unverified output;
presenting AI work as solely one's own where disclosure is expected; a system prompt with no
guardrails for an agent that acts on real systems.

## How the Ds interact

They aren't independent scores. Common patterns worth naming in feedback:

- **Strong Description, weak Discernment** — polished requests, unchecked results. Produces
  confident mistakes quickly; the most expensive profile.
- **Weak Delegation masking as weak Description** — the prompt reads badly because it's doing
  too many jobs at once. The fix is splitting, not rewording.
- **Discernment without loop-closing** — catching errors in follow-ups but never folding the
  lesson back into the original prompt, so the same correction is needed every time.
