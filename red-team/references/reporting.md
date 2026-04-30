# Reporting — Severity Scoring + Writeup Template

Phase 7. Loaded when packaging findings into a report or PR comments.

## Severity Models

Pick one. Be consistent within a report.

### DREAD-lite (fast)

| Dimension | Question | 1 | 3 | 5 |
|-----------|----------|---|---|---|
| **D**amage | Worst-case impact | minor info leak | data tampering / partial RCE | full RCE / mass data theft |
| **R**eproducibility | Reliability | rare conditions | sometimes | always |
| **E**xploitability | Difficulty | expert + custom tooling | scripted / public exploit | one-line curl / nmap |
| **A**ffected | Blast radius | one user | tenant / segment | all users / cross-tenant |
| **D**iscoverability | Visibility | source-only | internal logs / error msgs | externally observable |

| Sum | Severity |
|-----|----------|
| 5-12 | Low |
| 13-19 | Medium |
| 20-25 | High |
| 23-25 with full chain | Critical |

### CVSS v3 (industry-standard)

Use the [FIRST CVSS calculator](https://www.first.org/cvss/calculator/3.1).

Base metrics:
- Attack Vector: Network / Adjacent / Local / Physical
- Attack Complexity: Low / High
- Privileges Required: None / Low / High
- User Interaction: None / Required
- Scope: Unchanged / Changed
- Confidentiality / Integrity / Availability impact: None / Low / High

Severity bands (base score):
- 0.1-3.9 Low
- 4.0-6.9 Medium
- 7.0-8.9 High
- 9.0-10.0 Critical

CVSS is preferred for external advisories / CVE assignment. DREAD-lite is fine for internal triage.

## Per-Finding Template

```markdown
## [SEV] Title (CWE-XXX, OWASP A0X:2021)

**Severity**: <Critical/High/Medium/Low> — <CVSS 3.1: 9.8> or <DREAD: 22/25>
**Status**: Open / Confirmed / Fix-pending / Fixed
**Asset affected**: [data store / service / identity]
**Reporter**: [name / "internal red-team review"]
**Discovered**: YYYY-MM-DD

---

### Summary
[One paragraph: what's wrong, why it matters.]

### Affected Code
- Entry point: `path/file.ts:L23` (e.g. POST /api/run)
- Sink: `path/file.ts:L88` (e.g. exec(...))
- Path:
  1. `file.ts:L23` — req.body.cmd captured
  2. `processor.ts:L14` — passed unchanged
  3. `worker.ts:L88` — exec(input) invokes shell

### Exploit Chain (Lockheed)
| Stage | Action | MITRE |
|-------|--------|-------|
| Recon | discover endpoint via JS bundle | T1595 |
| Delivery | POST malicious cmd | T1190 |
| Exploit | shell injection → RCE | T1059 |
| Persist | install web shell | T1505.003 |
| Exfil | data over C2 | T1041 |

### Proof (Defensive)
Minimal payload demonstrating the issue. **Do not include weaponized code.**

```http
POST /api/run HTTP/1.1
Content-Type: application/json

{"cmd": "id"}
```

Expected (if vulnerable): response contains output of `id`.

### Root Cause
[The actual flaw. Not "we forgot to validate" — *why* validation was bypassed.]

E.g.: "child_process.exec invokes a shell. Any string argument is interpolated into the shell, allowing metacharacters to chain commands. The handler accepts arbitrary strings and passes them through."

### Remediation

**Primary fix** (preferred — diff snippet):

```diff
- import { exec } from 'child_process'
- exec(req.body.cmd, (err, stdout) => res.send(stdout))
+ import { execFile } from 'child_process'
+ const ALLOWED = new Set(['ls', 'pwd', 'date'])
+ const { cmd, args = [] } = req.body
+ if (!ALLOWED.has(cmd)) return res.status(400).send('disallowed')
+ execFile(cmd, args, (err, stdout) => res.send(stdout))
```

**Defense in depth**:
- Run worker as low-priv user.
- Audit log every command + caller identity.
- Rate limit + alert on anomaly.

**If fix not feasible**:
- Compensating control: WAF rule blocking shell metacharacters in body.
- Sunset timeline: this is a temporary mitigation, not a fix.

### Verification

**Regression test** (add to test suite):
```ts
test('rejects disallowed command', async () => {
  const r = await request(app).post('/api/run').send({ cmd: 'rm -rf /' })
  expect(r.status).toBe(400)
})

test('rejects shell metacharacters in args', async () => {
  const r = await request(app).post('/api/run').send({ cmd: 'ls', args: ['; whoami'] })
  // execFile passes args[] verbatim — metachars are not interpreted
  expect(r.status).not.toBe(500)
})
```

**Manual verification**:
- Deploy fix to staging.
- Re-run the proof from above. Expect 400 / sanitized response.
- Confirm regression test runs in CI.

### Detection (post-fix)

For SOC / observability:
- Alert on: 4xx spikes on /api/run.
- Log: caller identity + command + args, durably.
- Dashboard: top callers, top commands, error rate.

### Disclosure

- **Internal**: filed in <tracker> ticket #XXX, owner @user.
- **Coordinated** (if open-source / vendor): <SECURITY.md contact>, embargo until fix released.
- **Public**: after fix lands + N-day window. CVE if applicable.

### References
- CWE-78: https://cwe.mitre.org/data/definitions/78.html
- OWASP A03:2021: https://owasp.org/Top10/A03_2021-Injection/
- Internal: <link to threat model / DFD>
```

## Aggregate Report Template

For multi-finding engagements:

```markdown
# Red-Team Report: [System / Engagement]

**Engagement**: [name]
**Period**: YYYY-MM-DD → YYYY-MM-DD
**Reviewer**: [name / "internal red-team review"]
**Authorization**: [scope reference]

## Executive Summary

[3-5 sentences: posture, top risks, recommended priority. No jargon.]

| Severity | Count | Top Examples |
|----------|-------|--------------|
| Critical | X | command injection in /api/run |
| High | Y | broken access control on admin |
| Medium | Z | weak password policy |
| Low | W | verbose error messages |

## Scope

- **In scope**: [list]
- **Out of scope**: [list]
- **Method**: code review, no live probes / static analysis only / etc.

## Findings (Ranked)

| ID | Severity | Title | CWE | Status |
|----|----------|-------|-----|--------|
| F01 | Critical | Command injection in /api/run | CWE-78 | Open |
| F02 | High | Missing authz on /admin/users | CWE-862 | Open |
| ...

[Detailed writeups follow per the per-finding template]

## Top Recommendations (Across Findings)

1. [Highest-leverage change — e.g. "introduce a centralized auth middleware"]
2. [Second — e.g. "add WAF + rate-limit on all mutating endpoints"]
3. [Third]

## Threat Model Snapshot

[Brief: assets, top STRIDE risks, mitigations status]

## Compliance Notes

[Only if requested. SOC2 / ISO27001 / PCI controls touched by findings.]

## Appendix

- Tooling versions (semgrep X.Y, gitleaks X.Y, ...)
- Files reviewed
- Commits in scope
- Out-of-scope items deferred
```

## Severity Anti-Patterns

| Mistake | Why it's wrong | Fix |
|---------|----------------|-----|
| Score by CVE base alone | Ignores *your* deployment context | Adjust for reachability + impact in your system |
| Score "theoretical" High | If unreachable, it's not High *here* | Score by chain that actually fires |
| Ignore chain | A "Medium" in a chain ending in RCE is part of a Critical | Score the chain, not the bug |
| No remediation per finding | Findings without fixes don't ship | Every finding gets remediation |
| No regression test | Fix can decay silently | Test fails before fix, passes after |
| Public disclosure before fix | Helps attackers | Coordinate disclosure |

## Communication Tone

- **Direct, factual, no drama.** Vulns aren't moral failings.
- **Evidence-first.** file:line + observable behavior.
- **Action-oriented.** Each finding ends in a concrete fix.
- **Respect the team.** They wrote the code; they will write the fix. Findings are a tool, not a verdict.
