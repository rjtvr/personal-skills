#!/usr/bin/env python3
"""Convert neutral markdown tickets into tracker-specific import formats.

Usage:
    python tickets_to_csv.py tickets/ --target jira   > jira-import.csv
    python tickets_to_csv.py tickets/ --target linear > linear-import.csv
    python tickets_to_csv.py tickets/ --target github > create-issues.sh

Reads every *.md in the directory, expecting YAML frontmatter as defined in
assets/TICKET_template.md. Uses PyYAML when available and falls back to a minimal
parser otherwise, so the script runs in a bare environment.
"""

import argparse
import csv
import pathlib
import re
import shlex
import sys

PRIORITY = {
    "P0": {"jira": "Highest", "linear": "1", "github": "priority:p0"},
    "P1": {"jira": "High", "linear": "2", "github": "priority:p1"},
    "P2": {"jira": "Medium", "linear": "3", "github": "priority:p2"},
    "P3": {"jira": "Low", "linear": "4", "github": "priority:p3"},
}


def split_frontmatter(text):
    """Return (frontmatter_string, body). Raises if no frontmatter block."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("no YAML frontmatter found")
    return match.group(1), match.group(2).strip()


def parse_frontmatter(raw):
    try:
        import yaml

        return yaml.safe_load(raw) or {}
    except ImportError:
        pass

    # Minimal fallback: scalars, inline lists, and dash lists. Enough for this schema.
    def strip_comment(value):
        """Drop a trailing ' # ...' comment unless it sits inside quotes."""
        if value.startswith(('"', "'")):
            return value
        return re.split(r"\s+#", value, maxsplit=1)[0].strip()

    data, current_key = {}, None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and line.lstrip().startswith("- "):
            if current_key:
                item = strip_comment(line.lstrip()[2:].strip())
                data.setdefault(current_key, []).append(item.strip("\"'"))
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), strip_comment(value.strip())
        current_key = key
        if not value:
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()]
        else:
            data[key] = value.strip("\"'")
    return data


def load_tickets(directory):
    tickets = []
    for path in sorted(pathlib.Path(directory).glob("*.md")):
        try:
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError:
            print(f"skipping {path.name}: no frontmatter", file=sys.stderr)
            continue
        meta = parse_frontmatter(fm)
        meta["_body"] = body
        meta["_path"] = path
        tickets.append(meta)
    return tickets


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def full_title(t):
    return f"[{t.get('id', '?')}] {t.get('title', 'Untitled')}"


def labels_for(t, target):
    labels = as_list(t.get("labels"))
    for key in ("area", "type", "reach"):
        if t.get(key):
            labels.append(str(t[key]))
    if target == "github":
        priority = PRIORITY.get(str(t.get("priority", "")), {})
        if priority:
            labels.append(priority["github"])
    # de-duplicate, preserve order
    seen, out = set(), []
    for label in labels:
        if label and label not in seen:
            seen.add(label)
            out.append(label)
    return out


def emit_jira(tickets, out):
    max_labels = max((len(labels_for(t, "jira")) for t in tickets), default=0)
    header = ["Summary", "Issue Type", "Priority", "Description", "Component"]
    header += ["Labels"] * max_labels
    writer = csv.writer(out)
    writer.writerow(header)
    for t in tickets:
        issue_type = "Bug" if str(t.get("type", "")).lower() == "bug" else "Task"
        priority = PRIORITY.get(str(t.get("priority", "")), {}).get("jira", "Medium")
        labels = labels_for(t, "jira")
        row = [
            full_title(t),
            issue_type,
            priority,
            t["_body"],
            t.get("component", ""),
        ]
        row += labels + [""] * (max_labels - len(labels))
        writer.writerow(row)


def emit_linear(tickets, out):
    writer = csv.writer(out)
    writer.writerow(["Title", "Description", "Priority", "Labels", "Estimate"])
    for t in tickets:
        writer.writerow([
            full_title(t),
            t["_body"],
            PRIORITY.get(str(t.get("priority", "")), {}).get("linear", "3"),
            ",".join(labels_for(t, "linear")),
            t.get("estimate", ""),
        ])


def emit_github(tickets, out):
    out.write("#!/usr/bin/env bash\nset -euo pipefail\n\n")
    out.write("# Review before running. Labels must already exist in the repo,\n")
    out.write("# or add --label creation beforehand via `gh label create`.\n\n")
    for t in tickets:
        body_file = f"/tmp/{t.get('id', 'ticket')}.body.md"
        out.write(f"cat > {body_file} <<'TICKET_EOF'\n{t['_body']}\nTICKET_EOF\n")
        labels = ",".join(labels_for(t, "github"))
        out.write(
            "gh issue create "
            f"--title {shlex.quote(full_title(t))} "
            f"--body-file {body_file}"
        )
        if labels:
            out.write(f" --label {shlex.quote(labels)}")
        out.write("\n\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="directory of neutral ticket .md files")
    parser.add_argument(
        "--target", required=True, choices=["jira", "linear", "github"]
    )
    args = parser.parse_args()

    tickets = load_tickets(args.directory)
    if not tickets:
        print("no tickets found", file=sys.stderr)
        return 1

    try:
        {"jira": emit_jira, "linear": emit_linear, "github": emit_github}[args.target](
            tickets, sys.stdout
        )
    except BrokenPipeError:
        # Downstream closed the pipe (e.g. `| head`) — not an error worth a traceback.
        return 0
    print(f"wrote {len(tickets)} ticket(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
