# Testing Automation Protocol

> **Agent:** Load this file during ship BUILD phase when generating tests. Default test type is E2E. TDD is BLOCKING — tests written BEFORE implementation. Avoid mocking — use real systems. Also load for bug fixes when no test infrastructure exists.

Detect test infrastructure, understand existing patterns, propose setup if missing, scaffold tests with TDD enforcement (RED → GREEN → REFACTOR).

---

## Test Infrastructure Detection

Run once per session. Cache results.

### Test Runner Detection

| Indicator | Runner | Run Command |
|-----------|--------|-------------|
| `vitest.config.*` | Vitest | `vitest run` |
| `jest.config.*` or `"jest"` in package.json | Jest | `jest` |
| `pytest.ini` or `[tool.pytest]` in pyproject.toml | pytest | `pytest` |
| `*_test.go` files | Go test | `go test ./...` |
| `Cargo.toml` with `[dev-dependencies]` | Cargo test | `cargo test` |
| `*.test.ts` / `*.spec.ts` without config | Infer from package.json `"test"` script | Use script |
| None found | **No test infra** | Propose setup |

### E2E Framework Detection

| Indicator | Framework | Run Command |
|-----------|-----------|-------------|
| `playwright.config.*` | Playwright | `npx playwright test` |
| `cypress.config.*` or `cypress/` dir | Cypress | `npx cypress run` |
| `maestro/` dir or `.maestro/` | Maestro | `maestro test` |
| `detox.config.*` | Detox | `detox test` |
| `selenium` in dependencies | Selenium | Project-specific |
| None found | **No E2E infra** | Propose setup if journey-impacting changes |

### Package Manager Detection

| Lockfile | Manager | Install Command |
|----------|---------|-----------------|
| `pnpm-lock.yaml` | pnpm | `pnpm add -D` |
| `yarn.lock` | yarn | `yarn add -D` |
| `bun.lockb` | bun | `bun add -D` |
| `package-lock.json` | npm | `npm install -D` |

## Test Setup Deep Discovery (MANDATORY — once per session)

Don't just detect config files — understand the actual test setup. This informs all test generation.

### Discovery Protocol

1. **Read 3+ existing test files** to understand patterns, conventions, helpers
2. **Identify test utilities**: factories, fixtures, seeds, test DB setup, custom matchers
3. **Map mock usage**: what's already mocked vs real (inventory existing mocks)
4. **Identify test database strategy**: migrations, seeds, Docker, in-memory, test DB
5. **Identify test server setup**: real server, supertest, test client, test fixtures
6. **Cache results** for session — don't re-read every iteration

### Output: Test Environment Profile

```
Test Environment Profile:
  Runner: {vitest/jest/pytest/go test/cargo test}
  E2E Framework: {playwright/cypress/maestro/detox/none}
  DB Strategy: {test DB + migrations / Docker / in-memory / none}
  Mock Inventory: {list of currently mocked dependencies}
  Server Setup: {real server / supertest / test client}
  Existing Patterns: {describe structure, naming, helper usage}
  Existing E2E Coverage: {list of E2E test files + what they cover}
```

This profile informs all test generation — write tests that match the project's real setup.

## Test Type Mapping (E2E-First)

Default to E2E. Unit tests are the exception, not the rule.

```
For each scope item / AC:
  Is it a pure function? (no I/O, no side effects, deterministic)
    YES → Unit test (ONLY case for unit tests)
    NO  → E2E test
```

| Scope Item Type | Test Type | Why |
|-----------------|-----------|-----|
| Pure function / utility (no I/O) | Unit test | Isolated, fast, deterministic — the ONLY unit test case |
| API endpoint | E2E test | Tests full request → middleware → handler → DB → response |
| DB query / mutation | E2E test | Tests real DB with real schema, migrations, data |
| UI component (any) | E2E test | Tests in real browser with real rendering |
| User journey / flow | E2E test | Tests full path through the system |
| Bug fix | E2E regression test | See [regression-testing.md](patterns/regression-testing.md) |
| Config / env change | E2E smoke test | Verify system starts and responds end-to-end |
| State management | E2E test | Tests real state transitions in running app |
| Auth / permissions | E2E test | Tests real auth middleware with real tokens |
| Third-party integration | E2E test | Tests real integration (sandbox/test mode preferred) |

