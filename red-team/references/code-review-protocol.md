# Code-Review Protocol — Adversarial Walkthrough

The 7-phase protocol expanded with concrete questions, file:line evidence requirements, and stop conditions per phase.

## Mindset

Reverse every defensive question:

```
DEFENSIVE                          ADVERSARIAL
─────────                          ───────────
"Is this validated?"               "What input bypasses this validator?"
"Is auth checked?"                 "What path skips this check?"
"Is the query safe?"               "Where does user input meet a query?"
"Is this encrypted?"               "Where is the unencrypted copy?"
"Is the secret stored safely?"     "Where in the repo / history / logs is it?"
"Is the dep up to date?"           "What CVE applies to this version?"
"Did the test pass?"               "What test would have caught this?"
```

The adversarial form is what produces findings.

## Phase 1 — Recon (Detail)

Goal: build a structural map. **No live probes.**

### Questions to answer

- What languages? (`Glob: "**/*.{ts,js,py,go,rb,java,rs}"`)
- What frameworks? (`Read: package.json, pyproject.toml, go.mod, Gemfile`)
- What deploys? (`Glob: "Dockerfile, **/k8s/**, .github/workflows/**, terraform/**"`)
- What auth? (`Grep: "auth, session, jwt, oauth, saml"`)
- What data? (`Grep: "schema.prisma, *.sql, models/**"`)
- What secrets are referenced? (`Grep: "process.env\\.[A-Z_]+"`)

### Stop condition

A one-page recon brief exists. If not, do not proceed to enumeration.

## Phase 2 — Enumerate (Detail)

Goal: produce the entry-point / trust-boundary / sink graph from `attack-surface.md`.

### Questions

- For each entry point: who can call it? (auth required?)
- For each boundary: what control protects it?
- For each sink: what data feeds it?
- Which entries reach which sinks?

### Stop condition

A list of (entry, sink, path) candidates exists. If empty, recon was incomplete.

## Phase 3 — Threat Model (Detail)

Goal: STRIDE per asset → ranked threats. See `threat-modeling.md`.

### Stop condition

For each asset, every STRIDE row is filled with either a mitigation or a "no — investigate in Phase 4" entry.

## Phase 4 — Vuln Hunt (Detail)

Per (entry, sink, path) candidate from Phase 2 + per "investigate" item from Phase 3, perform adversarial review.

### Per-finding template

For each suspicious code path:

```markdown
### Candidate: [name]

**Entry**: file.ts:L23 — POST /api/x
**Sink**: file.ts:L88 — exec(...)
**Path**: 
  1. file.ts:L23 — req.body.cmd captured
  2. processor.ts:L14 — passed unchanged to worker
  3. worker.ts:L88 — exec(input)

**Adversarial questions**:
- Q: What validation happens between L23 and L88?
- A: [evidence — show the lines]

- Q: What input bypasses that validation?
- A: [the bypass — concrete example]

- Q: Does this match a known CWE?
- A: [CWE-XX, OWASP A0X]

**Verdict**: Confirmed / Refuted / Need-more-context
```

### Class-by-class adversarial questions

#### Injection (CWE-89, CWE-77, CWE-78, CWE-94)

```
- Where does user input meet a query / shell / template / eval?
- Is the bridge a parameterizing API or string concat?
- If parameterizing — is it actually parameterizing? (some libs accept identifiers via concat)
- Is there a "raw" / "unsafe" escape hatch nearby? Why is it there?
```

#### Auth / Authz (CWE-287, CWE-862, CWE-863, CWE-639 IDOR)

```
- Which routes are auth-checked? Which aren't? Which sometimes-are?
- Where is the role checked? Once at the gateway, or per-resource?
- For each resource ID accepted from the user, is there an ownership check?
- Are admin-only routes only checked by URL path? (path traversal, case mismatch)
- Is auth disabled in dev / test / debug — and is that flag derivable from prod?
```

#### Crypto (CWE-327, CWE-330, CWE-321, CWE-916)

