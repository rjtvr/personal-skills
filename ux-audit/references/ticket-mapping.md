# Ticket mapping

Tickets are authored once in the neutral format (`assets/TICKET_template.md`) and mapped
into whichever tracker is in use. Author neutral, map late — writing directly in one
tracker's idioms means re-authoring when the team switches, and teams switch.

## Why frontmatter

The YAML block carries the fields trackers need as *structured data*; the markdown body
carries what humans need. That split is what makes mechanical import possible. Keep
tracker-specific concepts (Jira epics, Linear cycles) out of the frontmatter — express
them as neutral fields and resolve them at mapping time.

## Field mapping

| Neutral field | Jira | Linear | GitHub Issues |
|---|---|---|---|
| `id` | prefix in Summary, or a custom field | prefix in Title | prefix in Title |
| `title` | Summary | Title | Title |
| body | Description | Description (markdown) | Body (markdown) |
| `type` | Issue Type (Bug / Task) | label (no native type) | label |
| `priority` | Priority field | Priority (numeric, see below) | label `priority:p1` |
| `area` | Component, or label | label | label |
| `component` | Component | label or project | label |
| `files` | in Description | in Description | in Body |
| `criterion` | label + Description | label + Description | label + Body |
| `estimate` | Story Points | Estimate | Projects v2 number field |
| `blocked_by` | "is blocked by" link | Blocked-by relation | body reference / task list |
| `labels` | Labels | Labels | Labels |
| `reach` | label | label | label |

### Priority values

| Neutral | Jira | Linear | GitHub |
|---|---|---|---|
| P0 | Highest | 1 (Urgent) | `priority:p0` |
| P1 | High | 2 (High) | `priority:p1` |
| P2 | Medium | 3 (Normal) | `priority:p2` |
| P3 | Low | 4 (Low) | `priority:p3` |

Linear's numeric scale runs 0–4, where **0 means no priority, not highest** — a common and
silent mistake in scripted imports that quietly buries every ticket.

## Markdown compatibility

All three render markdown in issue bodies, and all three support task-list checkboxes, so
acceptance criteria survive the trip intact. Two caveats:

- Jira Cloud's REST API v3 expects **Atlassian Document Format** (JSON), not markdown. The
  CSV importer and the UI accept markdown-ish wiki markup. If importing via API v3, either
  convert to ADF or use CSV.
- Heading levels: keep bodies at `##` and below. A top-level `#` collides with the title in
  most renderings.

## Import routes

**GitHub** — one command per ticket, no intermediate format needed:

```bash
gh issue create \
  --title "[A-01] Search input has no programmatic label" \
  --body-file tickets/A-01.md \
  --label "a11y,priority:p1,bug"
```

Strip the frontmatter from `--body-file` first, or it renders as a literal block.

**Jira** — bulk CSV import (Settings → System → External System Import). One row per
ticket, header row matching Jira field names. Multiple labels go in *repeated columns of
the same name*, not a comma-joined cell.

**Linear** — CSV import, or the API. The API takes markdown descriptions directly, which
makes it the cleanest of the three for scripted creation.

`scripts/tickets_to_csv.py` converts a directory of neutral tickets into Jira- or
Linear-shaped CSV, and can emit `gh` commands for GitHub.

## Granularity

One ticket per *fix*, not per *finding*. Seventeen hardcoded greys across nine files is
one ticket that closes seventeen findings — that's what `closes_findings` is for. Splitting
it into seventeen tickets creates review overhead nobody wants and makes the board look
alarming without adding information.

Conversely, don't bundle unrelated fixes because they're both P2. A ticket should be one
coherent change with one verification step.
