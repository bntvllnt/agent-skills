# Done Output Template

Edit this file to customize what the agent returns after `done`. Decision logic: [actions/done.md](../actions/done.md).

---

## Validation Passed

```markdown
## Done: {title}

**Spec:** `specs/shipped/{filename}`
**Estimate vs Actual:** {X}h → {Y}h ({accuracy}%)

### Validation
- Must Have ACs: {N}/{N} PASS
- Error ACs: {N}/{N} PASS
- New tests: {N} added
- Quality gates: lint OK | typecheck OK | build OK | test OK
- Bugs: {N} fixed, {N} deferred

### Retro
- **Worked:** {insight}
- **Didn't:** {insight with root cause}
- **Next time:** {specific improvement}

### Memory Update Proposed
- **User-level:** {learning or "None"}
- **Project-level:** {learning or "None"}

### Next (human)
1. Commit + push
2. Deploy
3. Verify in production
```

---

## Validation Failed

```markdown
## Done: NOT READY

**Failing checks:**
- {check}: {what's wrong}
- {check}: {what's wrong}

Run `ship` to fix remaining issues.
```