```
- Is "random" actually CSPRNG?
- Are passwords hashed with argon2/bcrypt/scrypt — not MD5/SHA1/plain SHA256?
- Are secrets in env vars, not source / config commits?
- Are JWT secrets long, rotated, not the default "secret" string?
- Are encryption keys derived per-tenant / per-key, or is there one master?
- Are signatures verified BEFORE parsing?
```

#### Deserialization (CWE-502)

```
- pickle / unserialize / yaml.load / java ObjectInputStream — over external input?
- Are JSON revivers triggered (prototype pollution, Object.assign with __proto__)?
- Are XXE protections enabled in XML parsers?
```

#### SSRF (CWE-918)

```
- Is the URL controlled by user input?
- Is there a host allowlist?
- Is DNS rebinding mitigated (resolve once, pin)?
- Can the URL hit cloud metadata (169.254.169.254, fd00:ec2::254)?
- Are redirects followed without re-checking the destination?
```

#### Path traversal (CWE-22)

```
- Is filename from user input?
- Is `path.join` followed by a base-dir check?
- Is the input normalized before the check?
- Are symlinks resolved before the check?
- Are uploads stored with original filenames?
```

#### XSS (CWE-79)

```
- Is anywhere using innerHTML / dangerouslySetInnerHTML?
- Is template auto-escape disabled?
- Is markdown rendered without sanitization (DOMPurify, etc)?
- Are user-provided URLs rendered as href without javascript: scheme check?
```

#### CSRF (CWE-352)

```
- Mutating routes — do they require a CSRF token / SameSite=strict cookie / non-cookie auth?
- Is the cookie SameSite=lax (vulnerable to top-level GET-able mutations)?
- Are CORS headers permissive (Access-Control-Allow-Credentials with wildcard origin)?
```

#### Race conditions (CWE-362, CWE-367)

```
- Check-then-act on shared state? (TOCTOU)
- Are ledger / payment writes idempotent?
- Are concurrent updates protected by optimistic locking / row locks?
- Are file operations protected against TOCTOU symlink swaps?
```

#### Secrets (CWE-798, CWE-532)

```
- Hardcoded keys, tokens, passwords in source?
- Secrets in error messages, stack traces, logs?
- Secrets in git history (gitleaks --log-opts="--all")?
- .env committed?
- Secrets in client bundles (window.__INITIAL_STATE__)?
- Secrets in CI logs?
```

#### Supply chain (CWE-1357, CWE-829)

```
- Lockfile committed?
- postinstall / preinstall hooks in deps?
- Recently published deps with low download count? (typo-squat)
- Any deps with known CVEs (npm audit / osv-scanner)?
- Vendored binaries / scripts not audited?
```

### Stop condition

For each candidate from Phase 2: a verdict (Confirmed / Refuted / Need-more-context). No "I'll come back to it" — either it's a finding or it's refuted.

## Phase 5 — Exploit Chain (Detail)

See `kill-chain.md`. Goal: turn each Confirmed finding into a chain showing real-world impact.

### Stop condition

Each Confirmed finding has a chain (recon → ... → final action) OR is documented as standalone (single-step impact).

## Phase 6 — Impact (Detail)

DREAD-lite or CVSS v3 per chain. Score is **per-chain**, not per-bug — a "low" bug in a chain that grants RCE is part of a critical chain.

### Stop condition

Every chain has a numeric score + qualitative tier (Low / Medium / High / Critical).

## Phase 7 — Report + Remediate (Detail)

See `reporting.md` for the writeup format.

Remediation must include:

- **Specific** code change (diff or pseudo-diff).
- **Defense-in-depth**: at least one secondary control if primary fails.
- **Regression test**: a test that fails before fix, passes after.
- **Verification**: how to confirm the fix in the running system.

### Stop condition

Every Confirmed finding has all four remediation elements OR has an explicit "accepted risk" decision recorded by the user.

## Cross-Phase Rule

If at any phase you find yourself reasoning *defensively* ("this is probably fine"), **stop and re-frame adversarially**. Defensive reasoning produces missed findings. Defensive thinking returns in Phase 7 (remediation) — never before.
