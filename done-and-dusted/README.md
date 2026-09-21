# done-and-dusted

A manually-triggered Claude Code skill that writes a work-journal entry for the task you
just finished, into a central folder outside your repositories.

```
/done-and-dusted
/done-and-dusted refactored the auth middleware
/dnd
```

---

## What's in this plugin

```
done-and-dusted/
├── .claude-plugin/plugin.json
├── SKILL.md
├── config.example.json
├── references/
├── assets/
├── commands/dnd.md      → optional alias, autocompletes to /done-and-dusted
├── README.md
└── ENHANCEMENTS.md
```

## Install

From this repo's marketplace (see the root [README](../README.md)):

```
/plugin marketplace add rjtvr/personal-skills
/plugin install done-and-dusted@personal-skills
```

Restart is only needed if `~/.claude/skills` didn't already exist when the session started.

### Verify

Type `/done` in a session — it should autocomplete to `/done-and-dusted`.

### First run configures itself

There's no config file to write by hand. On first run the skill takes your current repo,
goes up one level to find your projects root, proposes `<that>/daily-chore`, and shows you
the absolute path. Approve it and it writes `config.json`. That's the whole setup.

If you'd rather set it manually, copy `config.example.json` to `config.json` in the
installed plugin folder and edit `docsPath`.

---

## How it stores things

```
<your-projects-folder>/
├── daily-chore/
│   └── 2026-09-08/
│       ├── my-api.md
│       └── admin-dashboard.md
├── my-api/
└── admin-dashboard/
```

One file per repository per day. Running it again the same day appends a new section rather
than replacing anything.

---

## Behaviour worth knowing

**It asks for a task name when your branch doesn't carry one.** On `main` or `dev` there's
nothing to parse, and guessing would silently split one piece of work across two entries.
Skip the question by passing the name: `/done-and-dusted fixing the rate limiter`.

**It only shows you the entry when it had to guess.** Clean runs save silently and print the
path.

**It never touches your repo.** Read-only git commands only — no staging, committing, or
editing. It doesn't run git in your notes folder either.

**It won't record secrets.** Values from `.env`, keys, and tokens are described, never
reproduced, even when they appear in a diff.

**Multiple repos in one session get separate entries**, automatically, one per repo.

---

## Configuration

`config.json` in the installed plugin folder:

```json
{
  "docsPath": "C:/Users/you/projects",
  "excludeRepos": [],
  "timeFormat": "24h",
  "remoteHostMap": {
    "github-work": "github.com",
    "github-personal": "github.com"
  },
  "accountLabels": {
    "github-work": "work",
    "github-personal": "personal"
  }
}
```

`accountLabels` is optional. With two GitHub accounts it tags each entry `account: work` or
`account: personal` in frontmatter, so one journal stays filterable. Resolved from the SSH
host alias, falling back to `git config user.email`; if neither resolves, the field is
omitted rather than guessed. Leave `accountLabels` out entirely to skip tagging.

`remoteHostMap` is only needed if you use SSH host aliases for multiple keys. If your remote
looks like `git@github-work:acme/my-api.git`, map the alias to the real host so PR and issue
links resolve. Without it the skill records the reference without a URL rather than emitting
a broken one.

No SSH key is ever needed to run the skill — every git command it uses is local and
read-only, so nothing authenticates.

Forward slashes work on Windows and avoid JSON's backslash-escaping problem — `C:\Users`
is invalid JSON unless written `C:\\Users`.

`config.json` is never included in the package, so reinstalling the plugin won't overwrite
your settings. `config.example.json` is the shipped copy.

---

## Troubleshooting

**`/done-and-dusted` doesn't appear** — check the plugin's `SKILL.md` is installed, run
`claude plugin validate`, restart once.

**"Configured path doesn't exist"** — usually a shell mismatch. WSL sees your drive as
`/mnt/c/Users/...`, Git Bash sees `C:/Users/...`. Same folder, different string. The skill
offers to re-derive; accept, or edit `docsPath` to match the shell you actually use.

**It asks for a task name every time** — your branches don't contain ticket IDs. Either pass
the name as an argument, or adopt branch names like `feature/PAY-412-refunds`.

**Entries feel thin** — it's likely running late in a long session, after early work has been
compacted out of context. Git evidence survives, conversational detail doesn't. Run it closer
to finishing a piece of work.

**PR links point at a host that doesn't exist** — you're using SSH host aliases. Add
`remoteHostMap` to `config.json` mapping the alias to the real forge host.

**Nothing was detected** — expected if all work was committed and pushed on a previous day,
since it looks at the working tree and today's commits.

---

## Uninstall

```
/plugin uninstall done-and-dusted@personal-skills
```

Your `daily-chore` folder is untouched.
