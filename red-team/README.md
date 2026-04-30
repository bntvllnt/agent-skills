# Red Team — Adversarial Code Review

Find vulnerabilities in your own codebase by adopting an attacker's mindset. **The best defence is attack.**

## What This Does

Reverses the polarity of code review. Stops asking *"is this code safe?"* and starts asking *"how would I break this?"*. Combines:

- **STRIDE** threat modeling per asset
- **OWASP Top 10 / CWE Top 25** classification
- **Attack-surface enumeration** — entry points → trust boundaries → sinks
- **Lockheed kill chain + MITRE ATT&CK** for exploit-chain reasoning
- **DREAD / CVSS** severity scoring
- **Defensive-disclosure** report format with proof + remediation + regression test

## Authorized Use Only

This skill is **defensive**. It works against:

- Code in your working directory
- Systems for which you have explicit written authorization to test (CTF, owned infra, signed pentest scope)

It refuses operations against unauthorized third-party systems. Phase 0 (scope) is blocking.

## When To Use

| Situation | Mode |
|-----------|------|
| New auth / payment / external-input feature | Threat model |
| Existing codebase, posture unknown | Attack-surface map |
| Specific file / endpoint / function | Code-level red team |
| Pre-merge / pre-release gate | Full 7-phase pass |
| Post-incident triage | Indicator hunt |

## Entry Points

| Say | Action |
|-----|--------|
| "red team this code" | Run 7-phase protocol |
| "threat model [X]" | STRIDE + Shostack 4 questions |
| "attack surface of [repo]" | Enumerate entry → sink paths |
| "find vulnerabilities in [file]" | Adversarial code review |
| "exploit chain from [X] to [Y]" | Kill-chain walk |
| "severity of [finding]" | DREAD / CVSS scoring |
| "report [findings]" | Writeup with remediation + tests |

## The 7 Phases

```
0. SCOPE        Confirm authorization (BLOCKING)
1. RECON        Map languages, frameworks, deps, deploy
2. ENUM         Entry points + trust boundaries + sinks
3. THREAT       STRIDE per asset + OWASP/CWE mapping
4. VULN HUNT    Adversarial search per threat
5. EXPLOIT      Chain bugs into kill-chain stages
6. IMPACT       Score with DREAD or CVSS
7. REPORT       Severity-ranked findings + fix + regression test
```

## Files

- `SKILL.md` — frontmatter, router, phases, anti-patterns
- `references/scope-and-authorization.md` — Phase 0 + refusal triggers
- `references/threat-modeling.md` — STRIDE, Shostack 4 questions, DFD
- `references/attack-surface.md` — entry / boundary / sink + taint tracing
- `references/code-review-protocol.md` — 7-phase walkthrough with adversarial questions
- `references/kill-chain.md` — Lockheed + MITRE ATT&CK
- `references/owasp-cwe.md` — Top 10 / Top 25 with code patterns
- `references/secret-hunting.md` — secrets in code, history, logs
- `references/supply-chain.md` — dep audit, lockfile, typo-squat
- `references/reporting.md` — severity + writeup template

## Optional CLI Helpers

If installed locally, the skill will use them in recon. If not, it falls back to manual `Grep` + `Read`:

- `semgrep` — SAST patterns
- `gitleaks` / `trufflehog` — secret scanning
- `npm audit` / `pnpm audit` / `pip-audit` / `osv-scanner` — dep CVEs
- `snyk` — dep + container

## License

MIT
