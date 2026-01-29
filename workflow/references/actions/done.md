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
| New tests for new behavior | Yes (BLOCKING) |
| Existing tests passing | Yes |
| No typecheck/lint errors | Yes |
| No debug statements (console.log, debugger, print, pdb, etc.) | Yes |
| No hardcoded secrets | Yes |
| Can rollback (git revert works, no irreversible migrations) | Yes |
| No unresolved bugs (all fixed or deferred) | Yes |

**New test mandate:** Every new behavior MUST have at least one test. Not just "existing tests pass" — new code needs new tests. If test infrastructure doesn't exist, propose setting it up. If user declines, document the skip reason.

ACs are the definition of DONE. Scope items track implementation tasks, but ACs determine if the feature actually works as specified in the user journey.

If any check fails: STOP. Show what's remaining. Suggest `ship` to continue.

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

## Step 4: Propose Memory Update

Follow the full protocol in [memory-update.md](../memory-update.md):
1. Read existing user + project rules (MANDATORY)
2. Extract learnings (5 categories)
3. Classify & target (user-level vs project-level)
4. Present structured proposal for user approval

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
