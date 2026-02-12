# Fix Action

> **Agent:** Load this file when `fix` triggers. Also load `references/quality-gates.md` for gate commands and `references/session-management.md` for resume/stuck detection.

Fix bugs with scientific debugging and anti-cascade TDD. Prevents cascading failures.

---

## When to Fix

- User reports a bug (symptom, reproduction steps)
- Bug found during feature implementation (ship's Bug Encounter Protocol hands off here)
- Regression detected in CI or test suite

## Bug Classification

| Type | Signal | Approach |
|------|--------|----------|
| Simple | Clear cause, single file | Skip Phase 1, go directly to Phase 2 |
| Complex | Unclear cause, multiple files, intermittent | Full Phase 1 (investigate) then Phase 2 |

## Flow

```
fix {bug description}
  │
  ▼
┌──────────────────────────────────────┐
│ CLASSIFY: simple or complex?         │
└──────────┬───────────────────────────┘
           │
     ┌─────┴─────┐
     │           │
  complex     simple
     │           │
     ▼           │
┌────────────┐   │
│ Phase 1:   │   │
│ INVESTIGATE│   │
│ (debug.md) │   │
└─────┬──────┘   │
      │          │
      ▼          ▼
┌──────────────────────────────────────┐
│ Phase 2: FIX (anti-cascade TDD)     │
│ BASELINE → RED → GREEN → DIFF →    │
│ BLOCK → SCAN → PREVENT              │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Phase 3: VALIDATE                    │
│ lint → typecheck → build → test     │
└──────────────────────────────────────┘
```

## Phase 1: INVESTIGATE (Complex Bugs Only)

Load [patterns/debugging.md](../patterns/debugging.md) for full method.

```
1. SYMPTOM CAPTURE
   - Exact error message/behavior
   - Steps to reproduce
   - When it started (last known good state)

2. HYPOTHESIS FORMATION
   Rank by likelihood:
   H1: {most likely cause} (probability: X%)
   H2: {second most likely} (probability: Y%)
   H3: {least likely} (probability: Z%)

3. TEST HYPOTHESES
   For each (highest probability first):
     Design minimal test → execute → CONFIRMED / ELIMINATED

4. BINARY SEARCH (if no hypothesis confirmed)
   git bisect or manual binary elimination

5. ROOT CAUSE CONFIRMATION
   Can you explain WHY it broke, not just WHERE?
```

**Key rule:** Never make a change without a hypothesis for why it will fix the bug.

## Phase 2: FIX (Anti-Cascade TDD)

All bug fixes follow this protocol. Full details: [regression-testing.md](../patterns/regression-testing.md).

```
1. BASELINE → Run full test suite, record pass/fail counts
2. RED      → Write test reproducing the bug (MUST FAIL)
3. GREEN    → Implement fix, verify regression test passes
4. DIFF     → Run full test suite again, compare to baseline
5. BLOCK    → Any NEW failures = fix introduced regressions → roll back, rethink
6. SCAN     → Check codebase for sibling bugs (same pattern)
```

**DIFF is the anti-cascade mechanism.** By comparing full suite results before and after, you catch any regression the fix introduces — before it cascades.

If fix introduces regressions (DIFF fails):
- Option A: Fix regressions without breaking the original fix
- Option B: Roll back, find a different approach
- Option C: Escalate to user with evidence

## Phase 3: VALIDATE

Same quality gates as ship. Load `references/quality-gates.md`.

**Full pass** (before marking complete):
- Lint changed files
- Typecheck full project
- Build full project
- Test related tests + anti-cascade DIFF

Auto-detect tooling from project files.

## Task Template

```
[ ] Classify bug (simple/complex)
[ ] INVESTIGATE: scientific debugging (complex only)
[ ] BASELINE: run full test suite, record results
[ ] RED: write failing regression test
[ ] GREEN: implement fix, verify test passes
[ ] DIFF: run full suite, compare to baseline (zero new failures)
[ ] SCAN: check codebase for sibling bugs
[ ] Full pass: lint + typecheck + build + test
[ ] Output summary
```

Update tasks as you work: mark in-progress when starting, complete when done. One task in-progress at a time.

## Acceptance Criteria

Auto-generate these ACs for any bug fix:

```
- AC-B1: GIVEN {reproduction steps} WHEN {trigger} THEN bug no longer occurs
- AC-B2: GIVEN regression test WHEN run against unfixed code THEN test FAILS (RED)
- AC-B3: GIVEN regression test WHEN run against fixed code THEN test PASSES (GREEN)
- AC-B4: GIVEN full test suite WHEN run after fix THEN no NEW failures vs baseline
```

AC-B2 + AC-B3 = TDD proof. AC-B4 = anti-cascade proof.

## Guard Rails

| Situation | Action |
|-----------|--------|
| No test suite exists | Propose setup (link to testing-automation.md). If declined, document and proceed manually |
| Test suite is partial (low coverage) | Warn: "Coverage is low near fix area. Baseline may miss regressions." |
| Tests are flaky (intermittent failures) | Run baseline 2x, use consistent results as anchor. Flag flaky tests. |
| Fix is trivial (typo, config) | Still run BASELINE + DIFF. Skip RED/GREEN only if no testable behavior change. |
| Emergency/hotfix | Run abbreviated: RED + GREEN + DIFF. Skip SCAN. Document skip. |
| User says "skip tests" | Document skip reason. Still run DIFF if suite exists (non-blocking). |

## Spec-First Enforcement

```
Has spec?
  YES → Continue
  NO  → Estimate size
    trivial (<5 LOC)  → Fix directly, no spec
    micro (<30 LOC)   → Create inline comment spec
    mini (<100 LOC)   → Create spec file (minimal)
    standard (100+)   → Create full spec (suggest `plan` first)
    emergency/hotfix   → Skip spec, log reason
```

## Session Management

Uses same state machine as ship (see [session-management.md](../session-management.md)).

Resume detects which phase was last completed:
- No progress → FRESH (start from classify)
- Phase 1 complete → Resume at Phase 2 (BASELINE)
- Mid-Phase 2 → Resume at last completed TDD step

## Output

Follow the output template in `references/templates/fix-output.md`.

## Intent Auto-Detection

| User Says | Agent Does |
|-----------|-----------|
| "emergency fix", "hotfix" | Skip spec ceremony, abbreviated TDD (RED + GREEN + DIFF) |
| "skip tests", "don't run tests" | Skip test gate (log reason) |
| "fix this too", "also fix" | Run SCAN-style sibling check |

Always document any skipped steps in output.

## Never

- Never auto-fix sibling bugs without user approval
- Never skip BASELINE + DIFF (anti-cascade core)
- Never make a change without a hypothesis (complex bugs)
- Never runs `git push`
- Never runs deploy commands
- Never makes production changes
- Never runs destructive git commands (`reset --hard`, `clean -f`, `push --force`)