## Step 0: AC-to-Test Mapping

Before writing any tests, map ACs to test intentions. This feeds the [E2E scenario registry](e2e-scenarios.md).

```
For each AC in spec:
  1. Determine test type (E2E default, unit only if pure function)
  2. Determine test file location (follow existing conventions)
  3. Write registry entry: AC → test file → PENDING
  4. For Error ACs (AC-E): map to error scenario E2E test
  5. For Failure Hypotheses (FH): map to defensive E2E test

Output: populated e2e-scenarios.md registry with all entries PENDING
```

## TDD Enforcement Protocol (BLOCKING)

Every test follows RED → GREEN → REFACTOR. This is not advisory — it's structurally enforced.

### RED Phase (test before implementation)

```
1. Write E2E test asserting CORRECT behavior (what SHOULD happen)
2. Run test → MUST FAIL
   - If PASS → wrong test (doesn't test new behavior). Rewrite.
   - If ERROR (setup/config) → fix test infrastructure, not test logic
3. Log RED_CONFIRMED in e2e-scenarios registry
4. BLOCKING: cannot proceed to GREEN without RED_CONFIRMED
```

### GREEN Phase (minimal implementation)

```
1. Implement ONLY enough code to make the test pass
2. Run test → MUST PASS
   - If FAIL → fix implementation, not the test
   - Iterate until PASS (max 3 attempts → escalate)
3. Log GREEN_CONFIRMED in e2e-scenarios registry
4. BLOCKING: GREEN_CONFIRMED requires prior RED_CONFIRMED
```

### REFACTOR Phase (clean up)

```
1. Refactor implementation (extract, rename, simplify)
2. Run test → MUST STILL PASS
   - If FAIL → refactoring broke something. Undo refactor, try again.
3. No registry update needed — status stays GREEN_CONFIRMED
```

### TDD Violation Detection

```
IF agent tries to mark GREEN_CONFIRMED without RED_CONFIRMED:
  BLOCK "TDD violation: must confirm RED before GREEN for {AC}"

IF test passes on first run (RED phase):
  WARN "Test passes before implementation — not testing new behavior"
  Action: rewrite test to be more specific, or verify this AC was already implemented
```

## Mock Avoidance Hierarchy (prefer real over mock)

Mocking hides bugs. Use real systems whenever possible.

### Hierarchy (most preferred → least preferred)

| Level | Strategy | Example | Confidence |
|-------|----------|---------|------------|
| 1 (BEST) | Real system | Test DB, test server, sandbox API | Highest — tests real behavior |
| 2 | Docker/container | Testcontainers, Docker Compose | High — real dependency, isolated |
| 3 | In-memory equivalent | SQLite for Postgres, LocalStack for AWS, local S3 emulator | Medium — similar but not identical |
| 4 (LAST RESORT) | Mock | Jest mock, test double, stub | Lowest — tests your assumptions, not reality |

For each mock, document: WHY real isn't possible, WHAT you're losing by mocking.

**Mock justification required:** every mock must have a comment:
```
// MOCK: {reason real system not available} — losing: {what this mock doesn't test}
```

### DENY Mocking (hard boundary — NEVER mock these)

| Category | Why | Instead |
|----------|-----|---------|
| Own application code (services, repos, controllers) | Testing your code against your mocks proves nothing | Use real code paths |
| Own database | Missing real query bugs, schema issues, constraints | Use test DB with real migrations + seeds |
| Own HTTP endpoints | Missing middleware, auth, validation, serialization | Use real test server (supertest, test client) |
| Own auth middleware | Missing real auth flow, token validation, permissions | Use test tokens against real auth middleware |
| Internal service calls | Missing integration bugs at boundaries | Test the integrated path end-to-end |

