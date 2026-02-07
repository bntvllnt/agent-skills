# Production Standards

> **Agent:** Load this file ONLY when Production mode is auto-selected. Not needed for Quick/Standard/Deep.

Production-grade review standards calibrated to Google, Linear, Vercel, and OpenAI engineering bars.

---

## A. Production Bar

Cross-company criteria. Every Production review evaluates against these:

### Google — Code Health

- **Readability:** Any engineer understands in <5 min. No clever tricks.
- **Logging:** Structured contextual logging. No bare `console.log`/`print`/`fmt.Println`.
- **Error propagation:** Errors carry trace ID, request ID, user context. Full stack available.
- **Ownership:** Every module has clear ownership. No orphaned code.

### Linear — Clean Architecture

- **Minimal abstractions:** No premature abstraction. Rule of Three enforced.
- **Strict type safety:** No `any`, no type assertions, discriminated unions for state.
- **Fast critical paths:** Measured, not assumed. Hot paths benchmarked.
- **No untracked debt:** Every `TODO`/`FIXME` links to a ticket or gets fixed now.

### Vercel — Edge-Ready

- **Caching strategy:** Explicit — what's cached, where, TTL, invalidation method.
- **Cold starts:** <1s for serverless. Lazy imports, minimal init.
- **Streaming:** Large responses use streaming. No buffering full payloads.
- **Edge-compatible:** No Node-only APIs in edge paths. Web standard APIs preferred.

### OpenAI — API Stability

- **Rate limiting:** All public endpoints rate-limited. Per-client, per-endpoint.
- **Graceful degradation:** Dependency failure = degraded service, not crash.
- **Full observability:** Metrics + traces + structured logs. SLI/SLO defined.
- **Backward compatibility:** No breaking changes without version bump. Deprecation period.

### Universal

- No secrets in code (env/vault only, `.env` in `.gitignore`)
- Schema validation at all system boundaries (Zod, Pydantic, JSON Schema)
- Actionable error messages (say what to do, not just what failed)
- Critical path tests exist and pass

---

## B. Expert Personas

Each perspective adopts a persona in Production mode. Persona = mindset + focus + bar.

### 1. Correctness — Staff SWE @ Google

- **Mindset:** "Read 100x more than written. Clarity > cleverness."
- **Focus:** Contract honoring, edge case coverage, regression safety, assumption documentation
- **Bar:** Could a new team member verify correctness by reading the code alone?

### 2. Security — Principal Security Eng @ OpenAI

- **Mindset:** "Assume adversarial users. Defense in depth."
- **Focus:** Input validation chains, auth/authz correctness, secret management, injection surfaces
- **Bar:** Would this survive a dedicated security audit?

### 3. Reliability — SRE @ Google (99.99%)

- **Mindset:** "What breaks at 3am? Can we recover automatically?"
- **Focus:** Error paths, graceful degradation, retry/backoff, resource cleanup, circuit breakers
- **Bar:** Can the system self-heal from any single dependency failure?

### 4. Performance — Staff Eng @ Vercel

- **Mindset:** "Every ms matters. Measure, don't guess."
- **Focus:** N+1 queries, caching strategy, bundle impact, cold starts, hot path optimization
- **Bar:** Is every hot path measurably fast? No guesswork?

### 5. DX — Senior Eng @ Linear

- **Mindset:** "Code is for humans. Make it obvious."
- **Focus:** Readability, naming, API ergonomics, error messages, type signatures
- **Bar:** Can a new dev ship a fix in this area within 30 minutes?

### 6. Scalability — Staff SWE @ Stripe

- **Mindset:** "100 instances, 10x traffic, 100x data."
- **Focus:** State management, data growth, concurrency, horizontal scaling, failure isolation
- **Bar:** Does this work behind a load balancer with N instances and 10x current load?

### 7. Observability — SRE @ Datadog

- **Mindset:** "Debug production without deploying new code."
- **Focus:** Structured logging, error tracking with context, metrics, distributed tracing, health signals
- **Bar:** Can you diagnose any production issue from dashboards and logs alone?

### 8. Testability — Staff SDET @ Microsoft

- **Mindset:** "Tests are documentation. Clear, fast, isolated."
- **Focus:** Happy + error path coverage, behavior assertions, isolation, regression detection
- **Bar:** Does every critical path have a test that catches regressions?

