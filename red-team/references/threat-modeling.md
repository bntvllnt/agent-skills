# Threat Modeling — STRIDE + Shostack 4 Questions

Loaded when user invokes threat modeling explicitly, or when the engagement targets a *system / feature* (not just a single file).

## Shostack's 4 Questions

The whole-system frame:

```
1. What are we building?
2. What can go wrong?
3. What are we doing about it?
4. Did we do a good job?
```

Run these top-down, then drill into STRIDE per asset for question 2.

### Question 1 — What are we building?

Produce a **data-flow diagram** (DFD), even if just ASCII:

```
                         ┌──────────────┐
   ┌──────────┐  HTTPS   │              │   ┌──────────┐
   │  USER    │──────────│  WEB APP     │───│   DB     │
   │ (browser)│          │              │   └──────────┘
   └──────────┘          │              │
                         │              │   ┌──────────┐
   ┌──────────┐  webhook │              │───│  CACHE   │
   │ STRIPE   │──────────│              │   └──────────┘
   └──────────┘          │              │
                         │              │   ┌──────────┐
                         │              │───│ S3 / FS  │
                         └──────────────┘   └──────────┘
                                ▲
                                │
                       trust boundary
                       (── − − − ── )
```

Mark **trust boundaries** — every line crossing one is a place where attacker control or data leakage is possible.

### Question 2 — What can go wrong? (STRIDE)

For each asset (each box, each line), apply STRIDE:

| Letter | Threat | Concrete questions |
|--------|--------|--------------------|
| **S** Spoofing | identity forgery | Can an attacker authenticate as another user? Forge a session? Impersonate a service? |
| **T** Tampering | data modification | Can an attacker modify data on the wire? In the DB? In transit between services? In logs after the fact? |
| **R** Repudiation | deniable action | Can a user perform an action and deny it? Are auth events / mutations logged with non-repudiable identity? |
| **I** Info disclosure | data leakage | What's exposed in error messages? Logs? Side channels? Backup files? S3 buckets? Stack traces? |
| **D** DoS | availability loss | What input/load makes this asset unavailable? Are there resource limits? Rate limits? Circuit breakers? |
| **E** Elevation | privilege gain | What lets a low-priv principal become high-priv? Vertical (user → admin)? Horizontal (user A → user B's data)? |

Per-asset table:

```markdown
### Asset: User Session Cookie

| STRIDE | Threat | Mitigation in place | Adequate? | Action |
|--------|--------|---------------------|-----------|--------|
| S | Stolen cookie used for spoofing | HttpOnly, Secure, SameSite=strict | yes | — |
| T | Cookie value tampering | HMAC-signed | yes | — |
| R | User claims they didn't perform action | audit log w/ session ID | partial | add device fingerprint |
| I | Cookie leaked via XSS | HttpOnly + CSP | yes | — |
| D | Cookie store DoS | session expiry + size limit | yes | — |
| E | Session fixation → priv escalation | rotate on auth | yes | — |
```

### Question 3 — What are we doing about it?

For each STRIDE row marked "no" or "partial":

- Define a **specific** mitigation (not "improve security").
- Place it in the code: file path, layer, control type.
- Decide: prevent / detect / respond.

Mitigation cheat sheet:

| Threat type | Common controls |
|-------------|-----------------|
| Spoofing | strong auth, MFA, mutual TLS, short-lived tokens, session rotation |
| Tampering | TLS, HMAC / signatures, immutable logs, integrity checks, code signing |
| Repudiation | audit logs with non-repudiable identity, append-only stores, log shipping |
| Info disclosure | encryption at rest + in transit, key mgmt, access controls, error sanitization, no PII in logs |
| DoS | rate limits, quotas, timeouts, circuit breakers, autoscaling, load shedding |
| Elevation | least privilege, role checks at every boundary, separation of duties, no client-trusted role |

### Question 4 — Did we do a good job?

Test the mitigations. For each:

- **Unit / integration test** that fails when mitigation is removed.
- **Negative test** that asserts the threat scenario is blocked (e.g. test that posts a forged JWT and expects 401).
- **Regression test** in CI so the mitigation doesn't decay.

Without this step, the threat model is paper. With it, the threat model is enforced.

## Output Template

```markdown
## Threat Model: [System / Feature]

### Scope
[Target, in/out of scope, authorization]

### Architecture (DFD)
[ASCII DFD with trust boundaries]

### Assets
| Asset | Sensitivity | Owner |
|-------|-------------|-------|
| ... | ... | ... |

### STRIDE per Asset
[One table per asset, as above]

### Top Threats (Ranked)
| ID | Threat | Asset | STRIDE | Severity | Mitigation | Test |
|----|--------|-------|--------|----------|------------|------|
| T01 | ... | ... | S | High | ... | tests/auth.spec.ts:L23 |

### Open Questions
- [Things that need user / team input]
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| STRIDE applied at "system" level, no per-asset | Pick each asset, run STRIDE per asset |
| Mitigations vague ("improve auth") | Specify file, layer, control |
| No test for mitigation | Add negative test in same PR as mitigation |
| Trust boundaries omitted from DFD | Mark every line that crosses boundary |
| Internal services treated as fully trusted | Apply STRIDE there too — assume breach |
| Threat model done once, never updated | Re-run on architecture changes; gate in PR template |
