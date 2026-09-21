# Personal Skills

A personal collection of Claude Code skills, packaged as an installable plugin marketplace.

## Language

**Skill**:
A `SKILL.md` file with YAML frontmatter (`name`, `description`, optional `allowed-tools`)
that teaches Claude Code a workflow. Loaded automatically when the description matches, or
invoked manually as a slash command.

**Plugin**:
The distributable unit in this repo — a top-level folder containing a `.claude-plugin/plugin.json`
manifest plus one `SKILL.md` and optionally `commands/`, `references/`, `assets/`, `scripts/`.
Every plugin here currently wraps exactly one skill.
_Avoid_: bundle, package

**Marketplace**:
The root `.claude-plugin/marketplace.json` manifest listing every plugin in this repo, so it
can be added with `/plugin marketplace add` and its plugins installed individually.

**Status**:
A skill's lifecycle stage, tracked in the index in [CLAUDE.md](./CLAUDE.md): `idea` → `draft`
→ `stable` → `deprecated`. Independent of the `version` field in `plugin.json`, which tracks
packaging revisions, not maturity.
_Avoid_: version (when talking about maturity — version numbers and status move on separate
clocks: a stable skill can still bump its version for a small fix)