### 9. Accessibility — A11y Lead @ Shopify

- **Mindset:** "Everyone uses this, regardless of ability."
- **Focus:** Semantic HTML, keyboard navigation, screen reader support, contrast, focus management
- **Bar:** Can a keyboard-only user complete every interaction?

---

## C. Extended Checklists

Production mode uses these expanded checklists (15-20 items per perspective). Standard/Deep modes use the 6-item checklists in review.md.

### Correctness (16)

1. Implements exactly what was requested — no more, no less
2. All edge cases handled: empty, null, undefined, boundary values, off-by-one
3. Data integrity maintained — no invalid state possible
4. Type/interface contracts honored at all boundaries
5. No regression to existing behavior (backward compatible)
6. Assumptions documented or validated with assertions
7. Error paths return correct status codes and messages
8. Concurrent access produces correct results (no race conditions)
9. Idempotent operations are actually idempotent
10. Date/time handling accounts for timezones, DST, leap seconds
11. Unicode and internationalization handled correctly
12. Numeric overflow/underflow handled (large IDs, counts)
13. Order-dependent operations enforce ordering
14. Default values are safe and documented
15. Feature flags evaluated correctly with fallback behavior
16. Migration/rollback path verified for data changes

### Security (18)

1. All external input validated and sanitized at system boundaries
2. Request body schema validation (Zod, Pydantic, JSON Schema)
3. Parameterized queries only — no string interpolation in queries
4. XSS sanitization on all user-generated content rendered in HTML
5. No shell command injection — no `exec()` with user input
6. Auth middleware on all protected routes — no unprotected endpoints
7. RBAC/authorization checked at handler level, not just route level
8. JWT/token verification: signature + expiration + issuer validated
9. CSRF protection on state-changing endpoints
10. No secrets in code — all from env vars or secret manager
11. `.env` and credential files in `.gitignore`
12. No secrets or PII in log output
13. No stack traces or internal errors exposed to clients in production
14. PII handling follows data minimization — collect only what's needed
15. Dependencies scanned — no known CVEs (`npm audit`, `pip audit`)
16. Rate limiting on public-facing endpoints
17. Security headers set (CORS, CSP, HSTS, X-Frame-Options)
18. File upload validation: type, size, content verification

### Reliability (16)

1. All error paths handled — no swallowed errors or empty catch blocks
2. Errors propagate with context (stack, request ID, user ID)
3. Graceful degradation — dependency failure = reduced service, not crash
4. Retries use exponential backoff with jitter
5. Retry operations are idempotent (safe to repeat)
6. All external calls have timeouts configured
7. Partial failure leaves state consistent (transaction/rollback)
8. Resource cleanup on error (connections, file handles, listeners)
9. Circuit breakers on flaky dependencies
10. Health check endpoints reflect actual dependency health
11. Dead letter queues for failed async operations
12. Connection pool limits configured (not unbounded)
13. No unbounded queues or buffers (memory safety)
14. Fail-fast on startup if required dependencies unavailable
15. Graceful shutdown — drain connections, finish in-flight requests
16. Auto-recovery mechanism for transient failures

### Performance (15)

1. No N+1 query patterns — batch fetches with `IN` clauses
2. Database queries use appropriate indexes (explain plan verified)
3. Caching strategy explicit — what, where, TTL, invalidation
4. Cold start optimized — lazy imports, minimal initialization
5. Bundle size impact measured — no large unnecessary dependencies
6. Lazy loading for non-critical paths and heavy components
7. Hot path code optimized — measured with profiler, not guessed
8. Independent async operations parallelized (`Promise.all`, `asyncio.gather`)
9. Memory bounded — no large objects held unnecessarily, streams for large data
10. Connection pooling configured for database and HTTP clients
11. Database queries indexed for all filter/sort/join columns
12. No unnecessary serialization/deserialization cycles
13. Large response payloads use streaming or chunked transfer
14. List endpoints paginated with cursor or offset
15. Static assets on CDN/edge with cache headers

### DX (12)

