---
name: done-and-dusted
description: Capture a work-journal entry for the task just completed. Inspects git state and session context, writes a concise summary to the central daily-chore folder outside the repository, organised by date and repository. Manually invoked at the end of a piece of work. Accepts an optional task name as an argument.
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git remote:*), Bash(git config:*)
---

# Done and Dusted

Write a work-journal entry for what was just finished, into a central location outside the
repository, so future-you can reconstruct what happened and why.

`$ARGUMENTS`, when provided, is the task name. Use it instead of inferring one.

## Non-negotiables

- **Read-only against the working repository.** Only the git commands in `allowed-tools`.
  Never stage, commit, checkout, stash, or edit code. The user is mid-work; touching their
  repo is unacceptable.
- **No git operations in the notes location either.** Write files, nothing more.
- **Never record secrets.** Tokens, keys, passwords, `.env` contents, connection strings —
  even when they appear in a diff. Describe that a config value changed; never reproduce it.
- **Never invent.** If something can't be determined from git or context, ask or omit it. A
  journal with plausible fabrications is worse than a thin one, because it can't be trusted
  later and there's no way to tell which parts were real.

## Workflow

### 1. Resolve the documentation location

Read `config.json` from this skill's directory.

**If it's missing** (first run): derive the location. `git rev-parse --show-toplevel` gives
the repo root; its parent is the projects root. Propose `<parent>/daily-chore`, show the
absolute path, and ask for confirmation. On approval, write `config.json`. Never write it
without confirmation — a wrong path silently scatters entries somewhere they'll never be found.

**If `docsPath` is set but doesn't exist:** do not create it blindly and do not fall back
to another location. Say the configured path is missing, show it, and offer to re-derive.
This most often means the path was configured from a different shell — WSL sees
`/mnt/c/Users/...` where Git Bash sees `C:/Users/...`, same folder, different string.

Normalise backslashes to forward slashes when reading and writing config. Both work; mixed
ones don't.

### 2. Gather evidence

See [references/evidence-gathering.md](references/evidence-gathering.md). In short: working
tree state, the diff, and today's commits on the current branch. Prefer file and function
names over diff bodies.

### 3. Identify repo and task

**Repo name:** basename of the repo root. Sanitise for Windows — see the filename rules in
[references/duplicate-handling.md](references/duplicate-handling.md).

**Task name**, in priority order:

1. `$ARGUMENTS`, if given.
2. A ticket ID and description parsed from the branch (`feature/PAY-412-refunds` →
   `PAY-412 refunds`).
3. **Ask.** Do not infer a task name from the diff. Branches like `main`, `dev`, `master`,
   or `wip` carry no task identity, and a wrong task name silently splits one piece of work
   across two entries — the exact failure this design exists to prevent.

### 4. Check for duplicates

Read today's file for this repo if it exists. Compare task names **case-insensitively**
(Windows filesystems are case-insensitive; treating `PAY-412` and `pay-412` as different
produces a duplicate that looks like two tasks).

On a match, stop and offer three options — append a new session block, update the existing
section, or record as a separate task. Details in
[references/duplicate-handling.md](references/duplicate-handling.md).

### 5. Compose the entry

Use [assets/ENTRY_template.md](assets/ENTRY_template.md). Fixed sections: **Summary**,
**Changes**, **Next steps**. Add **Notes** only when there's a real technical decision,
discovery, or problem worth recording — not to fill space.

What makes this worth writing:

- **Why, not just what.** "Switched to a queue because the sync call timed out at 30s under
  load" is the sentence future-you needs. "Refactored the handler" is not.
- **Specifics from evidence.** File paths, function names, commit hashes, PR and issue links.
- **Decisions and their alternatives**, where visible.
- Not a transcript. Aim for something readable in thirty seconds.

Separate what was **done** from what was **discussed**. Committed and modified files are
done. Ideas from conversation are not, and shouldn't be written as if they were. When the
distinction is unclear for something significant, ask.

### 6. Multiple repositories

If the session touched several repos, write a separate entry in each repo's file
automatically. Don't ask, and don't combine them — a combined entry is unfindable when
searching for one project later.

### 7. Save

Path: `<docsPath>/daily-chore/YYYY-MM-DD/<repo>.md`. Create directories as needed.

**Append; never overwrite.** If the file exists, read it, add the new section, write it back
whole. Losing an earlier entry is the worst possible failure of this skill.

**When to show the entry before saving:** only if you guessed at something — asked for a
task name, was unsure whether work was complete, couldn't attribute a change. If everything
was determinable from evidence, save it and report the path.

Finish by printing the absolute path written to.

## Failure handling

- **Not a git repository:** ask for the project name and write an entry from session context
  alone, clearly noting there was no git evidence.
- **No changes found:** don't write an empty entry. Say nothing was detected and ask whether
  to record from session context.
- **Docs path unavailable:** fail loudly. Never silently write elsewhere.
- **Existing file is malformed:** don't repair it and don't overwrite. Append the new section
  and mention the file looks hand-edited.
