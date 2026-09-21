---
status: accepted
---

# Formalize this repo as a Claude Code plugin marketplace

The repo already held six skill folders in an ad-hoc mix of shapes (flat `SKILL.md`, and one
nested distribution bundle under `done-n-dusted/`). We decided to add a root
`.claude-plugin/marketplace.json` plus a `.claude-plugin/plugin.json` in every skill folder,
making the whole repo installable via `/plugin marketplace add` and each skill installable
individually via `/plugin install <name>@personal-skills`.

The alternative was to leave it a plain collection, copying or symlinking skill folders into
`~/.claude/skills` by hand. We chose the marketplace path because the copy/symlink step is
pure friction that recurs every time a skill changes, and it's the only option that lets
skills be shared or installed on another machine without re-explaining the layout.

Trade-off: every new skill now needs a `.claude-plugin/plugin.json` alongside its `SKILL.md`,
and the marketplace-listed metadata (name, description, version) has to be kept in sync with
the `SKILL.md` frontmatter by hand — there's no single source of truth enforced by tooling.
