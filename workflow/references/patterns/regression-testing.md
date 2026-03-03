# Regression Testing Patterns

> **Agent:** Load this file during bug fix flows. Enforces anti-cascade TDD: fix A without breaking B.

Core problem: fix A → breaks B → fix B → breaks C. This protocol breaks that cascade.

---

## Anti-Cascade TDD Protocol

```
1. BASELINE  → Run full test suite, record pass/fail counts (BLOCKING)
2. RED       → Write E2E regression test reproducing bug (MUST FAIL) (BLOCKING)
3. GREEN     → Implement fix, E2E test MUST PASS, no mocking own code (BLOCKING)
4. DIFF      → Run full test suite again, compare to baseline (BLOCKING)
5. BLOCK     → Any NEW failures = BLOCKING — rollback or fix regressions, no workaround
6. SCAN      → Check codebase for sibling bugs (same pattern)
7. PREVENT   → Propose rules to prevent this class of bug (max 2)
```

### Step-by-Step

**1. BASELINE** — Capture the world before touching anything.

```
Run full test suite → record:
  - Total tests: {N}
  - Passing: {N}
  - Failing: {N} (list failing test names)
  - Skipped: {N}

Store as baseline. This is your diff anchor.
```

If no test suite exists → propose setup (see [testing-automation.md](../testing-automation.md)). If user declines → document skip, proceed with manual verification.

**2. RED** — Prove the bug exists in E2E test form.

```
Write E2E test that:
  - Reproduces the exact bug scenario end-to-end (real systems, no mocks of own code)
  - Asserts the CORRECT behavior (what should happen)
  - MUST FAIL against current code
  - Uses real DB, real server, real auth — follows mock avoidance hierarchy

Run test → confirm FAIL
  If test PASSES → wrong test. Bug not reproduced. Redo.
  Log RED_CONFIRMED in e2e-scenarios registry.
```

Regression tests must be E2E even if the bug is in a "unit-testable" function — proves the fix works at system level, not just function level.

**3. GREEN** — Fix the bug, nothing more.

```
Implement minimal fix
Run E2E regression test → MUST PASS
  No mocking own code — real system must pass
  If FAIL → fix implementation, not the test. Iterate.
  Log GREEN_CONFIRMED in e2e-scenarios registry.
```

**4. DIFF** — Catch regressions immediately.

```
Run full test suite again → record:
  - Total tests: {N+1} (added regression test)
  - Passing: {N}
  - Failing: {N}

Compare to BASELINE:
  - New failures (tests that passed in baseline, fail now) = REGRESSIONS
  - Pre-existing failures (failed in baseline too) = KNOWN ISSUES (ignore)
```

**5. BLOCK** — Zero tolerance for new failures. BLOCKING — no workaround.

```
New failures found?
  YES → BLOCKING. Fix introduced regressions. Must resolve before proceeding.
        Options:
        a) Fix the regressions without breaking the original fix
        b) Roll back fix, find a different approach
        c) Escalate to user with evidence
        NO option to skip or proceed with regressions.
  NO  → PASS. Fix is safe. Continue.
```

**6. SCAN** — Find sibling bugs.

```
Search codebase for same pattern that caused the bug:
  - Same function/method used incorrectly elsewhere
  - Same assumption made in sibling files
  - Same missing validation in similar code paths

If siblings found → propose batch fix to user:
  "Same pattern exists in {files}. Fix those too? [y/n]"

Do NOT auto-fix siblings. Propose only.
```

**7. PREVENT** — Propose rules to prevent this class of bug.

**When to run:** After SCAN, for non-trivial bugs with a generalizable root cause.

**When to skip:**
- Trivial bugs (typos, config one-liners, obvious mistakes)
- Existing rule already covers this class of error
- Emergency/hotfix (speed > prevention)

```
Protocol:

1. CLASSIFY root cause → map to prevention category (see table below)
2. GENERATE max 2 proposals → concise, actionable rules
3. CHECK existing rules → read user/project rules, skip if covered
4. PROPOSE inline → user approves/declines immediately

Output format per proposal:
  [{target file} § {section}] {type}: "{rule text}"
  _Prevents: {class of error}_
```

**Root cause → prevention category:**

| Root Cause | Prevention Category | Example Rule |
|-----------|-------------------|-------------|
| Missing null/undefined check | Coding rule | "Always null-check optional fields before access" |
| Wrong type assumption | Coding rule | "Use discriminated unions for API responses, never assume shape" |
| Missing validation at boundary | Quality check | "Validate all external input at API boundaries with Zod" |
| Incorrect error handling | Anti-pattern | "Never swallow errors in catch blocks — rethrow or log with context" |
| Race condition / shared state | Coding rule | "Wrap shared state mutations in transactions or locks" |
| Missing edge case | Quality check | "Test empty/null/boundary inputs for all public functions" |
| Wrong API usage | Anti-pattern | "Never call {API} without {required precondition}" |
| Config/env assumption | Quality check | "Validate required env vars at startup, fail fast if missing" |

