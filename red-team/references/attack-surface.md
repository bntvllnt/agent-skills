# Attack-Surface Enumeration & Taint Tracing

Phase 2 of the protocol. Produces the input → sink graph that drives Phase 4 vuln hunting.

## Definitions

- **Entry point**: any code path where attacker-controlled input enters the system.
- **Trust boundary**: a code/network boundary where authority levels change. Crossing it requires a control.
- **Sink**: code that performs a sensitive or dangerous operation (DB query, exec, write, render).
- **Taint**: a label on data meaning *"originated from an untrusted source."* Removed only by validation/sanitization.

A vulnerability is, in 90% of cases: **tainted data reaches a sink without losing its taint label.**

## Entry Point Inventory

Search systematically. For each language/framework:

### Web (HTTP)

```
# Express / Fastify / Koa
Grep: "app\\.(get|post|put|delete|patch)" 
Grep: "router\\.(get|post|put|delete|patch)"
Grep: "addHandler", "registerRoute"

# Next.js / Remix
Glob: "app/api/**/route.{ts,js}"
Glob: "pages/api/**/*.{ts,js}"

# Django / Flask
Grep: "@app\\.route", "@api_view", "path\\(", "url\\("

# Go
Grep: "mux\\.Handle", "http\\.HandleFunc", "echo\\.GET"

# Rails
Grep: "resources :", "get '", "post '"
```

### Webhook / Event

```
Grep: "webhook", "callback"
Grep: "Stripe.webhooks", "shopify.*webhook"
Grep: "addEventListener", "subscribe"
```

### Queue Consumers

```
Grep: "consumer", "subscribe.*queue"
Grep: "kafka", "rabbitmq", "sqs"
```

### File Upload

```
Grep: "multer", "formidable", "busboy"
Grep: "multipart/form-data"
Grep: "FileSystemAccess"
```

### gRPC / RPC

```
Glob: "*.proto"
Grep: "rpc ", "service "
```

### CLI / argv

```
Grep: "process\\.argv", "argparse", "commander", "yargs"
```

### Deserialization

Treat any deserializer as an entry point if input is external:

```
Grep: "JSON.parse", "yaml.load", "pickle.loads", "unserialize", "msgpack"
```

## Trust Boundaries

A **trust boundary** is anywhere authority changes. Common ones:

| Boundary | Direction | Required control |
|----------|-----------|------------------|
| Internet → web tier | inbound | TLS, WAF, rate limit, input validation |
| Web tier → DB | outbound | parameterized queries, least-priv DB user |
| Web tier → internal service | outbound | mTLS, signed requests, allowlist |
| Web tier → external API | outbound | TLS, API key in env, no SSRF |
| Auth-anonymous → authenticated | conditional | session check, redirect |
| Authenticated → authorized for resource | conditional | ownership/role check (IDOR guard) |
| User → admin | conditional | role check, MFA, separate plane |
| Process → file system | outbound | path normalization, chroot, sandbox |
| Process → shell | outbound | argv (not shell string), allowlist |

Mark boundaries on the DFD. **Every boundary needs a control. Missing control = candidate finding.**

## Sink Inventory

The dangerous operations. Map each by language:

### Code execution

```
Grep: "eval\\(", "Function\\(", "vm\\.runIn"
Grep: "exec\\(", "spawn\\(.*shell", "child_process"
Grep: "subprocess\\.(call|run|Popen).*shell=True"
Grep: "os\\.system", "popen"
```

### Query

```
Grep: "\\.query\\(", "\\.exec\\(", "\\.raw\\("
Grep: "db\\.collection.*find.*\\$where"
```

### File / path

```
Grep: "fs\\.(readFile|writeFile|createReadStream).*req\\.", "open\\(.*req\\."
Grep: "path\\.join.*req\\."
```

### Network

```
Grep: "fetch\\(.*req\\.", "axios.*req\\.", "http\\.get.*req\\."
```

### Render / interpolate

```
Grep: "innerHTML", "dangerouslySetInnerHTML"
Grep: "Markup\\(", "render_template_string", "Jinja.*autoescape=False"
```

### Crypto

```
Grep: "Math\\.random", "crypto\\.createHash\\('md5'\\)", "createHash\\('sha1'\\)"
Grep: "ECB", "DES", "RC4"
```

### Auth / session

```
Grep: "session\\[", "jwt\\.sign", "jwt\\.verify"
```

## Taint Tracing

For each entry → sink combination, trace the data flow:

```
INPUT (tainted)
   │
   ▼
[validation?]  ←── if absent, taint persists
   │
   ▼
[transformation]  ←── may sanitize, may not
   │
   ▼
[boundary crossing]  ←── auth check needed?
   │
   ▼
SINK (dangerous)
```

For each step, ask:

1. Does this step **remove** the taint? (e.g. parameterized query removes SQL-injection taint at the DB driver)
2. Does this step **transform** the taint into a different one? (e.g. JSON parse may turn SQL injection into prototype pollution)
3. Does this step **trust the upstream**? (e.g. internal API call assumes input was validated by the front door)

Common taint-removal mechanisms:

| Sink type | Correct remover |
|-----------|-----------------|
| SQL | parameterized query (NOT escaping) |
| Shell | argv array (NOT shell escaping) |
| HTML | template auto-escape (NOT manual escape unless audited) |
| LDAP | RFC 4515 escape |
| OS path | normalize + allowlist + base-dir check |
| URL fetch | host allowlist + DNS resolution check (SSRF) |

## Output Template

```markdown
## Attack Surface — [System]

### Entry Points
| ID | Type | Path | File | Auth required? | Notes |
|----|------|------|------|----------------|-------|
| E01 | HTTP POST | /api/upload | api/upload.ts:L12 | yes | accepts multipart |
| E02 | webhook | /hooks/stripe | api/hooks.ts:L34 | sig-only | verifies HMAC? |

### Trust Boundaries
| ID | From | To | Control | Adequate? |
|----|------|----|---------|-----------|
| B01 | internet | web tier | WAF + auth | yes |
| B02 | web tier | DB | parameterized queries | check Phase 4 |

### Sinks
| ID | Type | File | Tainted from? |
|----|------|------|---------------|
| S01 | exec | worker.ts:L88 | E01? |
| S02 | SQL raw | repo.ts:L201 | E03 |

### Entry → Sink Paths (Candidate Vulns)
| ID | Entry | Path (file:line steps) | Sink | Tainted? | Verified |
|----|-------|------------------------|------|----------|----------|
| P01 | E01 | upload.ts:L12 → process.ts:L44 → worker.ts:L88 | S01 | yes | confirmed CWE-78 |
```

Each `P` row in the candidate-vulns table is the input to Phase 4.

## Anti-Patterns (NEVER)

- NEVER trust internal services without applying the same controls as external. Assume breach.
- NEVER assume the front door validated input. Re-check at each layer (defense in depth).
- NEVER conflate "encoded" with "sanitized." Encoding is for output; validation is for input.
- NEVER trust client-side validation. The browser is hostile.
- NEVER trust the framework's "secure defaults" without verifying the version + config.
