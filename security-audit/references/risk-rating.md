# OWASP Risk Rating

**Risk = Likelihood × Impact.** Rate each axis Low / Medium / High, then combine.

The value is in forcing two separate questions — *how likely is this to be exploited* and
*what happens when it is* — rather than collapsing both into one gut-feel severity. A
scanner's severity label answers neither, because it knows nothing about the application.

## Severity matrix

| | Likelihood Low | Likelihood Medium | Likelihood High |
|---|---|---|---|
| **Impact High** | Medium | High | **Critical** |
| **Impact Medium** | Low | Medium | High |
| **Impact Low** | Note | Low | Medium |

## Rating each axis

The full methodology scores sixteen factors 0–9 and averages them. That's too heavy for
every finding. Rate Low/Medium/High holistically using the factors as prompts, and only
score formally when a rating is contested or the finding is consequential enough to argue
about. Where you do score: 0 to <3 is Low, 3 to <6 Medium, 6 to 9 High.

### Likelihood factors

*Threat agent* — **skill level** required to exploit, **motive** (what's the reward),
**opportunity** (what access is needed first), **size** of the group who could attempt it.

*Vulnerability* — **ease of discovery**, **ease of exploit**, **awareness** (is this a
well-known class with public tooling), **intrusion detection** (would you notice).

Practical anchors:

- **High** — unauthenticated, reachable from the internet, no special skill, public tooling
  exists. Most reflected XSS and unauthenticated injection sit here.
- **Medium** — needs a valid account, or knowledge of an internal identifier, or a
  non-obvious sequence of steps. Most IDOR sits here.
- **Low** — needs privileged access, a race window that's hard to hit, or a chain of other
  conditions first.

### Impact factors

*Technical* — loss of **confidentiality**, **integrity**, **availability**,
**accountability** (can the actor be traced).

*Business* — **financial damage**, **reputation damage**, **non-compliance**, **privacy
violation**.

Business impact outranks technical impact when they disagree, and it's the axis developers
under-rate. "Reads any user's email address" is technically modest and, under GDPR with a
large user base, a notifiable breach.

## Reachability gates the rating

Before rating anything High, trace a path from an attacker-controlled entry point to the
vulnerable code. A vulnerable function nobody can reach is latent, not exploitable.

State which it is. "Confirmed reachable via `POST /api/report`" and "vulnerable pattern
present, reachability not established" are different findings and must be rated differently.
When reachability is unknown, say so and rate conservatively rather than assuming either way.

## Inherited CVE scores

A dependency's CVSS is the score for *that library in general*, not for your application.
A 9.8 in a code path your app never calls is not a 9.8 for you.

Record both: the base score as published, and your own likelihood/impact given actual usage.
Where a tool reports reachability analysis, use it — and where it doesn't, check whether the
affected function is imported at all before escalating.

The inverse also holds. A Medium CVE in your authentication path can outrank a Critical one
in a build-time-only dev dependency.

## Common rating errors

- **Everything is Critical.** If most findings are Critical, the rating carries no
  information and the genuinely urgent item gets lost. Most findings are Medium.
- **Rating the class instead of the instance.** "SQL injection is Critical" — but *this*
  one is in an admin-only internal tool behind a VPN with parameterized queries everywhere
  else. Rate what's in front of you.
- **Ignoring compensating controls.** A WAF, network segmentation, or a strict CSP lowers
  likelihood. Note the control and that the underlying defect still needs fixing, since
  controls get removed.
- **Rating without threat context.** Impossible. Go back and ask what the app holds.
