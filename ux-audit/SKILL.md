---
name: ux-audit
description: Audit the UI/UX of a web app, mobile app, or component library and produce a severity-ranked findings report plus a ready-to-execute fix plan. Covers accessibility (WCAG), visual consistency and design-system drift, and usability and user flows. Use this whenever the user asks for a UI review, UX review, design review, accessibility audit, a11y check, WCAG check, "why does this screen feel off", "make this more polished", "is this accessible", "review my UI before launch", or hands over screenshots, a live URL, a component directory, or Figma exports and wants feedback on the interface. Also use when the user wants UI problems turned into actionable work for Claude Code or into tickets. Do not use for backend architecture, API design, or performance profiling unrelated to perceived UI quality.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/tickets_to_csv.py *)
---

# UI/UX Audit

Audit an interface, rank what's wrong by how much it actually hurts users, and hand back
work that another agent can execute without re-deriving the analysis.

The failure mode this skill exists to prevent: a flat list of forty observations, all
weighted equally, half of them subjective taste, none of them tied to a file. That output
looks thorough and is nearly useless. Aim instead for a short list of things that matter,
each with evidence and a concrete change.

## Workflow

0. **Interview and lock the brief** — nothing runs before approval
1. **Take inventory of evidence** — see `references/evidence-gathering.md`
2. **Run the checklists** against that evidence — three reference files, below
3. **Assign severity** using the model in this file
4. **Write two artifacts** — `UX_AUDIT.md` and `FIX_PLAN.md`
5. **Optionally emit tickets** — only if the person tracks work in Jira/Linear/GitHub
6. **Log the judgment calls** — `DECISIONS.md`, see `references/decisions.md`

Do not skip step 1. Auditing from assumptions about what the code probably looks like
produces confident findings about problems that don't exist, which is worse than finding
nothing.

## Step 0 — Interview, then lock the brief

**This is a gate, not a preamble.** No checklist runs and no finding is written until the
person approves a written brief.

1. **Read-only recon.** List the components, note the framework, check for a token file,
   see which evidence exists. No evaluation, no findings. This exists so the interview can
   skip what's observable.
2. **Interview.** Follow `references/interview.md` — six areas, grouped two or three per
   turn, using `AskUserQuestion` where available.
3. **Write `AUDIT_BRIEF.md`** from `assets/AUDIT_BRIEF_template.md`. Show it. **Stop.**
4. **Wait for explicit approval.** Anything short of a clear yes is a revision: update the
   brief and re-confirm.

Writing the brief and continuing in the same turn defeats the mechanism entirely. The turn
ends when the brief is presented.

The brief is a contract. It exists so that "you audited the wrong thing" costs two lines
instead of a full redo, and so the person can correct a misread scope before it becomes
forty findings.

Skip the interview only when the request already fixes scope, depth, and evidence
("check `Button.tsx` for a11y only, report inline"). Partial specification means asking
about the rest, not assuming it.

## Step 1 — Inventory the evidence

Ask what's available before inspecting anything. Available sources determine which
findings are even possible:

| Source | Catches | Blind to |
|---|---|---|
| Screenshots / recordings | Visual hierarchy, spacing rhythm, real rendered contrast, empty/error states | Keyboard behaviour, semantics, ARIA, focus order |
| Source code | Missing labels, div-as-button, focus traps, hardcoded colors, magic-number spacing | Whether it *looks* right when composed |
| Live URL | Keyboard traversal, focus visibility, reflow at 320px, zoom to 200%, real DOM | Design intent |
| Design files | Intended tokens, intended states, what the build drifted *from* | What actually shipped |

With multiple sources, the highest-value findings are the **contradictions** between them:
design specifies a 44px tap target, code hardcodes 32px, screenshot confirms it renders
small. That triangulated finding is worth ten single-source observations.

Read `references/evidence-gathering.md` for the inspection procedure per source, including
what to look for in code and how to test a live URL by hand.

## Step 2 — Run the checklists

Read these as needed rather than all at once:

- [references/checklist-accessibility.md](references/checklist-accessibility.md) — WCAG 2.2 A/AA, mapped to success criteria
- [references/checklist-visual.md](references/checklist-visual.md) — token drift, spacing rhythm, typography, state coverage
- [references/checklist-usability.md](references/checklist-usability.md) — flows, feedback, error recovery, cognitive load

Cover accessibility first. It has objective pass/fail criteria and legal weight, so it
anchors the report in things nobody can argue with. Visual and usability findings land
better once the reader already trusts the analysis.

## Step 3 — Assign severity

Severity answers "what happens to a user who hits this", not "how much does this bother
me". Use this ladder:

**P0 — Blocker.** A user cannot complete the task. Keyboard user can't reach the submit
button. Screen reader announces nothing for the only navigation. Text invisible at
default zoom. Any WCAG **Level A** failure on a primary flow lands here by default.

**P1 — High.** Task is completable but the experience is materially degraded or excludes a
group. Contrast below 4.5:1 on body text. No visible focus indicator. Destructive action
with no confirmation. No error message when submission fails. Most WCAG **Level AA**
failures live here.

**P2 — Medium.** Friction, inconsistency, or confusion that costs time but not success.
Inconsistent button styles across screens. Spacing that breaks rhythm. Missing loading
state. Ambiguous label.

**P3 — Low.** Polish. Slight optical misalignment, minor copy tone, animation easing.

