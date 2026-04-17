# Ship Action

> **Agent:** Load this file when `ship` triggers. Also load `references/quality-gates.md` for gate commands, `references/session-management.md` for resume/stuck detection, and `references/rules-discovery.md` — code must follow project/user rules.

Implement features with a build/review/fix loop. Handles both quick one-shot and iterative spec-driven work.

**Bug fix?** Use the `fix` action instead. See [fix.md](fix.md).

---

## Mode Detection

```
Active spec in specs/active/?
  YES → LOOP mode (iterate until spec complete)
  NO  → ONE-SHOT mode (create inline spec, implement, validate)
```

## Task Tracking (MANDATORY for mini/standard)

Before starting any implementation, create tasks in your agent's built-in task/todo system. Track what to build AND what to validate.

**Create these tasks at the start of each ship cycle:**
```
[ ] {scope item 1} → AC-{N}
[ ] {scope item 2} → AC-{N}
[ ] ...
[ ] Create e2e-scenarios.md registry from spec ACs
[ ] Generate E2E tests (TDD: RED before implementation)
[ ] Quick pass: lint + typecheck (changed files)
[ ] Review: run perspectives
[ ] Fix BLOCKING issues
[ ] Full pass: lint (changed) + typecheck (full) + build (full) + test (related) + E2E (registry) + coverage (advisory)
[ ] Exit check: all Must Have ACs + Error ACs + scope items + e2e_coverage passing
```

Update tasks as you work: mark in-progress when starting, complete when done. One task in-progress at a time.

## Phase 0: Setup

1. **Detect project stack** (monorepo, framework, test runner, linter, E2E framework)
1b. **TypeScript structural analysis** (if `tsconfig.json` detected):
    Load `references/codebase-intelligence.md`, run detection gate.
    Run: `npx codebase-intelligence overview --json <project-root>`
    → Augments stack detection with module structure, dependency graph, file metrics.
    If CI unavailable: proceed with standard stack detection only.
2. **Validate test environment:**
   - Load spec's Test Strategy (from plan phase, if exists)
   - If no Test Strategy: run test setup discovery now (load references/testing-automation.md)
   - If no E2E infra detected: PROPOSE setup to user with specific recommendation
   - If user declines: document, downgrade E2E gate to ADVISORY for this session
   - If user accepts: install + configure before first iteration
   - Validate mock avoidance plan: check if proposed mocks can use real alternatives
3. **Load active spec** (if LOOP mode) or create inline spec (ONE-SHOT)
4. **Detect resume state** (see session-management.md):
   - FRESH: No prior work — start from beginning
   - RESUMING: Prior progress found — resume from last checkpoint
   - STUCK: Multiple failed iterations — escalate
   - READY_FOR_DONE: All scope complete — suggest `done`

## Spec-First Enforcement

```
Has spec?
  YES → Continue
  NO  → Estimate size
    trivial (<5 LOC)  → Implement directly, no spec
    micro (<30 LOC)   → Create inline comment spec
    mini (<100 LOC)   → Create spec file (minimal)
    standard (100+)   → Create full spec (suggest `plan` first)
    emergency/hotfix   → Skip spec, log reason
```

## ONE-SHOT Flow

For quick fixes and small features without an active spec:

```
1. Analyze scope (files affected, estimated LOC)
1b. **TypeScript scope analysis** (if CI available):
    `npx codebase-intelligence dependents --json <file>` for each affected file → reveals non-obvious consumers.
    For refactoring: `npx codebase-intelligence rename --json <path> <symbol>` → discovers all references before changes.
    If CI unavailable: use grep for scope analysis.
2. Run test setup discovery (load references/testing-automation.md)
3. Create plan (brief, inline)
4. Write E2E test for key behavior (RED — MUST FAIL)
5. Implement
6. Run E2E test (GREEN — MUST PASS)
7. Quality gates (lint → typecheck → build → test → E2E → coverage)
8. Self-review (re-read all changes)
9. Output summary
```

## LOOP Flow (Ship Loop)

Core iteration algorithm for spec-driven work:

