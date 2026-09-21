# Duplicates, file naming, and append safety

## Path shape

```
<docsPath>/daily-chore/YYYY-MM-DD/<repo>.md
```

One file per repository per day. Each run appends a session section. The file is the
container; sections are the entries.

Dates are local time, `YYYY-MM-DD` — sortable, unambiguous, and immune to the
DD/MM vs MM/DD problem.

## Windows filename rules

The repo name becomes a filename, so it must be sanitised:

- **Illegal characters:** `< > : " / \ | ? *` — replace with `-`.
- **Reserved device names:** `CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`.
  These are reserved with *any* extension, so `aux.md` fails too. Prefix with `repo-` if a
  repo name collides.
- **No trailing dots or spaces** — Windows strips them silently, so `myrepo .md` and
  `myrepo.md` become the same file without warning.
- **Case-insensitive filesystem:** `MyApi.md` and `myapi.md` are the same file. Always
  compare existing filenames case-insensitively before deciding whether to create one.

Task names go inside the file, not in the path, so branch slashes (`feature/PAY-412`) are
harmless there. Sanitise them anyway if they ever reach a filename.

## Duplicate detection

Before writing, read today's file for this repo if it exists and compare the task name
against existing section headings, **case-insensitively and ignoring surrounding
punctuation**.

On a match, stop and present three options:

**1. Append a new session block** — the usual case. You worked on the same task again later
in the day. Preserves the earlier record and shows progression, which is often exactly what
you want to see later.

**2. Update the existing section** — the first entry was premature or wrong. Show what will
be replaced before doing it, and keep the original timestamp while noting it was revised.

**3. Record as a separate task** — the name collided but the work is genuinely different.
Disambiguate the heading rather than merging two unrelated things under one title.

Never pick one of these silently. This is the one moment where a wrong guess destroys
information the user can't recover, and there's no reliable signal for choosing correctly.

## Append safety

**Read the whole file, add the section, write it back whole.** Never truncate, never write
in place, never assume the file ends where you expect.

If the file doesn't parse as expected — frontmatter missing, headings hand-edited — do not
repair it and do not overwrite. Append the new section and mention that the file appears to
have been edited by hand. It's the user's journal; unexpected structure is more likely
deliberate than corrupt.

## File-level frontmatter

Frontmatter is per file, but tasks are per session, so keep file-level fields to what's
genuinely file-scoped and let each section carry its own:

```yaml
---
date: 2026-09-08
repo: my-api
tasks:
  - PAY-412 partial refunds
  - hotfix rate limiter
---
```

Append to `tasks` on each run. It gives you a greppable index of what a given day and repo
covered without reading the body. Per-session details — branch, status, time — live on the
section, since they can differ between sessions in the same file.
