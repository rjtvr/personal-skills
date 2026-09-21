# Evidence gathering

Git is the primary evidence. Session context is supporting colour, not the source of record.

This matters because the context window may not hold the whole session — on a long one,
early work may already have been compacted away. Git state is still there regardless, so
anchor the entry to it and use conversation memory to explain the *why* behind what git shows.

## Commands

All read-only. These are the only ones permitted.

```bash
git rev-parse --show-toplevel          # repo root → repo name, and parent → projects root
git rev-parse --abbrev-ref HEAD        # current branch → task identity
git status --porcelain                 # changed files, machine-readable
git diff --stat                        # scale of change per file
git diff                               # uncommitted detail
git diff --cached                      # staged detail
git log --since=midnight --oneline     # today's commits
git log --since=midnight --stat        # what those commits touched
git remote get-url origin              # for building PR/issue links
```

`--porcelain` and `--oneline` are chosen for stable parsing. Plain `git status` output is
formatted for humans and changes between versions.

## Reading the diff

Read the diff to understand the change; don't reproduce it. The entry records what changed
and why, not the patch — the patch is already in git, and duplicating it makes the journal
unreadable.

Extract: files touched, functions or components added or changed, dependencies added or
removed, config or schema changes, tests added.

Skip: formatting-only changes, lockfile churn, generated files, vendored directories. These
inflate `--stat` and mean nothing later.

## Secrets — do not copy through

Diffs routinely contain credentials. Never reproduce a value from `.env`, `*.pem`, `*.key`,
`secrets.*`, or any line matching an assignment to something named like `token`, `secret`,
`password`, `api_key`, or `connection_string`.

Write "added `STRIPE_WEBHOOK_SECRET` to the environment config" — never the value. A journal
file is synced, backed up, and possibly in a cloud folder; a secret written there has been
leaked to every one of those places.

## Commits from today

`--since=midnight` uses local time, which is what you want — it matches the date the entry
is filed under.

Two caveats worth handling rather than getting wrong:

- **Commits authored by someone else** may appear after a pull or merge. Filter with
  `--author="$(git config user.email)"` when the branch is shared.
- **Work spanning midnight** is filed under today by `--since=midnight`, so a late-night
  session gets split across two dates. If the branch's commits start before midnight, ask
  whether to file everything under one date rather than deciding silently.

## Links and references

Build from `git remote get-url origin`. This reads `.git/config` locally — no network, no
SSH key, nothing to authenticate. It works identically regardless of how many keys are
configured.

### SSH host aliases

Multiple SSH keys are normally handled with host aliases in `~/.ssh/config`:

```
Host github-work
  HostName github.com
  IdentityFile ~/.ssh/id_work
```

The remote then reads `git@github-work:acme/my-api.git`, and naive parsing produces
`https://github-work/acme/my-api/...` — a dead link.

Resolve it before building any URL:

1. Check `remoteHostMap` in `config.json` for an explicit alias → host mapping.
2. Failing that, resolve via `git config --get-regexp '^url\.'` for any `insteadOf` rewrites.
3. Failing that, if the host isn't a recognised forge (`github.com`, `gitlab.com`,
   `bitbucket.org`, or a host containing them), **record the reference without a URL**.

Never emit a URL built on an unresolved host. A dead link in a journal is worse than a bare
reference, because it gets clicked once, months later, before the reader realises it was
never valid.

`~/.ssh/config` is not read directly — it's outside the repo and outside the skill's remit.
`remoteHostMap` exists so the mapping is stated explicitly rather than inferred from a file
the skill has no business opening.

### Account label

When `accountLabels` is set in config, tag the entry with which account the repo belongs to.
Resolve in this order:

1. **SSH host alias** from the remote URL, looked up in `accountLabels`. Most reliable —
   the alias exists precisely to distinguish accounts.
2. **`git config user.email`**, if its domain matches a label unambiguously.
3. **Omit the tag.** Never guess. A repo mislabelled `work` when it's personal is worse
   than an untagged one, because it's wrong in a way you won't notice while scanning.

The label is file-scoped, not session-scoped — a repository belongs to one account — so it
goes in file frontmatter where it can be grepped without reading bodies.

If `accountLabels` is absent from config, skip this entirely and emit no `account` field.

### What to capture

- **PR links:** only when a PR number appears in commit messages or branch metadata, and the
  host resolved. Never guess a number.
- **Issue and ticket references:** parse `PAY-412`, `#1234`, `GH-99` from branch name and
  commit messages. Record the reference even when no URL can be built.
- **Commit hashes:** short form (7 chars) — enough, and readable.
- **File paths:** relative to repo root, so they mean something on another machine.

## Distinguishing done from discussed

- **Done:** committed, staged, or modified in the working tree. Verifiable.
- **In progress:** modified but incomplete — say so rather than implying completion.
- **Discussed only:** raised in conversation with no corresponding change. Belongs under
  **Next steps** or **Notes**, never under **Changes**.

When something significant is ambiguous, ask. This is the one place where a wrong guess
makes the journal actively misleading — a future reader has no way to tell that "added
retry logic" was actually just an idea.
