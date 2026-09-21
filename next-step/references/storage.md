# Storage

Two environments, one file format. The user can move between them freely because the files
are identical.

## Layout

```
<notesPath>/
├── MASTER_ROADMAP.md
└── sessions/
    ├── 2026-09-22-career-learning.md
    └── 2026-10-10-checkin-money.md
```

- **`MASTER_ROADMAP.md`** — the current plan across all areas. Updated every session. Kept
  short — roughly a screen per area.
- **`sessions/`** — one note per session, never edited after it's written. The history of
  how the plan evolved and why.

Session filename: `YYYY-MM-DD-<type-or-areas>.md`. Sortable, readable at a glance.

## Claude Code

**Config:** `config.json` in the skill folder, created on first run:

```json
{ "notesPath": "C:/Users/you/life-roadmap" }
```

**First run:** propose a location in the user's home folder (for example
`~/life-roadmap`), show the absolute path, and write `config.json` only after the user
confirms. Never propose a path inside a code repository.

**Reading:** load `MASTER_ROADMAP.md` and the most recent session note at the start.

**Writing:** show the session note and the master roadmap changes, get approval, then write.
Read-modify-write the master roadmap whole; never truncate. Session notes are new files,
never overwrites. If a session note for today with the same name exists, add a suffix
rather than replacing it.

**Optional journal link:** if `journalPath` is set in config — for example a `daily-chore`
folder from a work journal — skim recent entries during check-ins for what the user
actually spent time on. Useful evidence against a stated plan. Read-only, and only when
configured.

## claude.ai

There is no persistent folder between chats, so the user carries the memory.

**At the start:** ask the user to attach their latest `MASTER_ROADMAP.md`, or confirm this
is a first session. If they have past session notes, the most recent one helps too, but the
master roadmap is enough.

**At the end:** create the session note and the updated master roadmap as files and present
them for download. Tell the user plainly: these files are the memory — keep them somewhere
safe and attach the master roadmap next time.

Never claim the skill will remember next time. In claude.ai, it won't, unless the user brings
the file back.

## Privacy

This material is personal — health, money, relationships. Treat it that way:

- Show what will be saved and let the user edit or remove anything before writing.
- Never write notes into a code repository, which may be pushed somewhere public.
- Save only what the roadmap needs. Detailed personal disclosures from the interview don't
  need to be transcribed into the session note; the conclusions do.