### ALLOW Mocking (only when levels 1-3 exhausted)

| Category | When Allowed | Check First |
|----------|-------------|-------------|
| Third-party APIs | No sandbox AND no Docker AND no recording | Stripe, Twilio, SendGrid have sandboxes — use real |
| Time/date | Deterministic test assertions needed | Use clock injection pattern if framework supports |
| Random/UUID | Deterministic test assertions needed | Seed the generator if possible |
| External OAuth providers | No test mode available | Check provider docs for test/sandbox mode first |
| Email/SMS delivery | No local test server available | Check for Mailhog, local SMTP, test mode |

### Before Mocking Any Third-Party API

```
1. Does it have a sandbox/test mode?
   Stripe → YES (test keys), Twilio → YES (test credentials),
   SendGrid → YES (sandbox), GitHub → YES (test tokens)
   → USE REAL SANDBOX

2. Does it have a Docker image?
   LocalStack (AWS), MinIO (S3), fake-gcs-server (GCS)
   → USE CONTAINER

3. Can we use recording/replay?
   VCR (Ruby), Polly.js (JS), go-vcr (Go), pytest-recording (Python)
   → USE RECORDING

4. None of the above available?
   → MOCK with justification comment (last resort)
```

## E2E Test Selection Framework

Synthesized from: Kent C. Dodds (Testing Trophy), Spotify (Testing Honeycomb), Google (Test Pyramid), risk-based testing.

### Core Principle

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

### Test Selection Heuristic (per AC)

```
For each AC or scope item, score on 3 axes:

1. REVENUE IMPACT (what breaks if this fails?)
   Money path (checkout, payment, subscription)    → CRITICAL
   Auth/onboarding (blocks all usage)              → CRITICAL
   Core feature (primary value prop)               → HIGH
   Secondary feature                               → MEDIUM
   Admin/internal tool                             → LOW

2. BLAST RADIUS (how many users affected?)
   All users                                       → CRITICAL
   Segment/role                                    → HIGH
   Edge case users                                 → MEDIUM
   Internal only                                   → LOW

3. FAILURE VISIBILITY (how fast is failure detected?)
   Silent data corruption                          → CRITICAL
   Degraded experience (slow, broken UI)           → HIGH
   Error message shown (user can recover)          → MEDIUM
   Logged server-side only                         → LOW

SCORE = max(revenue, blast_radius, failure_visibility)

  CRITICAL → E2E MANDATORY, multi-path (happy + error + edge)
  HIGH     → E2E MANDATORY, happy path + primary error
  MEDIUM   → E2E recommended, happy path minimum
  LOW      → Unit/integration sufficient (E2E optional)
```

### Test Shape by Architecture

| Architecture | Best Shape | E2E Focus |
|-------------|-----------|-----------|
| Monolith / Full-stack (Next.js, Rails) | Trophy (Dodds) | Integration-heavy, E2E for critical paths |
| Microservices | Honeycomb (Spotify) | Contract tests between services, E2E for user journeys |
| API-only / Backend | Diamond | E2E = API tests with real DB + real HTTP |
| UI-heavy / SPA | Trophy + E2E layer | Heavy E2E for visual + interaction + navigation |
| Mobile (Expo/RN) | Trophy + device | Maestro flows for core user journeys |

### Critical Path Categories (ALWAYS E2E regardless of score)

| Category | Why | Example |
|----------|-----|---------|
| Money paths | Revenue loss if broken | Checkout, payment, subscription, billing |
| Auth flows | Blocks all access if broken | Login, signup, password reset, OAuth, session |
| Onboarding | First impression, high churn risk | Registration, setup wizard, first-run |
| Data mutations | Corruption risk, hard to rollback | Create/update/delete user data, file upload |
| Third-party integrations | External failure = silent breakage | Payment gateway, email, SMS, OAuth provider |
| Cross-system flows | Integration boundary = failure boundary | API → DB → cache → queue → notification |

