# personal-skills

Rajat's personal collection of [Claude Code](https://claude.com/claude-code) skills,
packaged as an installable plugin marketplace.

This repo is **private**. The install command below only works for the repo owner (already
authenticated via `gh`/git) or an account added as a collaborator — cloning or adding this
marketplace with no access will fail, not silently skip.

## Install

```
/plugin marketplace add rjtvr/personal-skills
/plugin install <skill-name>@personal-skills
```

See the [skill index](./CLAUDE.md#skill-index) for what's available and each skill's
`SKILL.md` for what it does and when it triggers.

## Repo conventions

Contributor/agent-facing conventions (folder layout, how to add a skill, the status
tracking table) live in [CLAUDE.md](./CLAUDE.md). Domain vocabulary is in
[CONTEXT.md](./CONTEXT.md). Architectural decisions are in [docs/adr/](./docs/adr/).
