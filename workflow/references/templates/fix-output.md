# Fix Output Template

Edit this file to customize what the agent returns after `fix`. Decision logic: [actions/fix.md](../actions/fix.md).

---

## Fix Complete

```markdown
## Fix Complete

**Bug:** {description}
**Root cause:** {1-line cause}
**Classification:** simple | complex
**Fix:** {1-line what changed}

### Anti-Cascade TDD
**BASELINE:** {N} pass | {N} fail | {N} skipped
**RED:** {test name} → FAIL (confirmed)
**GREEN:** {what changed} → PASS
**DIFF:** {N} pass | {N} fail | {N} skipped (zero new failures)
**SCAN:** {N} sibling locations | {proposed/none found}

### Quality Gates
lint {OK/FAIL} | typecheck {OK/FAIL} | build {OK/FAIL} | test {OK/FAIL}

Next: Run `done` to validate, retro, and archive.
```

---

## Complex Bug Output

When Phase 1 (INVESTIGATE) ran, prepend before Anti-Cascade TDD:

```markdown
### Investigation
**Hypotheses:** {N} formed, {N} tested
**Confirmed:** H{N} — {hypothesis description}
**Evidence:** {key evidence that confirmed root cause}
```

---

## Fix Blocked

When DIFF detects regressions:

```markdown
## Fix Blocked

**Bug:** {description}
**Fix attempt:** {what was tried}
**DIFF result:** {N} new failures detected

**Regressions:**
- {test name}: {what broke}

Options: fix regressions (keep original fix) | roll back (different approach) | escalate
```

---

## Fix Abbreviated

For emergency/hotfix (skipped steps):

```markdown
## Fix Complete (Emergency)

**Bug:** {description}
**Fix:** {what changed}
**RED:** {test name} → FAIL
**GREEN:** → PASS
**DIFF:** {N} pass | {N} fail (zero new failures)
**Skipped:** {INVESTIGATE / SCAN / spec ceremony}
**Reason:** {why skipped}

Next: Run `done` to validate, retro, and archive.
```

---

## Example: Full Bug Fix

```markdown
## Fix Complete

**Bug:** Null reference on user.email when profile incomplete
**Root cause:** getDisplayName() assumes email is always populated
**Classification:** simple
**Fix:** Added null check with fallback to username

### Anti-Cascade TDD
**BASELINE:** 42 pass | 0 fail | 2 skipped
**RED:** test_null_email_profile → FAIL (confirmed bug)
**GREEN:** Added optional chaining in getDisplayName() → PASS
**DIFF:** 43 pass | 0 fail | 2 skipped (zero new failures)
**SCAN:** 2 sibling locations with same pattern → proposed batch fix

### Quality Gates
lint OK | typecheck OK | build OK | test OK

Next: Run `done` to validate, retro, and archive.
```
