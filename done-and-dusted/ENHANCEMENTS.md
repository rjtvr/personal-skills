# Extending done-and-dusted

Where things live, and how to change them without breaking the rest.

## Structure

| File | Holds | Change it when |
|---|---|---|
| `SKILL.md` | Workflow, rules, safety constraints | Behaviour changes |
| `references/evidence-gathering.md` | Git commands, what to extract | Adding a data source |
| `references/duplicate-handling.md` | Paths, naming, append safety | Changing storage layout |
| `assets/ENTRY_template.md` | Output format | Changing what an entry looks like |
| `config.json` | Your settings | Anything environment-specific |

Keep `SKILL.md` thin. It loads on every invocation; reference files load only when needed.
Detail belongs in `references/`.

**Rule of thumb:** if a change is about *what the output looks like*, edit the template. If
it's about *what gets gathered*, edit the evidence reference. If it's about *when to stop and
ask*, edit `SKILL.md`. Putting the same rule in two places guarantees drift.

## Easy changes

**Add a section to entries** — edit `assets/ENTRY_template.md` and add a rule for when it
applies. Only add sections with a clear inclusion condition; unconditional sections get
padded with filler, which is why the current design has three fixed and one conditional.

**Change the file layout** — edit the path shape in `duplicate-handling.md`. Note that
duplicate detection assumes one file per repo per day; switching to one file per task means
rewriting that logic, not just the path.

**Exclude repos** — `excludeRepos` already exists in config but isn't wired up. Add a check
after step 3 in `SKILL.md`.

**Different date format** — change it in `duplicate-handling.md`. Keep it sortable;
`YYYY-MM-DD` is why the folder listing is chronological for free.

## Worthwhile additions

### Weekly and monthly rollups

A second skill (`/week-in-review`) reading the last seven date folders and synthesising them.
This is why entries have consistent headings and frontmatter — the structure is what makes
a rollup possible without an LLM re-reading every diff.

Keep it a separate skill. Bolting a `--weekly` flag onto this one means one skill doing two
jobs with different failure modes.

### Search

`/what-did-i-do <query>` grepping `daily-chore/`. The `tasks:` frontmatter list is the
cheapest index — grep it before reading bodies.

Worth building only once you have a few months of entries. Before that, opening the folder
is faster.

### Ticket integration

Linear and Jira MCP connectors could pull the ticket title and status by ID. The branch
already yields the ID.

Guardrail: this makes the skill dependent on a network call in the middle of a save. Make it
best-effort — if the lookup fails, use the raw ID and carry on. A journal entry that fails to
write because Jira was slow is a bad trade.

### Status carry-forward

If yesterday's entry for a repo was `in-progress` with next steps, surface them when
starting a new entry for the same task. Turns the journal from a log into a handoff.

Needs care around what "the same task" means across days — the same problem duplicate
detection has, one directory level up.

### Push to Obsidian or Notion

The output is plain markdown with frontmatter, so an Obsidian vault works with zero changes —
just point `docsPath` at it. Notion would need an export step; keep it as a separate skill
reading `daily-chore/` rather than a second write path inside this one.

## Changes to be careful with

**Auto-invocation.** Removing `disable-model-invocation: true` would let Claude journal
whenever it thinks work finished. It would fire at the wrong moments and write entries you
didn't ask for. It's manual by design.

**Writing to git.** The skill is deliberately read-only against both your repos and your
notes folder. Committing notes automatically means commits appearing mid-session that you
didn't initiate, in a repo you may have staged changes in.

**Overwrite-in-place.** Every write is read-modify-write-whole for a reason. Truncating
loses earlier entries with no recovery — the worst failure this skill could have.

**Diff bodies in entries.** Tempting for detail, but it makes entries unreadable, duplicates
what git already stores, and is the most likely route for a secret to end up in a synced
folder.

## Testing changes

1. Make a scratch repo with a couple of commits and some uncommitted work.
2. Run against it and read the entry — is it useful in thirty seconds?
3. Run again the same day and confirm the duplicate prompt appears with all three options.
4. Check the earlier section survived intact.
5. Try it on a `main` branch and confirm it asks rather than inventing a task name.

Step 4 is the one that matters most. Everything else is cosmetic; losing an entry isn't.
