# personal-skills

Rajat's personal collection of Claude Code skills, packaged as an installable plugin
marketplace. Glossary in [CONTEXT.md](./CONTEXT.md); architectural decisions in
[docs/adr/](./docs/adr/).

## Structure

Every skill lives in its own top-level folder and doubles as a plugin:

```
<skill-name>/
├── .claude-plugin/
│   └── plugin.json       # name, description, version, author — marketplace metadata
├── SKILL.md               # required — frontmatter: name, description, optional allowed-tools
├── references/            # optional — loaded on demand, not on every invocation
├── assets/                # optional — templates the skill fills in
├── scripts/                # optional — code the skill shells out to
└── commands/               # optional — slash-command aliases (e.g. a short alternate name)
```

The root [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) lists every
plugin so the repo can be added as a marketplace:

```
/plugin marketplace add rjtvr/personal-skills
/plugin install <skill-name>@personal-skills
```

## CI

[`.github/workflows/validate.yml`](./.github/workflows/validate.yml) runs on every push and
PR: `claude plugin validate --strict` against the marketplace manifest and every plugin it
lists, plus [`.github/scripts/check-consistency.mjs`](./.github/scripts/check-consistency.mjs),
which enforces the doc-sync rule below in code — it fails if a plugin in the marketplace is
missing `SKILL.md`/`plugin.json`, or has no row in the skill index, or vice versa. Both steps
read `.claude-plugin/marketplace.json` at run time, so adding a skill needs no workflow edit.

## Skill index

| Skill | Status | Purpose | Last updated |
|---|---|---|---|
| [4d-analyzer](./4d-analyzer/SKILL.md) | stable | Grade a prompt/conversation/SKILL.md against Anthropic's 4D AI Fluency framework and rewrite it | 2026-09-21 |
| [done-and-dusted](./done-and-dusted/SKILL.md) | stable | Write a work-journal entry for the task just finished | 2026-09-22 |
| [next-step](./next-step/SKILL.md) | stable | Interview-driven personal roadmap (career, learning, life, money) | 2026-09-21 |
| [responsive-ui-debug](./responsive-ui-debug/SKILL.md) | stable | Measure and fix responsive/overflow layout bugs | 2026-09-21 |
| [security-audit](./security-audit/SKILL.md) | stable | OWASP-ranked security audit with brief/gate discipline | 2026-09-22 |
| [ux-audit](./ux-audit/SKILL.md) | stable | Severity-ranked UI/UX audit plus an executable fix plan | 2026-09-07 |

**Status** values: `idea` (not written yet) → `draft` (SKILL.md exists, untested or rough) →
`stable` (used and works) → `deprecated` (superseded or retired, kept for reference).

Update this table by hand whenever a skill is added, its maturity changes, or it's retired —
it's the whole point of the tracking structure; a stale table is worse than none.

## Adding a new skill

1. Create `<skill-name>/SKILL.md` with `name` and a specific, trigger-rich `description` —
   see any existing skill for the level of detail Claude Code needs to auto-invoke it correctly.
2. Add `<skill-name>/.claude-plugin/plugin.json` (name, description, version, author) —
   copy an existing one and edit.
3. Add it to `plugins` in `.claude-plugin/marketplace.json`.
4. Add a row to the **Skill index** above, status `idea` or `draft` depending on how baked it is.
5. Flesh out `references/`, `assets/`, `scripts/` only as the skill actually needs them —
   keep `SKILL.md` itself thin, since it loads on every invocation and reference files don't.
6. Update every doc the new skill actually affects, in the same change that adds it — a skill
   isn't done until these are in sync, not as a follow-up:
   - **`CLAUDE.md`** — the skill index (step 4) and, if the skill introduces a structural
     pattern worth reusing (a new gate/log discipline, a new folder convention), the
     **Conventions** section below.
   - **`CONTEXT.md`** — add or revise a term if the skill introduces one, or if it uses an
     existing term in a way that doesn't fit its current definition.
   - **`docs/adr/`** — write a new ADR only if this skill's addition meets the three-part test
     in the definition-of-done below; most new skills won't need one.
   - **Root `README.md`** — update only if the skill changes the install/usage story for
     someone landing on the repo (new one being added rarely does).

   **Definition of done for any change to this repo** — not just adding a skill: if you
   touched something a doc describes (renamed a skill, changed its status, changed the
   plugin/marketplace shape, resolved a glossary term differently), update that doc in the
   same change. A structural decision earns an ADR only when it's hard to reverse, would
   surprise a future reader without context, and was a real trade-off between genuine
   alternatives — skip the ADR otherwise. Never leave `CLAUDE.md`, `CONTEXT.md`, or the skill
   index describing a repo state that no longer exists.

## Conventions carried over from the existing skills

- Frontmatter `description` should name concrete trigger phrases a user might actually say —
  it's what Claude Code matches against for auto-invocation, not just documentation.
- Skills that gate on human approval before acting (security-audit, ux-audit) write an
  `AUDIT_BRIEF.md`-style contract before doing anything, and log judgment calls to a
  `DECISIONS.md`. Follow that pattern for any new skill that inspects someone else's
  code/design and could over-reach.
- Manually-triggered skills that should never auto-fire (done-and-dusted) set
  `disable-model-invocation: true` in frontmatter.