**Proposal rules:**
- Max 2 proposals per fix — keeps it lightweight
- Categories: coding rules, anti-patterns, quality checks only (no process/thinking patterns)
- Advisory, not blocking — user can decline with no gate failure
- Uses same targeting logic as memory-update.md (project CLAUDE.md, user rules, AGENTS.md)
- Never auto-apply — always propose, user approves

## Bug Type → Test Pattern Matrix

| Bug Type | Test Type | Test Pattern | What to Assert |
|----------|-----------|-------------|----------------|
| **Null/undefined handling** | E2E | Trigger null scenario via user action or API call | System handles gracefully — error message or safe default |
| **Off-by-one** | E2E | Test boundary values through real system path | Correct result at each boundary in system output |
| **Race condition** | E2E | Simulate concurrent access (parallel API calls, multi-tab) | Consistent state after concurrent operations |
| **Auth bypass** | E2E | Call endpoint without valid credentials via real HTTP | Returns 401/403, no data leaked, redirect works |
| **State mutation** | E2E | Perform operation through UI/API, verify all related state | Only intended state changed in real DB/store |
| **Validation gap** | E2E | Submit malformed input through real form/API | Rejected with clear error, no processing, user sees message |
| **Type coercion** | E2E | Submit wrong types through real input path | Proper error or safe coercion in system output |
| **Resource leak** | E2E | Trigger error path through real system, check cleanup | Resource cleaned up (connection closed, file handle released) |
| **Pure function bug** | E2E* | *Still E2E — proves fix at system level, not just function level | System-level output correct after fix |

*Even bugs in pure functions get E2E regression tests — proves the fix works at the integration level where users actually experience the bug.

## Mock Boundary for Regression Tests

Regression tests follow the same mock avoidance hierarchy as all tests:
- **NEVER mock**: own code, own DB, own endpoints, own auth, internal calls
- **ALLOW mock**: third-party APIs without sandbox (last resort only)
- Every mock requires `// MOCK: {reason real system not available}` comment

See [testing-automation.md](../testing-automation.md) for full mock avoidance hierarchy.

## Sibling Bug Detection

After fixing a bug, scan for the same pattern:

```
1. Identify the ROOT CAUSE pattern (not the symptom)
   e.g., "missing null check on user.email" → pattern: "accessing user.email without null check"

2. Search codebase:
   - Grep for same property/method access pattern
   - Check sibling files (same directory, same module)
   - Check callers of the same function

3. Filter results:
   - Already has null check / validation → SAFE
   - Missing same check → POTENTIAL SIBLING BUG

4. Report:
   "Found {N} locations with same pattern:
    - {file}:{line} — {context}
    Fix all? [y/n / select]"
```

## Guard Rails

| Situation | Action |
|-----------|--------|
| No test suite exists | Propose setup (link to testing-automation.md). If declined → document, proceed manually |
| Test suite is partial (low coverage) | Warn: "Coverage is low near fix area. Baseline may miss regressions." |
| Tests are flaky (intermittent failures) | Run baseline 2x, use consistent results as anchor. Flag flaky tests. |
| Fix is trivial (typo, config) | Still run BASELINE + DIFF. Skip RED/GREEN only if no testable behavior change. |
| Emergency/hotfix | Run abbreviated: RED + GREEN + DIFF. Skip SCAN. Document skip. |
| User says "skip tests" | Document skip reason. Still run DIFF if suite exists (non-blocking). |

## Acceptance Criteria (Bug Mode)

Auto-generate these ACs for any bug fix:

```
- AC-B1: GIVEN {reproduction steps} WHEN {trigger} THEN bug no longer occurs
- AC-B2: GIVEN regression test WHEN run against unfixed code THEN test FAILS (RED)
- AC-B3: GIVEN regression test WHEN run against fixed code THEN test PASSES (GREEN)
- AC-B4: GIVEN full test suite WHEN run after fix THEN no NEW failures vs baseline
```

AC-B2 + AC-B3 = TDD proof. AC-B4 = anti-cascade proof.

## Anti-Patterns (NEVER)

- NEVER fix a bug without running the full suite before AND after
- NEVER ignore new test failures ("they're probably unrelated")
- NEVER write a regression test that passes on the broken code
- NEVER skip SCAN for non-emergency fixes
- NEVER auto-fix sibling bugs without user approval
- NEVER treat flaky tests as "acceptable" — flag them
- NEVER propose more than 2 prevention rules per fix
- NEVER auto-apply prevention rules — always propose, user approves
- NEVER propose vague rules ("be more careful") — must be specific and actionable
- NEVER duplicate existing rules — check before proposing
- NEVER write a unit test when an E2E test is possible — system-level proof required
- NEVER mock own code in regression tests — real system must pass
