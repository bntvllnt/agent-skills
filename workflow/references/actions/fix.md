# Fix Action

> **Agent:** Load this file when `fix` triggers. Also load `references/quality-gates.md` for gate commands, `references/testing-automation.md` for E2E-first test generation + mock avoidance, `references/session-management.md` for resume/stuck detection, and `references/rules-discovery.md` — fixes must follow project/user rules.

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
| Complex | Unclear cause, multiple files, intermittent | Phase 1 (single-agent investigation) then Phase 2 |
| Highly complex | Cross-cutting, multiple possible root causes, reproduces inconsistently | Phase 1 with multi-agent parallel investigation then Phase 2 |

## State Machine

```
CLASSIFY → simple?         → BASELINE
CLASSIFY → complex?        → INVESTIGATE → CONFIRM → BASELINE
CLASSIFY → highly complex? → INVESTIGATE (parallel agents) → CONVERGE → CONFIRM → BASELINE

BASELINE → RED → GREEN → DIFF → BLOCK
  BLOCK [new failures] → ROLLBACK → rethink approach → BASELINE (max 3 cycles → ESCALATE)
  BLOCK [no new failures] → SCAN → LEARN → VALIDATE → DONE

INVESTIGATE → all hypotheses eliminated + bisect fails → ESCALATE
ESCALATE → present evidence to user → user decides next step
```

**States:**

| State | Entry condition | Exit condition | Next state |
|-------|----------------|----------------|------------|
| CLASSIFY | Fix triggered | Bug classified | INVESTIGATE (complex/highly complex) or BASELINE (simple) |
| INVESTIGATE | Complex or highly complex bug | Hypotheses tested, candidate root cause identified | CONFIRM (or ESCALATE if exhausted) |
| CONFIRM | Candidate root cause exists | Root cause passes 3-point validation | BASELINE |
| BASELINE | Investigation done (or simple bug) | Full suite results recorded | RED |
| RED | Baseline recorded | Regression test written and FAILS | GREEN |
| GREEN | RED test exists | Fix implemented, regression test PASSES | DIFF |
| DIFF | Fix passes regression test | Full suite re-run, compared to baseline | BLOCK |
| BLOCK | DIFF results available | Decision: new failures or not | SCAN (clean) or ROLLBACK (regressions, max 3) |
| ESCALATE | Investigation exhausted OR 3 rollback cycles | Evidence presented, user decides | User-directed (new approach, defer, or accept risk) |
| SCAN | No new failures | Sibling bugs searched, proposed to user | LEARN |
| LEARN | Scan complete | Spec updated + rules proposed, user approved/declined | VALIDATE |
| VALIDATE | Prevention done | All quality gates pass | DONE |

## Phase 1: INVESTIGATE (Complex and Highly Complex Bugs)

Load [patterns/debugging.md](../patterns/debugging.md) for full method.

### Step 1: SYMPTOM CAPTURE

```
Collect before doing anything else:
  - Exact error message / unexpected behavior
  - Steps to reproduce (minimal)
  - When it started (last known good state / commit)
  - Environment details (OS, runtime version, config)
  - Frequency: always / intermittent / once
```

### Step 2: HYPOTHESIS FORMATION

```
Generate ranked hypotheses:
  H1: {most likely cause} (probability: X%)
  H2: {second most likely} (probability: Y%)
  H3: {least likely} (probability: Z%)

Each hypothesis must:
  - Name a specific code path or condition
  - Be falsifiable (you can design a test that disproves it)
  - State what evidence would CONFIRM vs ELIMINATE it
```

**TypeScript projects with CI available** (augments code reading):

```
For suspect function/symbol:
  npx codebase-intelligence symbol --json <path> <name>
    → Callers, callees, type info — narrows hypothesis scope
  npx codebase-intelligence dependents --json <file>
    → Blast radius — what else could be affected by this bug?
If CI unavailable: use grep for callers/callees
See references/codebase-intelligence.md for full command reference.
```

### Step 3: TEST HYPOTHESES

For **complex** bugs: test each hypothesis sequentially, highest probability first.

For **highly complex** bugs: if the agent supports parallel execution (sub-agents, concurrent tool calls, or background tasks), investigate multiple hypotheses simultaneously. If not, investigate sequentially but assign a time box per hypothesis to avoid rabbit holes.

**TypeScript structural investigation** (if CI available):

