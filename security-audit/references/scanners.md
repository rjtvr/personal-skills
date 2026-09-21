# Scanners

Run what's installed. Don't block the audit on a missing tool — note which ran and which
didn't, since that determines what the audit could have found.

Check availability first:

```bash
for t in semgrep gitleaks trivy osv-scanner; do
  command -v "$t" >/dev/null && echo "$t: yes" || echo "$t: not installed"
done
```

## semgrep — code patterns (SAST)

```bash
semgrep --config=p/owasp-top-ten --config=p/secrets --json -o semgrep.json .
# language-specific packs stack on top:
semgrep --config=p/javascript --config=p/python --config=p/golang --json -o semgrep.json .
```

Good at: injection sinks, dangerous API usage, hardcoded crypto choices, unsafe
deserialization, framework-specific anti-patterns.

Blind to: anything defined by *missing* code. It cannot see that an authorization check
isn't there, because absence has no pattern.

False positives to expect: sinks reached only by literal or already-validated input; test
fixtures and mock data; example code in docs directories; rules matching a safe wrapper the
codebase uses consistently. Read the matched line before reporting it.

## gitleaks — secrets, including history

```bash
gitleaks detect --source . --report-format json --report-path gitleaks.json   # full history
gitleaks detect --source . --no-git --report-format json --report-path gl.json # working tree only
```

The history scan is the point. A secret deleted in a later commit is still in the objects
and still readable by anyone with the repo. See
[secrets-and-history.md](secrets-and-history.md) for what to do about a hit — the ordering
matters more than the detection.

False positives: example keys in docs, test fixtures, high-entropy strings that aren't
credentials (hashes, UUIDs, minified asset names, lockfile integrity hashes). Verify the
shape before escalating — but treat anything that looks live as live until proven otherwise.

## trivy / osv-scanner — dependency CVEs

```bash
trivy fs --scanners vuln,secret,misconfig --format json -o trivy.json .
trivy image --format json -o trivy-image.json <image>:<tag>
osv-scanner --format json --recursive . > osv.json
```

Trivy also covers IaC misconfiguration (Terraform, Kubernetes, Dockerfile) and container
layers, which makes it the broadest single tool here.

Ecosystem-native tools are worth running alongside — they sometimes know about advisories
the general scanners lag on:

```bash
npm audit --json > npm-audit.json
pip-audit --format json -o pip-audit.json
govulncheck -json ./... > govulncheck.json   # does real reachability analysis
bundle audit check --update
```

`govulncheck` deserves specific mention: it reports whether the vulnerable *function* is
actually reachable from your code, not just whether the module is present. That's exactly
the reachability question the risk rating needs, answered mechanically.

## Normalizing

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/normalize_findings.py \
  --semgrep semgrep.json --gitleaks gitleaks.json --trivy trivy.json \
  --format markdown
```

Merges into one deduplicated list keyed by file, line, and rule, and **redacts secret
values** to a fingerprint so they don't propagate into the report. Use `--format json` to
pipe onward.

## What scanners cannot do

Worth stating in the report so nobody reads a clean run as a clean bill of health:

- No scanner finds broken access control, because it's missing code.
- No scanner understands your business logic, so it can't see that a discount can be
  applied twice.
- Scanners don't know what data is sensitive in your domain.
- A clean scan means known patterns weren't matched. Nothing more.

The scanners exist to clear the mechanically-detectable ground cheaply, so the reasoning
pass in [reasoning-gaps.md](reasoning-gaps.md) can spend its attention where it's needed.
