# Testing Automation Protocol

> **Agent:** Load this file during ship BUILD phase when generating tests. Also load for bug fixes when no test infrastructure exists.

Detect test infrastructure, propose setup if missing, scaffold tests, verify RED/GREEN.

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

## Test Type Mapping

Map scope items to test types:

| Scope Item Type | Test Type | Why |
|-----------------|-----------|-----|
| Pure function / utility | Unit test | Isolated, fast, deterministic |
| API endpoint | Integration test | Tests request → response with real middleware |
| DB query / mutation | Integration test | Needs real (or test) DB connection |
| UI component (logic) | Unit test | Test behavior, not rendering |
| UI component (visual) | Snapshot or visual test | Catch unintended visual changes |
| User journey / flow | E2E test | Tests full path through the system |
| Bug fix | Regression test | See [regression-testing.md](patterns/regression-testing.md) |
| Config / env change | Smoke test | Verify system starts and responds |

## Generation Workflow

```
1. DETECT   → Scan for test infra (runner, framework, conventions)
2. PROPOSE  → If missing, propose setup (don't auto-install)
3. SCAFFOLD → Generate test file structure + describe blocks
4. VERIFY   → Run scaffolded tests (expect failures = RED)
5. FILL     → Add assertions as implementation progresses
6. GREEN    → All tests pass after implementation
```

### Step 1: DETECT

```
Check project root for:
  - Test runner config (see detection table above)
  - Existing test files (glob: **/*.test.*, **/*.spec.*, **/*_test.*)
  - Test directory conventions (check existing test locations)
  - Test scripts in package.json / Makefile / Cargo.toml
```

### Step 2: PROPOSE (if missing)

```
No test runner found.
Recommend: {runner} based on project stack.

Setup:
  {install command}
  {minimal config}

Proceed with setup? [y/n]
```

If user declines → document skip, continue without tests.

### Step 3: SCAFFOLD

Generate test files following project conventions:

```
For each scope item needing tests:
  1. Determine test type (unit/integration/e2e)
  2. Find existing test directory convention
  3. Create test file with:
     - Imports
     - describe block matching module name
     - it/test blocks for each behavior (empty assertions)
     - Setup/teardown if needed
```

### Step 4-6: VERIFY → FILL → GREEN

```
Run scaffolded tests → should FAIL (RED, no assertions yet)
  If they PASS → tests aren't testing anything. Fix.

Fill assertions as implementation progresses:
  - One assertion per behavior
  - Test the contract, not implementation details
  - Include happy path + key error paths

Run tests → should PASS (GREEN)
  If FAIL → fix implementation or test, iterate
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
    // Assert
  })
})
```

**File location:** `e2e/` or `tests/e2e/` directory. Follow existing convention.

## Test Naming Conventions

| Framework | Convention | Example |
|-----------|-----------|---------|
| Vitest/Jest | `{module}.test.ts` | `auth.test.ts` |
| pytest | `test_{module}.py` | `test_auth.py` |
| Go | `{file}_test.go` | `auth_test.go` |
| Playwright | `{feature}.spec.ts` | `auth.spec.ts` |
| Cypress | `{feature}.cy.ts` | `auth.cy.ts` |

**Follow existing project conventions over these defaults.** Check 3+ existing test files for patterns.

## Rules

- **Scaffolds only** — agent generates structure, user owns assertions for complex logic
- **Always verify RED first** — a test that passes on empty assertions is useless
- **Follow existing conventions** — check 3+ existing tests before creating new ones
- **One test file per module** — don't scatter tests across files
- **Test behavior, not implementation** — assert outputs and effects, not internal calls
- **Mock only external APIs** — use real instances for internal dependencies
- **No test file without a reason** — every test must trace to a scope item or bug
