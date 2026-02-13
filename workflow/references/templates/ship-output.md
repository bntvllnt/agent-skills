# Ship Output Template

Edit this file to customize what the agent returns during and after `ship`. Decision logic: [actions/ship.md](../actions/ship.md).

---

## Iteration Output

After each iteration:

```markdown
## Iteration {N}/{max}

**Scope item:** {name} → {DONE / IN_PROGRESS / BLOCKED}
**Quick pass:** lint {OK/FAIL} | typecheck {OK/FAIL}
**Progress:** {completed}/{total} scope items ({percent}%)
**ACs passing:** {N}/{total} Must Have | {N}/{total} Error

{If review ran:}
**Review:** {CLEAN / WARNINGS_ONLY / HAS_BLOCKERS} (see review output)
{If bug fix + PREVENT ran:}
**PREVENT:** {N} rules proposed | {approved/declined/skipped}

**Next:** {what happens next iteration}
```

---

## Exit Output

### Clean

```markdown
## Ship Complete

**Status:** CLEAN — all checks passing
**Progress:** {N}/{N} scope items | {N}/{N} Must Have ACs | {N}/{N} Error ACs
**Quality:** lint OK | typecheck OK | build OK | test OK
**Review:** {CLEAN / WARNINGS_ONLY}
{If bug fix:}
**Prevention:** {N} rules saved to {files} | {N} declined

Next: Run `done` to validate, retro, and archive.
```

### Partial

```markdown
## Ship Partial

**Status:** PARTIAL — scope done, ACs failing
**Progress:** {N}/{N} scope items | {passing}/{total} Must Have ACs | {passing}/{total} Error ACs
**Failing ACs:**
- AC-{N}: {description} — {why failing}

Fix failing ACs, then re-run `ship`.
```

### Stuck

```markdown
## Ship Paused

**Status:** STUCK — {reason}
**Progress:** {N}/{total} scope items ({percent}%) | Iteration {N}/{max}
**Blocked on:** {what's blocking progress}

Options: continue (different approach) | reduce scope | defer | drop
```

### Hard Stop

```markdown
## Ship Stopped

**Status:** MAX_ITERATIONS — hit limit at {N}
**Progress:** {N}/{total} scope items | {passing}/{total} ACs
**Remaining:**
- [ ] {incomplete scope item}

Reduce scope or re-plan.
```

---

## Spec Mutation Output

When user requests mid-loop changes:

```markdown
## Spec Updated

**Added:** {N} scope items, {N} ACs
**Modified:** {list}
**Removed:** {list}
**Traceability:** {PASS / orphans found}
**New progress:** {completed}/{new_total} scope items

Resuming ship loop.
```

---

## Bug Fix Iteration Example

```markdown
## Iteration 1/1 (Bug Mode)

**Bug:** Null reference on user.email when profile incomplete
**BASELINE:** 42 pass | 0 fail | 2 skipped
**RED:** test_null_email_profile → FAIL (confirmed bug)
**GREEN:** Added null check in getDisplayName() → test PASSES
**DIFF:** 43 pass | 0 fail | 2 skipped (zero new failures)
**SCAN:** Found 2 sibling locations with same pattern → proposed batch fix
**PREVENT:** 2 rules proposed

  1. [{project config} § Coding Rules] rule: "Always null-check optional user fields (email, phone, avatar) before access"
     _Prevents: null reference errors on incomplete user profiles_

  2. [{user config} § Anti-Patterns] anti-pattern: "Never assume user profile fields are populated — use optional chaining or explicit guards"
     _Prevents: runtime crashes from missing optional fields_

  Apply which? [all / 1,2 / none]
```
