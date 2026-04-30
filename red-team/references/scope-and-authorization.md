# Phase 0 — Scope & Authorization (BLOCKING)

This skill performs adversarial reasoning against code. That power is only safe when scoped to systems the user has authorization to test. Phase 0 is a hard gate.

## The 4 Scope Questions

Before any recon:

```
1. WHAT codebase / system / endpoint?
   - Path, repo, URL — be specific.

2. WHO authorized this review?
   - "I own it" (working dir, personal repo, employer's repo with employment scope)
   - "Written pentest scope" (engagement agreement covers it)
   - "CTF / training" (boxes designed for this)
   - "Public bug bounty" (program rules cover it)

3. WHAT is OUT of scope?
   - Third-party services (payment processors, identity providers, cloud APIs)
   - Customer data in production
   - Vendor systems
   - Anything not in (2)

4. WHAT artifact?
   - Threat model document
   - Vuln list with severities
   - PR comments / inline findings
   - Internal writeup
```

If any of (1)-(3) is ambiguous, **stop and ask**. Do not proceed with assumed scope.

## Authorization Matrix

| Target | Default verdict | Required confirmation |
|--------|-----------------|------------------------|
| Working directory the user opened | OK | none |
| Personal GitHub repo, public | OK | none |
| Personal GitHub repo, private | OK if user provides it | none |
| Employer's repo, user is employee | OK | one-line confirmation |
| Customer's codebase via consulting | OK | engagement scope referenced |
| Open-source project, third-party | OK for read-only review | only public-facing analysis; coordinated disclosure |
| Random GitHub repo, no relation | **Refuse** | n/a |
| Live production endpoint, owned | OK for non-destructive | rate limits + auth context |
| Live production endpoint, third-party | **Refuse** | n/a unless bug-bounty scope |
| Customer prod data | **Refuse** | even with code access |

## Refusal Triggers (HARD)

The skill **stops and refuses** when:

- Target is a third-party service the user does not own and has not been authorized to test.
- Goal is to remain undetected on a system the user does not own.
- Request is for an exploit payload tailored to a named external target.
- Request is for credential-stuffing / brute-force / DoS infrastructure.
- Request involves customer or third-party PII without sanitization.

Refusal text template:

```
I can't help with that as stated. The skill is defensive — for code you own
or have written authorization to test. If you're working on:
- Your own code → share the path/repo and I'll proceed.
- A pentest engagement → confirm scope and I'll work within it.
- A bug-bounty target → confirm program + scope and I'll work within it.
- A CTF box → confirm and I'll proceed.
Otherwise I'd need scope clarification before continuing.
```

## Soft Pause Triggers

The skill **pauses and asks** (does not refuse) when:

- Scope is plausible but not stated.
- The chain crosses a trust boundary the user might not own (e.g. their app calls a third-party API — the third-party is out of scope).
- A finding would be destructive to verify in a live environment.

In these cases, ask once, get clarification, and proceed within the clarified scope.

## Recording Scope

For non-trivial engagements, record at the top of the report:

```markdown
## Scope

- **Target**: <repo / system>
- **Authorization**: <how user is authorized — owns / engagement / bounty / CTF>
- **In scope**: <list>
- **Out of scope**: <list>
- **Test type**: code review / static analysis only / no live probes
- **Disclosure**: private writeup / PR comments / coordinated disclosure
```

This is a contract with future-you and the user — and a guard against scope creep.

## Coordinated Disclosure

When findings affect software with users / customers:

1. Do **not** post the finding publicly (issues, PRs, chat) until fixed.
2. Use the project's `SECURITY.md` reporting channel if it exists.
3. Apply embargo until a fix lands + a release window has passed.
4. After disclosure, the report can be made public (CVE, advisory).

This skill defaults to private writeup. Public disclosure is an explicit user decision, not the skill's.

## Anti-Patterns (NEVER)

- NEVER assume scope. Confirm in writing (chat counts).
- NEVER proceed when the chain crosses out-of-scope. Stop, report the boundary, get clarification.
- NEVER write exploit payloads aimed at named live targets the user does not own.
- NEVER help bypass detection of a system the user does not own.
- NEVER include real customer data, real tokens, or real credentials in findings — sanitize or use placeholders.