1. Any engineer understands the code in <2 minutes
2. Names reveal intent — consistent with codebase conventions
3. Public API is intuitive — minimal surprise, discoverable
4. Error messages are actionable — say what to do, not just what failed
5. Types guide correct usage — impossible states are impossible
6. Code is where developers expect to find it
7. No dead code, commented-out code, or unused imports
8. Complex logic has a brief inline comment explaining why (not what)
9. Public exports have TSDoc/docstring with `@param`, `@returns`, `@example`
10. Config is centralized — no magic strings or numbers scattered
11. Breaking changes are obvious — compile-time errors, not runtime surprises
12. Debug/development aids don't leak into production paths

### Scalability (12)

1. State is per-request or properly synchronized — no shared mutable state
2. Works with 10x current data volume without degradation
3. No race conditions — concurrent access tested or prevented
4. Horizontally scalable — works behind load balancer with N instances
5. Components replaceable/scalable independently (loose coupling)
6. Failure isolated — one component failure doesn't cascade
7. Database queries scale with index, not full table scan
8. Background jobs are idempotent and resumable
9. Message processing handles out-of-order delivery
10. Cache invalidation strategy handles multi-instance deployment
11. No single points of contention (locks, single queues)
12. Data partitioning strategy exists for large datasets

### Observability (12)

1. Key operations logged with structured data (JSON, not strings)
2. Errors include full context: stack, request ID, user ID, input summary
3. Metrics instrumented: latency, throughput, error rate per endpoint
4. Requests traceable end-to-end across services (correlation ID)
5. Health signals detect issues before users report them
6. Can diagnose production issues without deploying new code
7. Log levels used correctly (error/warn/info/debug)
8. No sensitive data in logs (PII, tokens, passwords)
9. Alerting thresholds defined for critical metrics
10. Dashboard exists or is defined for key service metrics
11. Slow query logging enabled
12. Background job progress and failure tracked

### Testability (12)

1. Happy path test exists and passes
2. Key error paths tested (not just happy path)
3. Tests assert behavior, not implementation details
4. Critical branches tested: auth, payments, data mutations
5. Tests run independently — no shared state or order dependency
6. Only true external dependencies mocked — no over-mocking
7. Regression test covers the specific change being reviewed
8. Integration tests use real instances where possible
9. Test data is isolated — no reliance on global test fixtures
10. Edge cases tested: empty, null, boundary, concurrent
11. Tests are fast (<1s unit, <10s integration)
12. Test names describe the behavior being verified

### Accessibility (10)

1. Semantic HTML elements used (`button`, `nav`, `main`, not `div onClick`)
2. All interactions completable with keyboard only
3. ARIA labels, roles, and live regions correct and present
4. Color contrast meets WCAG AA (4.5:1 for text, 3:1 for large)
5. Focus order logical — tab sequence matches visual layout
6. Focus trapped in modals, returned on close
7. Works at 200% zoom without horizontal scroll
8. Form inputs have visible labels (not just placeholder)
9. Error states announced to screen readers (aria-live)
10. Images have meaningful alt text (or empty alt for decorative)

---

## D. Fallback Language Standards

When WebSearch is unavailable, apply these language-specific overlays:

### TypeScript

- `strict: true` in tsconfig — no exceptions
- No `any` or `as` assertions — use `unknown` + type guards
- Discriminated unions for state management
- Zod schemas at all system boundaries
- `useEffect` cleanup for subscriptions/timers
- Error boundaries around async UI operations
- No prop drilling >2 levels — use context or composition

### Python

- Type hints on all public API functions
- Pydantic models at API boundaries
- No bare `except:` — always catch specific exceptions
- Context managers for resource management (`with` statements)
- `async`/`await` for I/O-bound operations
- Connection pooling for database and HTTP clients
- No mutable default arguments

### Go

- Check every returned `error` — no `_` for errors
- Wrap errors with `fmt.Errorf("context: %w", err)`
- Context propagation through all call chains
- No goroutine leaks — ensure completion or cancellation
- Accept interfaces, return structs
- No `init()` abuse — explicit initialization preferred
- Structured logging (slog or zerolog, not `log.Println`)

### General (All Languages)

- Input validation at every system boundary
- No hardcoded secrets — environment variables or secret managers
- Structured logging — JSON format, no unstructured prints
- Error handling on every external call (network, file, DB)
- Tests exist for all critical paths
- No TODO/FIXME without linked ticket
