# What each skill might ask permission for

Claude Code prompts for approval the first time a session uses a tool or Bash command not
already allowlisted (in `SKILL.md` frontmatter, project settings, or your own permission
mode). This is a heads-up for someone trying a skill from this marketplace for the first
time, so the prompts aren't a surprise.

Nothing here runs automatically — it's what to expect you'll be *asked* about, not something
these skills do without asking. `allowed-tools` in a skill's frontmatter pre-approves only
the exact Bash pattern listed; every other tool call (Read, Write, Edit, WebFetch, other Bash
commands) still prompts under a default permission mode.

| Skill | Pre-approved (`allowed-tools`) | Will likely also prompt for |
|---|---|---|
| [4d-analyzer](../4d-analyzer/SKILL.md) | — | Write (the analysis report) |
| [done-and-dusted](../done-and-dusted/SKILL.md) | `git status`, `git diff`, `git log`, `git rev-parse`, `git branch`, `git remote`, `git config` (read-only) | Write, to a folder **outside this repo** (a path you confirm on first run, stored in `config.json`) |
| [next-step](../next-step/SKILL.md) | — | Write, to a folder **outside this repo** (a `notesPath` you confirm on first run) |
| [openai-api](../openai-api/SKILL.md) | — | WebFetch, to re-check current OpenAI pricing/docs before quoting a number |
| [responsive-ui-debug](../responsive-ui-debug/SKILL.md) | — | Bash, to run `scripts/diagnose.py` (Playwright — may prompt to install a browser binary on first use); Write, for screenshots if you pass `--shots` |
| [security-audit](../security-audit/SKILL.md) | `python3 scripts/normalize_findings.py` | Bash, for whatever scanners you authorize in the `AUDIT_BRIEF.md` gate (`semgrep`, `gitleaks`, `trivy`/`osv-scanner`, `npm audit`/`pip-audit`/etc.); WebFetch/network, only if you separately authorize CVE lookups; Write, for the brief and report files |
| [ux-audit](../ux-audit/SKILL.md) | `python3 scripts/tickets_to_csv.py` | WebFetch or browser automation, if you hand it a live URL instead of screenshots; Write, for the report and fix plan |

## Reading the table

- **"Pre-approved"** means that exact command pattern won't prompt — everything else the
  skill does still goes through your normal permission flow.
- **security-audit** and **ux-audit** are the two skills that write an approval gate into
  their own workflow (an `AUDIT_BRIEF.md`-style contract) before doing anything beyond
  read-only recon — see each skill's `SKILL.md` for what that gate covers. Claude Code's own
  tool-permission prompts still apply on top of that gate; the two are independent.
- **done-and-dusted** and **next-step** are the two skills that write outside this
  repository by design (a work journal / a personal roadmap aren't project artifacts) —
  both confirm the destination path with you before the first write, not just the first
  Write-tool prompt.
- If you run with a permissive permission mode (auto-approving Bash or all tools), these
  prompts won't appear — the skill still does the same things, just without asking first.