Two rules keep this honest:

- **Never promote taste to P0/P1.** "I'd use a different blue" is P3 or it isn't a finding.
  If a severity can't be justified by naming the user who gets hurt and how, drop it a level.
- **Frequency multiplies severity.** A P2 in a shared `<Button>` used on every screen
  outranks a P1 on an admin page three users visit. Note reach explicitly.

## Step 4 — Write the artifacts

Produce exactly two files. Templates are in `assets/`.

### `UX_AUDIT.md` — the findings

For humans. Uses `assets/AUDIT_REPORT_template.md`. Every finding follows this shape:

```markdown
### [P1] Form inputs have no programmatic label

**Where:** `src/components/SearchBar.tsx:24`
**Evidence:** Input has `placeholder="Search"` and no `<label>`, `aria-label`, or
`aria-labelledby`. Placeholder text disappears on focus and is not announced as a name.
**Impact:** Screen reader users hear "edit text, blank" — no way to know what the field
wants. Also fails voice-control targeting.
**Criterion:** WCAG 4.1.2 Name, Role, Value (Level A) — also 3.3.2 Labels or Instructions
**Reach:** Search bar is in the global header, so every screen.
**Fix:** Add a visually-hidden `<label htmlFor>` bound to the input id, or `aria-label`
if the visual design can't accommodate a label.
```

Non-negotiable: **Where**, **Evidence**, **Impact**, **Fix**. A finding without a file
path or a screenshot region isn't actionable. A finding without observed evidence is a
guess — mark it `[unverified]` and say what would confirm it rather than asserting it.

### `FIX_PLAN.md` — the executable work

For Claude Code. Uses `assets/FIX_PLAN_template.md`. This is the artifact that makes the
audit worth doing, so optimize it for an agent that has the repo but not this conversation.

Structure it as **batches**, not a flat task list. A batch groups changes that touch the
same files or share the same verification step, which keeps the agent from thrashing
between unrelated areas and lets it commit coherently.

Order batches by: token/primitive fixes first (they cascade), then shared components, then
page-level fixes, then polish. Fixing `<Button>` once often closes six page-level findings —
say so, so nobody does the work twice.

Each task must carry:

- **Finding ID** back-reference (`A-03`) so the agent can read context in `UX_AUDIT.md`
- **Files to touch** — actual paths, not "the button component"
- **The change** — specific enough to implement, loose enough to respect existing patterns
- **Verification** — how to confirm it worked (`tab to the field, confirm focus ring is
  visible at 3:1 against the background`)
- **Risk** — what might break. Changing a shared component is a blast-radius warning.

End the plan with an **explicitly out of scope** section listing what you chose not to fix
and why. Without it, the executing agent invents scope.

## Step 5 — Tickets (optional)

Only when the person tracks work in an issue tracker. Skip it otherwise — an unwanted
`tickets/` directory is noise.

Write one file per ticket into `tickets/<ID>.md` using `assets/TICKET_template.md`. The
format is deliberately tracker-neutral: YAML frontmatter carries the structured fields,
markdown carries the human content. Author neutral and map late — writing in one tracker's
idioms means re-authoring when the team moves, and teams move.

`references/ticket-mapping.md` has the field mapping for Jira, Linear, and GitHub, plus
import routes. `scripts/tickets_to_csv.py` converts a ticket directory into Jira or Linear
CSV, or a `gh issue create` script. Invoke it by absolute path, since the working directory
is the user's project rather than the skill folder:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/tickets_to_csv.py tickets/ --target linear > linear-import.csv
```

Two things that go wrong here. **Granularity**: one ticket per *fix*, not per *finding* —
seventeen hardcoded greys is one ticket that closes seventeen findings, which is what
`closes_findings` records. **Linear priority**: its scale is 0–4 where 0 means *no
priority*, not highest, so a naive numeric mapping silently buries everything.

Tickets and `FIX_PLAN.md` are not redundant. The plan is sequenced work for an agent with
the repo; tickets are units of tracked work for a team. Generate both only when both
audiences exist.

## Decision discipline

Judgment calls get **logged**, not gated. Four things get gated. See
`references/decisions.md` for the full protocol.

**Gates — never self-authorize:** starting the audit without an approved brief; expanding
scope beyond it; creating `tickets/`; modifying any source file. This skill audits, it
does not fix — even an obvious one-line fix waits for a separate request.

**Log — decide, but show your work.** Write `DECISIONS.md` from
`assets/DECISIONS_template.md`. Threshold: log a decision when a reasonable reviewer might
have made it differently. Severity calls, aggregations, exclusions, assumptions about
intent. Not routine steps — a log of everything hides the decisions worth reviewing.

Every entry carries a **Reverse it** line. A decision you can see but can't easily undo
isn't under the person's control, which was the point.

Mark affected findings inline with the decision ID (`[D-03]`) so nothing has to be
cross-referenced by hand.

## Working with the person

Audits generate more findings than anyone will action. Before writing the plan, if the
list exceeds roughly a dozen items, say what you found at each severity and ask what
they want in this pass — P0/P1 only is a common and sensible answer. Do not silently
truncate; tell them what you're setting aside.

If evidence is thin (one screenshot, no code), say what you can and can't conclude. An
audit that admits its blind spots is trustworthy. One that pads to look comprehensive
isn't.
