# OWASP Top 10 + CWE Top 25 — Code Patterns + Remediation

Loaded for classification + lookup of code patterns + remediation per category.

## OWASP Top 10 (2021)

| ID | Category | Common CWEs |
|----|----------|-------------|
| A01 | Broken Access Control | CWE-22, CWE-285, CWE-639, CWE-862, CWE-863 |
| A02 | Cryptographic Failures | CWE-261, CWE-310, CWE-321, CWE-327, CWE-330 |
| A03 | Injection | CWE-77, CWE-78, CWE-79, CWE-89, CWE-94, CWE-643 |
| A04 | Insecure Design | (design-level, not single CWE) |
| A05 | Security Misconfiguration | CWE-2, CWE-13, CWE-16, CWE-260, CWE-315, CWE-732 |
| A06 | Vulnerable & Outdated Components | CWE-1104 |
| A07 | Identification & Authentication Failures | CWE-287, CWE-294, CWE-303, CWE-384, CWE-521 |
| A08 | Software & Data Integrity Failures | CWE-345, CWE-353, CWE-426, CWE-494, CWE-502, CWE-565, CWE-829 |
| A09 | Security Logging & Monitoring Failures | CWE-117, CWE-223, CWE-532, CWE-778 |
| A10 | Server-Side Request Forgery (SSRF) | CWE-918 |

## Per-Category Reference

### A01 — Broken Access Control

**Patterns to find**:

```
# IDOR — direct object refs from user, no ownership check
Grep: "findById\\(req\\.params\\.|findOne\\(.*req\\.body\\.id"
Grep: "WHERE id = \\$1" (without WHERE user_id = ?)

# Missing auth on routes
Grep: "@app\\.route\\(.*\\)" → for each, check next 5 lines for auth middleware

# Path traversal
Grep: "path\\.join\\(.*req\\." (not followed by base-dir check)
Grep: "fs\\.(readFile|createReadStream)\\(.*req\\."
```

**Remediation**:
- Check ownership on every resource access: `WHERE id = ? AND owner_id = ?`
- Centralize authz in middleware / decorator; deny-by-default.
- Normalize paths; check `resolved.startsWith(base)`.

---

### A02 — Cryptographic Failures

**Patterns**:

```
Grep: "crypto\\.createHash\\('(md5|sha1)'\\)"     # weak hashes
Grep: "Math\\.random"                              # not CSPRNG
Grep: "ECB|DES|RC4"                                # broken ciphers
Grep: "createCipher\\("                            # deprecated, no IV
Grep: "jwt\\.sign\\(.+,\\s*['\"][^'\"]{1,20}['\"]" # short JWT secret
```

**Remediation**:
- Hashing passwords: argon2id (preferred) / bcrypt (cost ≥ 12) / scrypt.
- Random tokens: `crypto.randomBytes` (Node), `secrets` (Python), `crypto/rand` (Go).
- Ciphers: AES-GCM with random IV, or libsodium / age.
- Long, rotated JWT secrets; or asymmetric (RS256 / EdDSA).

---

### A03 — Injection

**Patterns** (covers SQL, command, XSS, LDAP, NoSQL):