```
iteration = 0
max_iterations = spec.max_iterations OR default_by_size()
stuck_threshold = max(3, max_iterations / 2)

WHILE iteration < max_iterations:
  iteration++

  # 1. SELECT
  Pick next unchecked scope item

  # 1b. TDD-ENFORCED TEST GENERATION (BEFORE implementation)
  Load ACs + Test Strategy for current scope item
  Create e2e-scenarios.md registry entries if not exists (iteration 1)
  Write E2E test asserting correct behavior (use real systems per mock avoidance hierarchy)
  Run test → MUST FAIL (RED). Log RED_CONFIRMED in registry.
    If PASS → wrong test — rewrite to test new behavior
  Implement scope item (minimal — just enough to pass)
  Run test → MUST PASS (GREEN). Log GREEN_CONFIRMED in registry.
    If FAIL → fix implementation, not test
  Refactor if needed → re-run → still PASS
  Mock audit: if any mock added, verify it follows avoidance hierarchy

  Run quick quality pass (lint + typecheck on changed files)
  Mark scope item [x] if passing

  # 2. REVIEW (every 2-3 iterations or on request)
  Run multi-perspective review (see actions/review.md)
  Collect issues: BLOCKING vs WARN

  # 3. FIX
  Fix all BLOCKING issues
  Log WARN issues in spec notes

  # 4. EXIT CHECK
  all_must_have_acs = all Must Have ACs checked [x]
  all_error_acs = all Error Criteria ACs checked [x]
  all_scope_complete = all spec scope items checked [x]
  quality_clean = lint + typecheck + build + test all pass
  e2e_coverage = all BLOCKING e2e-scenarios entries GREEN_CONFIRMED
  tdd_proof = every GREEN_CONFIRMED has prior RED_CONFIRMED
  no_blockers = no BLOCKING review issues

  IF all_must_have_acs AND all_error_acs AND all_scope_complete
     AND quality_clean AND e2e_coverage AND tdd_proof AND no_blockers:
    EXIT → clean (suggest `done`)

  # ACs are the source of truth for "is work done?"
  # Scope items track implementation progress.
  # Both must be complete.

  # 5. STUCK DETECTION
  progress = scope_items_completed / total_scope_items
  IF iteration >= stuck_threshold AND progress < 0.5:
    ESCALATE (see Stuck Escalation below)
```

### Default Iterations by Size

| Size | Max Iterations | Stuck Threshold |
|------|---------------|-----------------|
| mini | 5 | 3 |
| standard (small) | 8 | 4 |
| standard (medium) | 12 | 6 |
| standard (large) | 20 | 10 |

## Quality Gates (Per Iteration)

**Quick pass** (after each edit batch):
- Lint changed files
- Typecheck changed files

**E2E pass** (after each scope item TDD cycle):
- Verify RED_CONFIRMED logged for current AC
- Verify GREEN_CONFIRMED logged after implementation
- Mock audit: no new mocks of own code

**Full pass** (before exit):
- Lint changed files
- Typecheck full project
- Build full project
- Test related tests
- E2E registry validation (all BLOCKING entries GREEN_CONFIRMED)
- TDD proof (every GREEN has prior RED)
- Coverage check (advisory — warn on >5% drop)

Auto-detect tooling from project files. See `references/quality-gates.md`.

## Stuck Escalation

Three levels, triggered by lack of progress:

| Level | Trigger | Action |
|-------|---------|--------|
| Warning | At stuck_threshold, progress < 50% | Log warning, continue |
| Pause | 2 iterations after warning, no progress | Present options to user |
| Hard stop | At max_iterations | Force exit with summary |

**Pause options:**
1. Continue with different approach
2. Reduce scope (cut items)
3. Defer to next session
4. Drop feature entirely

## Bug Encounter Protocol

When a bug is found during feature implementation:

```
1. Log bug in spec under "## Encountered Bugs"
   Format: BUG-{N}: {summary} | Status: Investigating/Fixed/Deferred
2. Classify: blocks current scope item? (Y/N)
3. If blocking: pause ship, run `fix` action (see fix.md)
4. If non-blocking: defer, continue with scope
5. All bugs must be Fixed or Deferred before `done`
```

**Resume after fix:** When the `fix` action completes, it updates the spec's Encountered Bugs section and Progress table (LEARN step). Ship resumes automatically:

```
fix completes → spec updated with BUG-{N} status: Fixed
  → ship detects RESUMING state (session-management.md)
  → reads spec Progress section
  → finds first non-[x] scope item
  → continues implementation from that point
  → runs quick quality pass before continuing
```

The handoff is seamless because both actions share the same spec file and session management state machine.

## Review Integration

Review runs automatically during ship loop. Perspectives:

**Core (always):** Correctness, Security, Reliability, Performance, DX
**Conditional:** Scalability, Observability, Testability, Accessibility

See `actions/review.md` for full perspective details.

## Progress Tracking

Update spec after each iteration:

```markdown
## Progress
| Item | Status | Iteration |
|------|--------|-----------|
| Scope item 1 | [x] Complete | 2 |
| Scope item 2 | [~] In progress | 3 |
| Scope item 3 | [ ] Pending | - |
```

## Output

Follow the output template in `references/templates/ship-output.md`.

Covers: iteration output, 4 exit states (clean/partial/stuck/hard stop), spec mutation output.

Exit states:

| State | Condition |
|-------|-----------|
| Clean | All Must Have + Error ACs pass, all scope done, gates green (6 gates), e2e_coverage 100%, tdd_proof clean, no blockers |
| Partial | Scope done but ACs failing |
| Stuck | Hit stuck threshold, user chose to stop |
| Hard stop | Hit max iterations |

## Risk Flag System

After each implementation step, assess risk level of changes:

```
For each changed file, check:
  Auth/security logic?        → HIGH
  DB schema/migration?        → HIGH
  Payment/billing?            → HIGH
  Public API contract?        → HIGH
  Delete/destructive op?      → HIGH
  Config/environment?         → MEDIUM
  New dependency?             → MEDIUM
  Performance-critical path?  → MEDIUM
  Internal refactor?          → LOW
  Tests/docs only?            → LOW

  Highest risk across all changes = overall risk
```

| Risk | Action |
|------|--------|
| LOW | Continue autonomously |
| MEDIUM | Note in spec, mention in self-review |
| HIGH | **PAUSE.** Present to user: what changed, what could go wrong, recommendation. User approves before continuing. |

Configurable by editing this file directly.

## Production Validation

Concrete checks for production deploys. Run these in addition to standard gates.

```
Auto-detect and run (if tooling exists):

1. Dependency vulnerability scan
   npm audit / pnpm audit / yarn audit / pip-audit / cargo audit
   Level: BLOCKING (critical/high), ADVISORY (moderate/low)

2. Security scan
   Check for: hardcoded secrets, SQL injection patterns,
   XSS vectors, open redirects, insecure dependencies
   Level: BLOCKING

3. Build verification
   Full production build (not dev build)
   Command: {framework build command} with production flags
   Level: BLOCKING

4. Smoke test (if test infrastructure supports it)
   Start server, hit health endpoint, verify response
   Level: ADVISORY

5. Bundle/artifact size check
   Compare to previous build if baseline exists
   Level: ADVISORY (warn if >20% increase)

6. Schema validation (if schema files changed)
   Verify migration is reversible
   Check for breaking changes in API contracts
   Level: BLOCKING
```

## Intent Auto-Detection

No flags needed. The agent detects intent from natural language:

| User Says | Agent Does |
|-----------|-----------|
| "emergency fix", "hotfix" | Route to `fix` action with abbreviated mode |
| "skip tests", "don't run tests" | Skip test gate (log reason) |
| "skip review" | Skip review perspectives |
| "deploy to production", "production ready" | Run production validation |
| "force it", "proceed anyway" | Proceed past CONDITIONAL readiness |

Always document any skipped gates in output.

## Parallel Execution

When scope items are independent (no shared files), they can be implemented in parallel if your agent supports multi-tool or concurrent execution.

```
Check: Do scope items share files in Codebase Impact?
  NO shared files → parallelizable (implement simultaneously)
  YES shared files → sequential (implement in order)

Parallel rules:
  - Each parallel item gets its own quick pass
  - Merge results before running full pass
  - If parallel items conflict at merge → resolve, re-run quick pass
  - Review runs once after all parallel items complete
```

## Spec Mutation Protocol (Mid-Loop Changes)

When user requests scope changes during the ship loop:

```
User: "also add X" / "change Y to Z" / "remove W"
  │
  ├─ 1. PAUSE current implementation
  ├─ 2. UPDATE SPEC FILE:
  │     - Add/modify/remove scope items
  │     - Add/modify acceptance criteria (GIVEN/WHEN/THEN)
  │     - Update user journey if flow changes
  │     - Re-run traceability check (scope ↔ AC, no orphans)
  │     - Update Progress section
  ├─ 3. UPDATE TASKS: create new, delete obsolete
  ├─ 4. RE-ASSESS: does change affect tier, iteration limit, or risk?
  ├─ 5. RESUME ship loop with updated scope
  │
  └─ RULE: Never implement untracked work.
           If it's not in the spec, update the spec first.
```

The spec is the SINGLE SOURCE OF TRUTH. It must reflect reality at all times.

## Never

- Never runs `git push`
- Never runs deploy commands
- Never makes production changes
- Never runs destructive git commands (`reset --hard`, `clean -f`, `push --force`)