### Confidence Metric

```
                     confidence gained
Test ROI = ─────────────────────────────────
           time to write + time to maintain

Integration tests: HIGH confidence / LOW maintenance  → best ROI
E2E tests:         HIGHEST confidence / HIGHER maint  → use selectively (CRITICAL/HIGH)
Unit tests:        MEDIUM confidence / LOWEST maint    → pure functions only
```

### Anti-Patterns in Test Selection (NEVER)

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| "Test everything with E2E" | Slow, flaky, expensive | Score per AC, E2E for CRITICAL/HIGH |
| "100% code coverage" | Diminishing returns past ~70-80% | AC coverage > line coverage |
| "E2E for implementation details" | Brittle, breaks on refactor | Test user outcomes, not DOM structure |
| "Mock everything for speed" | False confidence, misses real bugs | Real systems, mock only third-party |
| "One giant E2E test per feature" | Hard to debug, flaky, slow | Focused tests per AC/journey step |
| "Ice cream cone" (all manual) | Expensive, slow feedback | Shift left, automate integration layer |

## Generation Workflow

```
0. MAP      → Map ACs to test types, create e2e-scenarios registry entries
1. DETECT   → Scan for test infra (runner, framework, conventions)
2. DISCOVER → Deep test setup discovery (read existing tests, understand patterns)
3. PROPOSE  → If missing, propose setup (don't auto-install)
4. SCAFFOLD → Generate test file structure + describe blocks
5. RED      → Run scaffolded tests → MUST FAIL (TDD enforcement)
6. FILL     → Implement code to make tests pass
7. GREEN    → All tests pass after implementation
8. REFACTOR → Clean up, re-run → still GREEN
```

### Step 0: MAP

```
Load spec ACs + Error Journeys + Failure Hypotheses
For each:
  Determine test type (E2E default, unit for pure functions)
  Create entry in e2e-scenarios.md: AC → test file → PENDING
```

### Step 1: DETECT

```
Check project root for:
  - Test runner config (see detection table above)
  - E2E framework config (see E2E detection table above)
  - Existing test files (glob: **/*.test.*, **/*.spec.*, **/*_test.*)
  - Test directory conventions (check existing test locations)
  - Test scripts in package.json / Makefile / Cargo.toml
```

### Step 2: DISCOVER (MANDATORY)

```
Read 3+ existing test files:
  - Understand patterns (describe structure, assertion style, setup/teardown)
  - Identify test utilities (factories, fixtures, custom matchers)
  - Map mock inventory (what's mocked, what's real)
  - Identify DB strategy (test DB, Docker, in-memory)
  - Identify server setup (real server, supertest, test client)

Output: Test Environment Profile (cached for session)
```

### Step 3: PROPOSE (if missing)

```
No test runner found:
  Recommend: {runner} based on project stack
  Setup: {install command} + {minimal config}
  Proceed with setup? [y/n]

No E2E framework found (but test runner exists):
  Recommend: {E2E framework} based on project type
  Setup: {install command} + {minimal config}
  Proceed with setup? [y/n]

If user declines → document skip, E2E gate downgrades to ADVISORY
```

### Step 4: SCAFFOLD

```
For each scope item needing tests:
  1. Determine test type from AC mapping (E2E default)
  2. Find existing test directory convention
  3. Create test file with:
     - Imports (matching project patterns from DISCOVER)
     - describe block matching feature/module name
     - it/test blocks for each AC (with assertions for CORRECT behavior)
     - Setup/teardown matching project patterns
     - Real system connections (test DB, test server — NOT mocks)
```

### Step 5-8: RED → FILL → GREEN → REFACTOR

```
RED: Run scaffolded tests → should FAIL (correct behavior not yet implemented)
  If they PASS → tests aren't testing new behavior. Fix.
  Log RED_CONFIRMED in e2e-scenarios registry.

FILL: Implement code to make tests pass
  Minimal implementation — just enough to pass

GREEN: Run tests → should PASS
  If FAIL → fix implementation, not tests
  Log GREEN_CONFIRMED in e2e-scenarios registry.

REFACTOR: Clean up implementation
  Run tests → must still PASS
```

