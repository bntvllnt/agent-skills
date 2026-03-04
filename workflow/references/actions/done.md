# Done Action

> **Agent:** Load this file when `done` triggers. Read the user's agent config (global + project rules) before proposing memory updates.

Validate, archive spec, capture learnings. Does NOT deploy — that's human-controlled.

---

## Step 1: Pre-Ship Validation

### Quality Gate

| Check | Required |
|-------|----------|
| All Must Have ACs passing [x] | Yes (MANDATORY) |
| All Error Criteria ACs passing [x] | Yes (MANDATORY) |
| All scope items checked [x] | Yes |
| Ship exit was CLEAN (not partial/stuck/hard-stop) | Yes |
| New tests for new behavior (E2E default) | Yes (BLOCKING) |
| Existing tests passing | Yes |
| No typecheck/lint errors | Yes |
| No debug statements (console.log, debugger, print, pdb, etc.) | Yes |
| No hardcoded secrets | Yes |
| Can rollback (git revert works, no irreversible migrations) | Yes |
| No unresolved bugs (all fixed or deferred) | Yes |
| E2E scenario registry: 100% Must Have + Error AC coverage | Yes (BLOCKING) |
| TDD proof: every AC has RED_CONFIRMED + GREEN_CONFIRMED | Yes (BLOCKING) |
| Mock boundary: no mocks of own code in new tests | Yes (BLOCKING) |
| Bug regressions: AC-B2 (RED) + AC-B3 (GREEN) + AC-B4 (DIFF) confirmed | Yes (BLOCKING, bug fixes only) |
| Coverage threshold met | Advisory |
| Agent docs updated for critical learnings | Advisory |

**New test mandate:** Every new behavior MUST have at least one E2E test (unit only for pure functions). Tests must follow TDD: RED_CONFIRMED before GREEN_CONFIRMED. No mocking of own code — real systems required. If E2E infrastructure doesn't exist, propose setting it up. If user declines, document the skip and downgrade E2E gate to ADVISORY.

ACs are the definition of DONE. Scope items track implementation tasks, but ACs determine if the feature actually works as specified in the user journey.

If any check fails: STOP. Show what's remaining. Suggest `ship` to continue.

### Step 1.5: E2E Coverage + TDD Validation (BLOCKING)

```
validate_e2e_coverage(spec, registry):
  # Registry exists?
  IF not exists(registry):
    IF spec.tier in [trivial, micro]: SKIP
    IF spec created before e2e protocol: WARN (advisory)
    ELSE: FAIL "E2E registry missing"

  # All ACs mapped?
  unmapped = [ac for ac in spec.must_have + spec.error_acs if ac not in registry]
  IF unmapped: FAIL "Unmapped ACs: {unmapped}"

  # TDD proof: RED before GREEN
  for entry in registry:
    IF entry.status == GREEN_CONFIRMED AND NOT entry.had_red:
      FAIL "TDD violation: {entry.ac} — no RED_CONFIRMED before GREEN"

  # All BLOCKING entries GREEN?
  blocking = [e for e in registry if e.required == BLOCKING]
  not_green = [e for e in blocking if e.status != GREEN_CONFIRMED]
  IF not_green: FAIL "Incomplete: {not_green}"

  # Mock boundary clean?
  new_test_files = get_new_test_files(git_diff)
  for file in new_test_files:
    IF contains_mock_of_own_code(file): FAIL "Mock boundary violation in {file}"

  # Bug fix validation
  IF spec.is_bug_fix:
    IF NOT registry.has("AC-B2") OR registry["AC-B2"].status != GREEN_CONFIRMED:
      FAIL "Bug fix missing RED proof (AC-B2)"
    IF NOT registry.has("AC-B3") OR registry["AC-B3"].status != GREEN_CONFIRMED:
      FAIL "Bug fix missing GREEN proof (AC-B3)"
    IF NOT registry.has("AC-B4") OR registry["AC-B4"].status != GREEN_CONFIRMED:
      FAIL "Bug fix DIFF not confirmed (AC-B4)"

  PASS "100% E2E coverage, TDD proof clean"
```

**Unresolved bugs are blocking.** All entries in "Encountered Bugs" must be Fixed or Deferred before done.

### Production Validation

Additional checks for production deploys:
- Schema validation (if schema files changed)
- Deploy readiness check
- Security audit
- Performance validation

## Step 2: Retro (Always Runs)

Analyze the session and capture learnings:

    ### Ship Retro ({DATE})
    **Estimate vs Actual:** {X}h → {Y}h ({accuracy}%)
    **What worked:** {insight}
    **What didn't:** {insight with root cause}
    **Next time:** {specific improvement}

Write retro to:
1. Spec file `## Notes` section
2. Project learnings file (if maintained)

## Step 3: Record Timestamp

Add done entry to spec Timeline:

    | done | {ISO_TIMESTAMP} | {total_duration} | - |

## Step 4: Propose Memory Update (Agent Self-Improvement)

Follow the full protocol in [memory-update.md](../memory-update.md):
1. Detect agent type, read correct config files (CLAUDE.md for Claude Code, AGENTS.md for others)
2. Extract learnings (6 categories — including **patterns & anti-patterns**)
3. Classify & target (user-level vs project-level, route to correct file)
4. Present file-targeted proposals with exact content for user approval

**Pattern extraction is critical.** Every session produces learnings worth remembering: user preferences (coding style, architecture choices), repeated requests that should become defaults, project knowledge discovered during implementation, and anti-patterns from mistakes or regressions. Capturing these in agent config avoids repeat questions and makes future sessions faster.

If no project agent config exists (no CLAUDE.md or AGENTS.md), propose creating one with initial rules from this session's learnings.

## Step 5: CI Integration (Optional)

If the agent has access to CI pipelines (GitHub Actions, GitLab CI, etc.):

```
1. Push to feature branch (if not already pushed)
2. Wait for CI pipeline to complete
3. Read CI results:
   - Build: PASS/FAIL
   - Tests: PASS/FAIL (N passing, N failing)
   - Lint/typecheck: PASS/FAIL
   - Coverage: {percent} (delta from main)
4. Include CI status in validation output
5. If CI fails: treat as validation failure — suggest `ship` to fix
```

CI is ADVISORY by default. Edit this file to make it BLOCKING.

## Step 6: Archive Spec

```
mkdir -p specs/shipped
mv specs/active/{spec-file}.md specs/shipped/
Update spec: status → shipped, shipped → {YYYY-MM-DD}
```

## Step 7: Log to History

Append to `specs/history.log`:
```
{DATE} | shipped | {slug} | {estimate}h→{actual}h | {duration} | {summary}
```

## Step 8: Output

Follow the output template in `references/templates/done-output.md`.

Covers: validation passed (retro + memory update + next steps) and validation failed.

## Express Ship (No Spec)

If no spec exists (one-shot build):
1. Skip spec archival
2. Still run validation
3. Log to history

## Never

- Never runs `git push`
- Never runs deploy commands
- Never makes production changes