```
npx codebase-intelligence processes --json <path>
  → Entry-point execution tracing — identifies code paths through suspect area
npx codebase-intelligence impact --json <path> <symbol>
  → Symbol-level blast radius — what breaks if this symbol behaves differently?
Feed these to investigation agents alongside hypothesis prompts.
If CI unavailable: agents use grep + manual code path tracing.
```

#### Highly Complex: Parallel Investigation

When the bug is cross-cutting, has multiple plausible root causes, or spans several systems, investigate from multiple perspectives at once.

**How to dispatch (adapt to your agent's capabilities):**

```
For each hypothesis, create a focused investigation task:

Task 1: "Investigate H1: {hypothesis}. Search for {pattern} in {area}.
  Report: evidence found, CONFIRMED or ELIMINATED, reasoning."

Task 2: "Investigate H2: {hypothesis}. Search for {pattern} in {area}.
  Report: evidence found, CONFIRMED or ELIMINATED, reasoning."

Task 3: "Investigate H3: {hypothesis}. Alternatively, explore
  {alternative angle — e.g., git history, dependency changes, config drift}.
  Report: evidence found, CONFIRMED or ELIMINATED, reasoning."

If agent supports sub-agents or parallel execution → run all tasks simultaneously.
If agent is single-threaded → run sequentially, time-box each to 15 min max.
```

**Agent perspective assignments (pick based on bug type):**

| Perspective | Focus | When to use |
|-------------|-------|-------------|
| Code path tracer | Follow execution path, find where behavior diverges | Logic bugs, wrong output |
| State inspector | Track state mutations, find unexpected side effects | State bugs, data corruption |
| History investigator | git log/bisect, find breaking change, review recent commits | Regressions, "it used to work" |
| Dependency auditor | Check dependency versions, breaking changes, API diffs | Post-upgrade bugs, integration issues |
| Concurrency analyzer | Identify shared state, race windows, timing dependencies | Intermittent bugs, deadlocks |
| Environment comparator | Diff configs, env vars, runtime versions across environments | "Works on my machine" bugs |

**Convergence protocol:**

```
Collect all agent results → synthesize:
  1. Which hypotheses were CONFIRMED? Which ELIMINATED?
  2. Do agents agree on root cause? If not, what's the conflict?
  3. If conflict → form new hypothesis from combined evidence → test directly
  4. If no hypothesis confirmed → escalate to BINARY SEARCH (Step 4)
```

### Step 4: BINARY SEARCH (if no hypothesis confirmed)

```
git bisect or manual binary elimination:
  Find last known good commit
  Bisect to identify breaking change
  Read the breaking commit → form new hypothesis → test
```

### Step 5: ESCALATE (if investigation exhausted)

If all hypotheses are eliminated AND binary search fails (or is not possible):

```
ESCALATE to user with:
  1. Summary of all hypotheses tested and evidence
  2. What was eliminated and why
  3. Remaining unknowns
  4. Recommended next steps:
     a) Bring in domain expert / pair debug
     b) Add instrumentation and wait for recurrence
     c) Accept risk and document as known issue
     d) Try different investigation angle (user suggests)
```

Do NOT loop back to Step 2 more than once after escalation. If the second round also fails → hard stop, present all evidence, let user decide.

### Step 6: ROOT CAUSE CONFIRMATION

Before proceeding to Phase 2, the root cause must pass **all 3 validation checks**:

```
Root Cause 3-Point Validation:

  1. EXPLAINS: Does it explain ALL observed symptoms (not just some)?
     Ask: "If this is the root cause, why does {symptom} happen?"
     Every symptom must have an answer. If any symptom is unexplained → dig deeper.

  2. PREDICTS: Does it predict the fix?
     Ask: "If I change {specific code}, will the bug stop AND no new issues appear?"
     Must be able to name the exact change. Vague fixes = wrong root cause.

  3. REPRODUCES: Can you make the bug appear and disappear at will?
     The reproduction case must:
       - FAIL without the fix (proves the root cause triggers the bug)
       - PASS with the fix (proves the fix addresses the root cause)
     If you can't toggle it → you found a correlation, not the cause.
```

**If any check fails:** Do NOT proceed to Phase 2. Go back to Step 2 with new evidence and form new hypotheses. If this is the second failed round → ESCALATE (Step 5).

**Key rule:** Never make a change without a hypothesis for why it will fix the bug.

## Phase 2: FIX (Anti-Cascade TDD)

All bug fixes follow this protocol. Full details: [regression-testing.md](../patterns/regression-testing.md).

```
1. BASELINE → Run full test suite, record pass/fail counts (BLOCKING)
2. RED      → Write E2E regression test reproducing the bug (MUST FAIL) (BLOCKING)
               Log RED_CONFIRMED in e2e-scenarios registry
               Use real systems — never mock own code (see testing-automation.md mock avoidance hierarchy)
               Even if bug is in a "unit-testable" function → E2E proves fix at system level
3. GREEN    → Implement fix, E2E regression test MUST PASS (BLOCKING)
               Log GREEN_CONFIRMED in e2e-scenarios registry
               No mocking own code — real DB, real server, real auth
4. DIFF     → Run full test suite again, compare to baseline (BLOCKING)
5. BLOCK    → Any NEW failures = fix introduced regressions → roll back, rethink (BLOCKING)
6. SCAN     → Check codebase for sibling bugs (same pattern) (advisory)
```

**All steps except SCAN are BLOCKING — cannot skip.**

**DIFF is the anti-cascade mechanism.** By comparing full suite results before and after, you catch any regression the fix introduces — before it cascades.

**Mock boundary:** Regression tests follow the same mock avoidance hierarchy as all tests (see `references/testing-automation.md`). DENY mocking own application code, own DB, own HTTP endpoints, own auth. ALLOW mocking only third-party APIs without sandbox/Docker/in-memory alternatives.

If fix introduces regressions (DIFF fails):
- Option A: Fix regressions without breaking the original fix
- Option B: Roll back, find a different approach
- Option C: Escalate to user with evidence

**ROLLBACK cap:** Max 3 BLOCK → ROLLBACK cycles. If the 3rd approach still introduces regressions → ESCALATE. Present all 3 attempts + their regressions to the user. Do not loop indefinitely.

## LEARN: Capture Learnings & Prevent Recurrence

After SCAN, capture what was learned so the same class of error doesn't recur. Two sub-steps: update the active spec (if one exists), then propose prevention rules for the agent's config files.

**When to run:** Non-trivial bugs with a generalizable root cause.
**When to skip:** Trivial bugs (typos, config), emergency/hotfix.

### Step 1: Update Active Spec

If the bug relates to an active spec in `specs/active/`, update it with the fix details.

**1a. Check for active spec.**

```
Read specs/active/ directory
  Files found? → Continue to 1b
  Empty? → Skip to Step 2
```

**1b. Determine if bug relates to the active spec.**

Read the spec file. Check:
- Does the bug affect a scope item in this spec?
- Was the bug found during implementation of this spec?
- Does the fix change behavior described in the spec's ACs?

If YES to any → continue. If NO to all → skip to Step 2.

**1c. Log the bug in the spec.**

Open the spec file. Find or create `## Encountered Bugs` section. Append:

```markdown
BUG-{N}: {1-line summary}
- **Root cause:** {why it happened}
- **Fix:** {what was changed}
- **Status:** Fixed
- **Regression test:** {test file}:{test name} (E2E)
- **Registry:** AC-B1 through AC-B4 in e2e-scenarios.md — RED_CONFIRMED + GREEN_CONFIRMED
```

**1d. Update spec Progress section.**

Find the `## Progress` table. If the bug blocked a scope item, update its status:
- Was `[!] Blocked` → change to `[~] In progress` or `[x] Complete`
- Add note: `Fixed via BUG-{N}`

**1e. Update ACs if fix changed behavior.**

If the fix changed how a feature works (not just a bug in implementation):
- Update affected GIVEN/WHEN/THEN ACs to match new behavior
- Add new AC if the fix introduced a new user-observable behavior
- Run traceability check: every scope item maps to an AC, no orphans

### Step 2: Propose Prevention Rules

Propose rule updates to the agent's config files so the same class of error doesn't happen again.

**When to skip this step:** Existing rule already covers it, or root cause is too specific to generalize.

**2a. Identify the root cause category.**

Look at the confirmed root cause from INVESTIGATE or GREEN phase. Map it:

| Root Cause | Category | Example Rule |
|-----------|----------|-------------|
| Missing null/undefined check | Coding rule | "Always null-check optional fields before access" |
| Wrong type assumption | Coding rule | "Use discriminated unions, never assume shape" |
| Missing validation at boundary | Quality check | "Validate external input at API boundaries" |
| Incorrect error handling | Anti-pattern | "Never swallow errors in catch blocks" |
| Race condition / shared state | Coding rule | "Wrap shared state mutations in transactions" |
| Missing edge case | Quality check | "Test empty/null/boundary inputs for public functions" |
| Config/env assumption | Quality check | "Validate required env vars at startup" |

**2b. Read existing agent rules.**

Detect which agent CLI is running, then read all config files at both project and user level. Use the **Agent Config Targets** table in [memory-update.md](../memory-update.md) to resolve the correct file paths for the detected agent.

If the root cause is already covered by an existing rule at any level → **SKIP**. Do not propose duplicates.

**2c. Draft max 2 proposals.**

Write each proposal in this exact format:
```
[{target file} § {section}] {type}: "{rule text}"
_Prevents: {class of error}_
```

Target file routing (resolve via [memory-update.md](../memory-update.md) Agent Config Targets table):
- Project-specific patterns → agent's project-level config
- Universal patterns → agent's user-level config
- Unknown agent → `{project}/AGENTS.md` (universal fallback)

Categories allowed: `rule` (coding rules), `anti-pattern`, `quality-check`.

See [memory-update.md](../memory-update.md) **Proposal Format Examples** for per-agent targeting (Claude Code, Cursor, Windsurf, Codex, OpenCode, etc.).

**2d. Present to user for approval.**

If agent has multi-select UI (AskUserQuestion or equivalent):
```
question: "Save prevention rules from this fix?"
multiSelect: true
options:
  - label: "#1 {short summary}"
    description: "[{target file} § {section}] {type}: {rule text}"
  - label: "#2 {short summary}"
    description: "[{target file} § {section}] {type}: {rule text}"
```

If no multi-select UI (fallback):
```
Prevention rules from this fix:
1. [{target file} § {section}] {type}: "{rule text}"
   _Prevents: {class of error}_
2. [{target file} § {section}] {type}: "{rule text}"
   _Prevents: {class of error}_

Apply which? [all / 1,2 / none]
```

**2e. Apply approved rules.**

For each approved proposal:
1. Open the target file
2. Find the target section
3. Append the rule text
4. Confirm write to user

Declined proposals → log in output, take no action.

### LEARN Rules

- Max 2 rule proposals per fix
- Advisory, not blocking — user can decline with no gate failure
- Never auto-apply — always get explicit user approval before writing rules
- Never propose vague rules ("be more careful") — must be specific and actionable
- Spec updates don't require approval (they log facts, not opinions)

## Phase 3: VALIDATE

Same quality gates as ship. Load `references/quality-gates.md`.

**Full pass** (before marking complete — all 6 gates + TDD proof):

| # | Gate | Scope | Level |
|---|------|-------|-------|
| 1 | Lint | Changed files | BLOCKING |
| 2 | Typecheck | Full project | BLOCKING |
| 3 | Build | Full project | BLOCKING |
| 4 | Test | Related tests + anti-cascade DIFF | BLOCKING |
| 5 | E2E registry | All bug fix ACs (AC-B1 through AC-B4) GREEN_CONFIRMED | BLOCKING |
| 6 | TDD proof | Every GREEN_CONFIRMED has prior RED_CONFIRMED | BLOCKING |
| 7 | Coverage | Advisory — warn on >5% drop | ADVISORY |

Auto-detect tooling from project files. See `references/quality-gates.md`.

## Task Tracking (Use Agent Capabilities)

If your agent has built-in task/todo tracking (TaskCreate, TaskUpdate, etc.), use it to track each phase. Create tasks at the start, update status as you progress.

```
[ ] Classify bug (simple/complex/highly complex)
[ ] INVESTIGATE: scientific debugging (complex/highly complex)
[ ] CONFIRM: root cause passes 3-point validation
[ ] BASELINE: run full test suite, record results (BLOCKING)
[ ] Create e2e-scenarios.md registry entries for bug fix ACs (AC-B1 through AC-B4)
[ ] RED: write E2E regression test → MUST FAIL → log RED_CONFIRMED (BLOCKING)
[ ] GREEN: implement fix → E2E test MUST PASS → log GREEN_CONFIRMED (BLOCKING)
[ ] DIFF: run full suite, compare to baseline (zero new failures) (BLOCKING)
[ ] Mock audit: verify no mocking of own code in regression test
[ ] SCAN: check codebase for sibling bugs
[ ] LEARN: update spec (if related) + propose prevention rules
[ ] Full pass: lint + typecheck + build + test + E2E registry + TDD proof + coverage
[ ] Output summary
```

Update tasks as you work: mark in-progress when starting, complete when done. One task in-progress at a time.

**If agent lacks task tracking:** Track progress in the spec's Progress section instead.

## Acceptance Criteria

Auto-generate these ACs for any bug fix:

```
- AC-B1: GIVEN {reproduction steps} WHEN {trigger} THEN bug no longer occurs
- AC-B2: GIVEN E2E regression test WHEN run against unfixed code THEN test FAILS (RED_CONFIRMED in registry)
- AC-B3: GIVEN E2E regression test WHEN run against fixed code THEN test PASSES (GREEN_CONFIRMED in registry)
- AC-B4: GIVEN full test suite WHEN run after fix THEN no NEW failures vs baseline (DIFF clean)
```

AC-B2 + AC-B3 = TDD proof (tracked in `e2e-scenarios.md` registry). AC-B4 = anti-cascade proof.

All bug fix ACs are registered in `e2e-scenarios.md` with type prefix `AC-BN`. See `references/e2e-scenarios.md` for registry format.

## Guard Rails

| Situation | Action |
|-----------|--------|
| No test suite exists | Propose setup (load testing-automation.md for recommendation). If declined, document and downgrade E2E gate to ADVISORY |
| No E2E framework exists | Propose E2E framework setup (Playwright/Cypress/Maestro/Detox per stack). If declined, downgrade E2E gate to ADVISORY for this session |
| Test suite is partial (low coverage) | Warn: "Coverage is low near fix area. Baseline may miss regressions." |
| Tests are flaky (intermittent failures) | Run baseline 2x, use consistent results as anchor. Flag flaky tests. |
| Fix is trivial (typo, config) | Still run BASELINE + DIFF. Skip RED/GREEN only if no testable behavior change. |
| Emergency/hotfix | Run abbreviated: RED + GREEN + DIFF. Skip SCAN. Document skip. |
| User says "skip tests" | Document skip reason. Still run DIFF if suite exists (non-blocking). |
| Non-deterministic bug (race condition, heisenbug) | Use Concurrency analyzer perspective. RED test may need stress/repeated runs. If can't reproduce reliably → document conditions, write best-effort test, note uncertainty. |
| Can't reproduce locally | Skip RED (can't write failing test). Investigate via logs/history/code review. Propose fix based on code analysis. Run DIFF to ensure no regressions. Document that RED was skipped and why. |
| Root cause is in dependency | Document dependency + version. Propose workaround (pin version, patch, or wrapper). Do NOT attempt to fix external code. File upstream issue if applicable. |
| Investigation exhausted (no root cause found) | ESCALATE with all evidence. Do NOT guess-and-fix. Present hypotheses tested + results to user. |

## Time Limits

### Investigation Time-Box

| Bug Type | Max Investigation Time | Max Hypotheses | Escalation |
|----------|----------------------|----------------|------------|
| Simple | N/A (skip Phase 1) | N/A | — |
| Complex | 30 min | 5 | ESCALATE with evidence |
| Highly complex | 60 min | 8 (across all agents) | ESCALATE with evidence |

If time-box expires without confirmed root cause → ESCALATE (Step 5). Do not continue investigating indefinitely.

### Fix Iteration Limits

| Bug Complexity | Max ROLLBACK Cycles | Max Total Fix Time |
|----------------|--------------------|--------------------|
| Simple | 2 | 30 min |
| Complex | 3 | 60 min |
| Highly complex | 3 | 90 min |

Exceeding any limit → ESCALATE to user with all evidence collected.

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
- Never auto-apply prevention rules — always propose, user approves (LEARN step)
- Never propose more than 2 prevention rules per fix (LEARN step)
- Never skip BASELINE + DIFF (anti-cascade core)
- Never make a change without a hypothesis (complex bugs)
- Never runs `git push`
- Never runs deploy commands
- Never makes production changes
- Never runs destructive git commands (`reset --hard`, `clean -f`, `push --force`)