## Framework-Specific Scaffolds

### Vitest / Jest (TypeScript)

```typescript
import { describe, it, expect } from 'vitest' // or jest globals
import { functionName } from '../module'

describe('functionName', () => {
  it('should {expected behavior} given {input condition}', () => {
    // Arrange
    // Act
    // Assert
  })

  it('should {error behavior} given {edge case}', () => {
    // Arrange
    // Act & Assert
  })
})
```

**File location:** Mirror source structure. `src/utils/parse.ts` → `src/utils/parse.test.ts` (colocated) or `tests/utils/parse.test.ts` (separate dir). Follow existing convention.

### pytest (Python)

```python
import pytest
from module import function_name


class TestFunctionName:
    def test_expected_behavior_given_input_condition(self):
        # Arrange
        # Act
        # Assert
        pass

    def test_error_behavior_given_edge_case(self):
        # Arrange
        # Act & Assert
        pass
```

**File location:** `tests/test_{module}.py` or colocated `{module}_test.py`. Follow existing convention.

### Go

```go
package module_test

import (
    "testing"
)

func TestFunctionName_ExpectedBehavior(t *testing.T) {
    // Arrange
    // Act
    // Assert
}

func TestFunctionName_EdgeCase(t *testing.T) {
    // Arrange
    // Act
    // Assert
}
```

**File location:** Same package directory, `{file}_test.go`.

### Playwright (E2E)

```typescript
import { test, expect } from '@playwright/test'

test.describe('{feature name}', () => {
  test('should {user journey step}', async ({ page }) => {
    // Navigate
    // Interact
    // Assert outcome (not DOM structure)
  })

  test('should handle {error scenario}', async ({ page }) => {
    // Trigger error condition
    // Assert error feedback visible to user
    // Assert recovery path works
  })
})
```

**File location:** `e2e/` or `tests/e2e/` directory. Follow existing convention.

### Cypress (E2E)

```typescript
describe('{feature name}', () => {
  it('should {user journey step}', () => {
    // Navigate
    // Interact
    // Assert outcome
  })
})
```

**File location:** `cypress/e2e/` directory. Follow existing convention.

## Test Naming Conventions

| Framework | Convention | Example |
|-----------|-----------|---------|
| Vitest/Jest | `{module}.test.ts` | `auth.test.ts` |
| pytest | `test_{module}.py` | `test_auth.py` |
| Go | `{file}_test.go` | `auth_test.go` |
| Playwright | `{feature}.spec.ts` | `auth.spec.ts` |
| Cypress | `{feature}.cy.ts` | `auth.cy.ts` |
| Maestro | `{feature}.yaml` | `auth.yaml` |

**Follow existing project conventions over these defaults.** Check 3+ existing test files for patterns.

## Rules

- **E2E-first** — default to E2E tests. Unit tests only for pure functions (no I/O, no side effects)
- **TDD is BLOCKING** — RED must be confirmed before GREEN. Tests written BEFORE implementation.
- **Real systems preferred** — use test DB, test server, sandbox APIs. Mock is last resort.
- **Mock justification required** — every mock needs `// MOCK: {reason}` comment
- **Never mock own code** — services, repos, DB, endpoints, auth, internal calls are NEVER mocked
- **Always verify RED first** — a test that passes on empty implementation is useless
- **Follow existing conventions** — check 3+ existing tests before creating new ones
- **One test file per module** — don't scatter tests across files
- **Test behavior, not implementation** — assert user outcomes and effects, not internal calls
- **No test file without a reason** — every test must trace to an AC, scope item, or bug
- **AC-driven coverage** — every Must Have + Error AC gets an E2E test in the registry
- **Failure mode coverage** — every HIGH/MED failure hypothesis gets a defensive E2E test
