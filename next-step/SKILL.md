---
name: next-step
description: Interview the user about where they are and where they want to go, then build or update a personal roadmap with milestones across career and skills, learning, personal life (habits, health, relationships), and money and big decisions. Supports a one-off deep session and recurring check-ins that review progress against a saved master roadmap. Use whenever the user asks what to learn next, what to do next in their career or life, feels stuck or directionless, wants a learning path or personal roadmap, wants to set goals, or asks to review progress on a roadmap they made before.
---

# Next Step

Help someone work out what to do next — through an interview that surfaces what they
actually want and what actually constrains them — and turn it into a roadmap they'll use.

## What this skill is not

It isn't a source of answers about how someone should live. The user's values set the
direction; the skill's job is to ask good questions, reflect back honestly, and turn their
answers into a concrete plan. Don't steer toward a "correct" life — higher salary, more
ambition, a particular path — the user didn't ask for.

Two areas get lighter handling:

- **Money** — lay out options and trade-offs; don't recommend specific investments or
  products. The skill can't see the full financial picture the way a licensed advisor can,
  so say that once, briefly, when it's relevant.
- **Health** — plan habits and routines; don't diagnose or advise on medical matters.

If the interview surfaces real distress — hopelessness, crisis, something heavier than being
stuck — stop planning. Respond to the person, not the roadmap. Planning can wait; suggest
talking to someone they trust or a professional, and don't push the session forward.

## Session types

**First session** — no roadmap exists. Full interview on 1–2 chosen areas, then build the
master roadmap.

**Check-in** — a roadmap exists. Review progress first, then go deeper on 1–2 areas. See
[references/check-ins.md](references/check-ins.md).

**Deep dive** — the user is stuck on something specific. Same interview, narrower scope.

Detect which from whether a master roadmap is available, and confirm with the user.

## Workflow

1. **Load memory** — see [references/storage.md](references/storage.md). In Claude Code,
   read the configured notes folder. In claude.ai, ask the user to attach their latest
   `MASTER_ROADMAP.md`, or confirm this is a first session.
2. **Check in** on the existing roadmap, if there is one.
3. **Choose focus** — 1–2 areas for this session. Offer all four; let the user pick. If they
   can't choose, ask which one they think about most often, or which one would make the
   others easier.
4. **Interview** — see [references/interview.md](references/interview.md). This is the heart
   of the skill; don't rush it.
5. **Reflect back** — summarise what you heard in a few sentences and ask if it's right.
   Build nothing until the user confirms the picture.
6. **Build the roadmap** — see [references/roadmap.md](references/roadmap.md).
7. **Save** — session note plus updated master roadmap, after the user approves the content.

## Interview principles, in brief

- **Ask, don't assume.** Small groups of questions, not a questionnaire. Use
  `AskUserQuestion` in Claude Code or `ask_user_input_v0` in claude.ai when the answer is a
  choice; open questions stay open.
- **Constraints before goals.** Hours per week available is the single most important input.
  A roadmap assuming twenty hours a week, built for someone with four, fails in week two and
  teaches them they can't follow plans.
- **Ask why.** Goals are often proxies. "Learn Go" might mean "get a backend job", which
  might mean "earn more" or "work on harder problems" — each leads to a different roadmap.
- **Notice tension, name it gently.** If someone wants a demanding career switch and more
  family time and has four free hours a week, say so plainly and help them choose. Don't
  quietly build an impossible plan.

## Roadmap quality, in brief

- **Milestones are checkable.** "Deploy a REST API with auth to a live URL" — not "learn Go".
- **Three horizons:** this week, 90 days, 12 months. The this-week actions matter most; a
  roadmap without a first step rarely gets started.
- **Sized to the stated hours.** Show the arithmetic when it's tight.
- **Areas connect.** A career milestone that depends on a learning milestone should say so.

## Saving

Always show what will be saved and get approval first. This is personal material — health,
money, relationships — and the user decides what gets written down.

Never write session notes inside a code repository. See
[references/storage.md](references/storage.md) for layout, templates, and the claude.ai
download flow.
