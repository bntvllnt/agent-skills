# Secret Hunting

Secrets in code, history, logs, build artifacts, and client bundles. Loaded when user invokes secret hunting or full audit.

## Where Secrets Hide

```
1. Source code           — string literals
2. Config files          — .env committed, config.{json,yml,toml}
3. Git history           — even if removed in latest commit
4. CI logs               — printed env, secrets in error output
5. Client bundles        — window.__INITIAL_STATE__, inlined env
6. Container images      — multi-stage but final layer has secret
7. Logs                  — "Authorization: Bearer <token>" in HTTP logs
8. Backups               — pg_dump, S3 snapshots
9. Test fixtures         — real keys used in tests
10. Comments             — "// TODO: rotate this prod key"
```

## Tools (use if installed; fallback to manual Grep)

### gitleaks

```bash
gitleaks detect --source . --no-banner
gitleaks detect --source . --log-opts="--all"   # full history
```

### trufflehog

```bash
trufflehog filesystem . --no-update
trufflehog git file://. --no-update             # full history
```

### detect-secrets

```bash
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

If none installed, the skill notes it in the report and proceeds with manual `Grep`.

## Manual Grep Patterns

These are starting points. Each gives false positives; verify by reading.

### Generic high-entropy strings

```
# Looks like a key (40+ char alnum)
Grep: "['\"][A-Za-z0-9+/=_-]{40,}['\"]"
```

### Provider-specific

```
# AWS
Grep: "AKIA[0-9A-Z]{16}"                  # access key id
Grep: "aws_secret_access_key"

# Google
Grep: "AIza[0-9A-Za-z\\-_]{35}"           # API key
Grep: "ya29\\."                            # OAuth

# Stripe
Grep: "sk_(live|test)_[0-9a-zA-Z]{24,}"

# GitHub
Grep: "ghp_[0-9a-zA-Z]{36}"
Grep: "github_pat_[0-9a-zA-Z_]{82}"

# Slack
Grep: "xox[baprs]-[0-9a-zA-Z-]{10,}"

# Generic JWT
Grep: "eyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+"

# Private key
Grep: "-----BEGIN (RSA |EC |OPENSSH |PGP |DSA )?PRIVATE KEY"
```

### Variable-name signals

```
Grep: "(api_?key|secret|token|password|passwd|pwd|credential)\\s*[:=]\\s*['\"]"
```

### Env file commits

```
Glob: ".env, .env.*"   # excluding .env.example
```

## Git History Search

Even if `.env` was deleted, history retains it:

```bash
git log --all --pretty=format: --name-only --diff-filter=A | sort -u | grep -E "\\.env$"

git log -p --all -S "AKIA"      # any historical commit containing AKIA prefix
git log -p --all -S "BEGIN PRIVATE KEY"
```

If found:

1. **Treat the secret as compromised.** It is in history; assume disclosed.
2. **Rotate the secret immediately.** Don't rewrite history first.
3. **After rotation**, optionally rewrite history (`git filter-repo` / BFG) to remove the old secret. This requires force-push and coordination with all clones.
4. **Document** in report: rotation timestamp, old → new, comms to consumers.

## Client-Bundle Inspection

Front-end bundles often contain inlined "public" keys that are actually private:

```bash
# Build the production bundle, then:
Grep: "AKIA|sk_live|ghp_|xox[baprs]" in dist/ / build/ / .next/static/
```

Look for env vars exposed via build-time inlining (`NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`) — anything in those will end up in the client.

## Log Hygiene

```
# Authorization header logged
Grep: "log.*[Aa]uthorization"
Grep: "log.*headers"          # check if headers are logged in entirety

# Tokens in URL (then in access logs)
Grep: "\\?(access_)?token="   # tokens in query strings
Grep: "Bearer " in URL paths
```

**Rule**: tokens go in `Authorization` header, never in query strings. Headers can be redacted in logs; URLs end up in access logs everywhere.

## CI / Container

```
# Dockerfile copies .env or secrets
Grep: "COPY \\..*\\.env" in Dockerfile

# CI prints env
Grep: "env\\s*$|printenv" in .github/workflows/**/*.yml
```

## Output Template

```markdown
## Secret Hunt Findings

### High Confidence (verified live secret)
| ID | Type | Location | Line | Status | Rotated? |
|----|------|----------|------|--------|----------|
| S01 | AWS access key | src/config.ts | 42 | LIVE | NO — rotate |

### Medium Confidence (likely secret, needs verification)
| ID | Type | Location | Line | Action |
|----|------|----------|------|--------|
| S02 | high-entropy string | tests/fixture.json | 17 | verify if real |

### Git History
| ID | Secret | First commit | Last commit | Status |
|----|--------|--------------|-------------|--------|
| H01 | DB password | abc123 | def456 | rotated 2024-12-01 |

### Remediation Required
- [ ] Rotate S01 immediately
- [ ] Verify S02
- [ ] Move secrets to env / secret manager (not source)
- [ ] Add gitleaks to pre-commit / CI
- [ ] Audit access logs for last N days for compromise indicators
```

## Anti-Patterns (NEVER)

- NEVER print full secret in writeup — first/last 4 chars + length is enough.
- NEVER rewrite git history before rotating. Rotation first, history rewrite second.
- NEVER assume "it's only in history" means safe. History is public on public repos and accessible to anyone with read access on private repos.
- NEVER store secrets in source even if "encrypted at rest" — the decryption key has to live somewhere.
- NEVER commit `.env` even with `.gitignore` "in front" — verify with `git ls-files .env`.