```
# SQL
Grep: "query\\(['\"`].+\\$\\{|\\+ req\\."           # template-string SQL with input
Grep: "raw\\(['\"`].*\\$\\{"                         # ORM raw

# Command
Grep: "exec\\(.*req\\.|spawn\\(.*shell:\\s*true"
Grep: "subprocess\\.(call|run)\\(.+shell=True"

# XSS
Grep: "dangerouslySetInnerHTML|innerHTML\\s*="
Grep: "v-html"                                       # Vue
Grep: "{{.*\\| safe }}"                              # Jinja unsafe

# Code injection
Grep: "\\beval\\(|new Function\\("

# NoSQL injection
Grep: "\\$where|\\$function"                         # MongoDB
```

**Remediation**:
- SQL: parameterized queries (via driver), never string concat. Use prepared statements.
- Shell: pass argv array, never a shell string. `child_process.execFile([cmd, args])`. Allowlist commands.
- HTML: rely on framework auto-escape. If raw HTML needed, sanitize via DOMPurify.
- Code: don't `eval` user input. Ever.
- NoSQL: typed ORM / query builder; reject `$`-prefixed keys in user input.

---

### A04 — Insecure Design

Design-level. Look for:

- Missing rate limits on sensitive ops (login, password-reset, signup, mutations).
- No idempotency on payment / mutation endpoints (replay risk).
- Trust in client-supplied state (e.g. price in cart, role in JWT).
- Lack of separation between admin and user planes.

**Remediation**: threat modeling per `references/threat-modeling.md`. This isn't fixed by patches.

---

### A05 — Security Misconfiguration

```
# Permissive CORS
Grep: "Access-Control-Allow-Origin.*\\*"
Grep: "cors\\(\\)" without origin allowlist

# Debug / verbose errors in prod
Grep: "DEBUG\\s*=\\s*True|app\\.config\\['DEBUG'\\]"
Grep: "stack:.*err\\.stack" in HTTP responses

# Default creds
Grep: "admin/admin|root/root|postgres/postgres"

# Open buckets / exposed dirs
Glob: "public/**, static/**" — review for accidental secrets / backups
```

**Remediation**: env-specific config, deny-by-default network policies, infra-as-code review.

---

### A06 — Vulnerable Components

```
# Run audits
Bash: "npm audit --json"
Bash: "pnpm audit --json"
Bash: "pip-audit --format json"
Bash: "osv-scanner --json ."

# Lockfile present?
Glob: "package-lock.json|pnpm-lock.yaml|yarn.lock|Cargo.lock|go.sum|poetry.lock|Pipfile.lock"
```

**Remediation**: keep lockfile committed, automate dep updates (Renovate/Dependabot), pin versions, see `references/supply-chain.md`.

---

### A07 — Authentication Failures

```
# Weak session
Grep: "express-session" → check store, cookie flags
Grep: "session_id.*Math\\.random"

# No MFA option for sensitive paths
Grep: "isAdmin|admin_required" → check for MFA gate

# Credential stuffing not mitigated
Grep: "/login|signin" → check for rate limits, CAPTCHA on threshold

# Password policy
Grep: "password.*length.*[0-9]+" → min length, complexity, breach-list check (HIBP)
```

**Remediation**: secure session lib defaults, MFA on admin + sensitive ops, rate limit per IP+account, breach-list check on password set.

---

### A08 — Software & Data Integrity Failures

```
# Insecure deserialization
Grep: "pickle\\.loads|yaml\\.load\\(|unserialize\\("
Grep: "ObjectInputStream"  # Java

# Unsigned auto-update
Grep: "fetch.*\\.tar\\.gz|wget|curl" in CI / install scripts — verify signatures?

# Untrusted CDN
Grep: "<script src=\"http://" → no SRI / wrong protocol
```

**Remediation**: `yaml.safe_load`, signed updates, Subresource Integrity for CDN scripts.

---

### A09 — Logging & Monitoring Failures

```
# Sensitive data in logs
Grep: "log.*password|log.*token|log.*ssn|log.*credit"

# No audit log on sensitive actions
Grep: "delete\\(" without nearby audit log call

# Errors swallowed
Grep: "catch.*\\{\\s*\\}" or "catch.*\\{\\s*//.*\\}"
```

**Remediation**: structured logging with field-level redaction, audit log for mutations, alert on auth failures + privilege changes.

---

### A10 — SSRF

```
# User-controlled URL fetch
Grep: "fetch\\(.*req\\.|axios.*req\\.|http\\.(get|request)\\(.*req\\."
Grep: "urllib\\..*\\(.*req\\.|requests\\.(get|post)\\(.*req\\."

# Cloud metadata fetch reachable?
Grep: "169\\.254\\.169\\.254|metadata\\.google\\.internal"
```

**Remediation**: host allowlist; resolve DNS once and pin IP for the request; block link-local / metadata IPs; block redirects to disallowed hosts.

---

## CWE Top 25 (selected high-impact)

| CWE | Name | OWASP |
|-----|------|-------|
| CWE-79 | XSS | A03 |
| CWE-787 | Out-of-bounds Write | (memory-unsafe langs) |
| CWE-89 | SQL Injection | A03 |
| CWE-416 | Use After Free | (memory-unsafe) |
| CWE-78 | OS Command Injection | A03 |
| CWE-20 | Improper Input Validation | (cross-cutting) |
| CWE-125 | Out-of-bounds Read | (memory-unsafe) |
| CWE-22 | Path Traversal | A01 |
| CWE-352 | CSRF | A01 |
| CWE-434 | Unrestricted File Upload | A04 |
| CWE-862 | Missing Authorization | A01 |
| CWE-476 | NULL Pointer Deref | (memory-unsafe) |
| CWE-287 | Improper Authentication | A07 |
| CWE-190 | Integer Overflow | (memory-unsafe) |
| CWE-502 | Insecure Deserialization | A08 |
| CWE-77 | Command Injection | A03 |
| CWE-119 | Buffer Errors | (memory-unsafe) |
| CWE-798 | Hardcoded Credentials | A07 |
| CWE-918 | SSRF | A10 |
| CWE-306 | Missing Auth for Critical Function | A01 |
| CWE-362 | Race Condition | (varies) |
| CWE-269 | Improper Privilege Mgmt | A01 |
| CWE-94 | Code Injection | A03 |
| CWE-863 | Incorrect Authorization | A01 |
| CWE-276 | Incorrect Default Permissions | A05 |

## How to Cite in Findings

Always cite CWE + OWASP in finding titles:

```
## [HIGH] User-controlled URL passed to fetch (CWE-918, OWASP A10:2021)
```

This makes findings searchable, comparable across teams, and mappable to remediation guides.
