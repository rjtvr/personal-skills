#!/usr/bin/env python3
"""Merge scanner output into one deduplicated findings list, with secrets redacted.

Usage:
    python3 normalize_findings.py --semgrep semgrep.json --gitleaks gitleaks.json \
        --trivy trivy.json --format markdown

Secret values from gitleaks are never emitted. They are reduced to a fingerprint
(first 4 chars, length, sha256 prefix) that identifies which credential was found
without reproducing it, because an audit report gets pasted, committed, and emailed.
"""

import argparse
import hashlib
import json
import pathlib
import sys

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "note": 4, "unknown": 5}


def load(path):
    if not path:
        return None
    p = pathlib.Path(path)
    if not p.exists():
        print(f"warning: {path} not found, skipping", file=sys.stderr)
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"warning: {path} is not valid JSON ({exc}), skipping", file=sys.stderr)
        return None


def fingerprint(secret):
    """Identify a secret without reproducing it."""
    if not secret:
        return "unavailable"
    digest = hashlib.sha256(secret.encode("utf-8")).hexdigest()[:12]
    head = secret[:4]
    return f"{head}\u2026 ({len(secret)} chars, sha256:{digest})"


def norm_severity(value):
    """Map tool-specific scales onto one scale so sorting is meaningful.

    semgrep reports ERROR/WARNING/INFO rather than critical/high/medium, so without
    this an ERROR-level injection finding sorts below a trivy MEDIUM.
    """
    sev = (value or "unknown").strip().lower()
    return {"error": "high", "warning": "medium", "info": "low"}.get(sev, sev)


def from_semgrep(data):
    out = []
    for r in (data or {}).get("results", []):
        extra = r.get("extra", {}) or {}
        meta = extra.get("metadata", {}) or {}
        cwe = meta.get("cwe")
        if isinstance(cwe, list):
            cwe = ", ".join(cwe)
        owasp = meta.get("owasp")
        if isinstance(owasp, list):
            owasp = ", ".join(owasp)
        out.append({
            "source": "semgrep",
            "rule": r.get("check_id", ""),
            "severity": norm_severity(extra.get("severity")),
            "file": r.get("path", ""),
            "line": (r.get("start", {}) or {}).get("line", 0),
            "message": (extra.get("message") or "").strip(),
            "cwe": cwe or "",
            "owasp": owasp or "",
        })
    return out


def from_gitleaks(data):
    """gitleaks emits a top-level array. Secret values are redacted here."""
    out = []
    for r in data or []:
        out.append({
            "source": "gitleaks",
            "rule": r.get("RuleID", ""),
            "severity": "high",  # a committed credential is high until triaged otherwise
            "file": r.get("File", ""),
            "line": r.get("StartLine", 0),
            "message": r.get("Description", "Potential secret"),
            "cwe": "CWE-798",
            "owasp": "A04:2025",
            "commit": (r.get("Commit") or "")[:8],
            "author": r.get("Author", ""),
            "date": r.get("Date", ""),
            "fingerprint": fingerprint(r.get("Secret") or r.get("Match")),
        })
    return out


def from_trivy(data):
    out = []
    for result in (data or {}).get("Results", []) or []:
        target = result.get("Target", "")
        for v in result.get("Vulnerabilities", []) or []:
            fixed = v.get("FixedVersion")
            out.append({
                "source": "trivy",
                "rule": v.get("VulnerabilityID", ""),
                "severity": norm_severity(v.get("Severity")),
                "file": target,
                "line": 0,
                "message": (
                    f"{v.get('PkgName', '?')} {v.get('InstalledVersion', '?')} — "
                    f"{v.get('Title') or v.get('VulnerabilityID', '')}"
                    + (f" (fixed in {fixed})" if fixed else " (no fix available)")
                ),
                "cwe": ", ".join(v.get("CweIDs", []) or []),
                "owasp": "A03:2025",
                "cvss": ((v.get("CVSS") or {}).get("nvd") or {}).get("V3Score", ""),
            })
        for m in result.get("Misconfigurations", []) or []:
            out.append({
                "source": "trivy",
                "rule": m.get("ID", ""),
                "severity": norm_severity(m.get("Severity")),
                "file": target,
                "line": ((m.get("CauseMetadata") or {}).get("StartLine") or 0),
                "message": m.get("Title", ""),
                "cwe": "",
                "owasp": "A02:2025",
            })
    return out


def dedupe(findings):
    """Same rule at the same location from the same tool is one finding."""
    seen, out = set(), []
    for f in findings:
        key = (f["source"], f["rule"], f["file"], f["line"])
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def render_markdown(findings, out):
    out.write("# Normalized scanner findings\n\n")
    if not findings:
        out.write("No findings from the tools provided.\n\n")
        out.write("> A clean scan means known patterns were not matched. ")
        out.write("It is not evidence that the application is secure.\n")
        return

    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    out.write("| Severity | Count |\n|---|---|\n")
    for sev in sorted(counts, key=lambda s: SEVERITY_ORDER.get(s, 9)):
        out.write(f"| {sev} | {counts[sev]} |\n")
    out.write("\n> Unfiltered tool output. Triage before reporting — ")
    out.write("SAST false-positive rates are high.\n\n")

    current = None
    for f in findings:
        if f["severity"] != current:
            current = f["severity"]
            out.write(f"\n## {current.upper()}\n\n")
        loc = f["file"] + (f":{f['line']}" if f["line"] else "")
        out.write(f"### {f['rule']}\n\n")
        out.write(f"- **Location:** `{loc}`\n")
        out.write(f"- **Tool:** {f['source']}\n")
        if f.get("cwe"):
            out.write(f"- **CWE:** {f['cwe']}\n")
        if f.get("owasp"):
            out.write(f"- **OWASP:** {f['owasp']}\n")
        if f.get("cvss"):
            out.write(f"- **CVSS (published):** {f['cvss']} — rate your own exposure separately\n")
        if f.get("fingerprint"):
            out.write(f"- **Secret fingerprint:** `{f['fingerprint']}` (value withheld)\n")
            if f.get("commit"):
                out.write(f"- **Introduced:** {f['commit']} {f.get('date', '')}\n")
            out.write("- **Action:** rotate first, then scrub history\n")
        out.write(f"- {f['message']}\n\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--semgrep")
    ap.add_argument("--gitleaks")
    ap.add_argument("--trivy")
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args()

    if not any([args.semgrep, args.gitleaks, args.trivy]):
        ap.error("provide at least one scanner report")

    findings = []
    findings += from_semgrep(load(args.semgrep))
    findings += from_gitleaks(load(args.gitleaks))
    findings += from_trivy(load(args.trivy))
    findings = dedupe(findings)
    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9), f["file"], f["line"]))

    try:
        if args.format == "json":
            json.dump(findings, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            render_markdown(findings, sys.stdout)
    except BrokenPipeError:
        return 0

    print(f"{len(findings)} finding(s) after dedupe", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
