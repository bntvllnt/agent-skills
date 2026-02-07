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

### Agent Config Updates

1. [P/CLAUDE.md § {section}] **{type}**: "{exact text to add}"
   _Context: {why this matters}_

2. [P/AGENTS.md § {section}] **{type}**: "{exact text to add}"
   _Context: {why this matters}_

3. [~/CLAUDE.md § {section}] **{type}**: "{exact text to add}"
   _Context: {why this matters}_

{or "No learnings to save this session."}

Apply which? [all / 1,3 / none]

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

**Learned patterns (add to agent config):**
- {user preference or anti-pattern}: {context and how to apply}
- {or "None"}

Run `ship` to fix remaining issues.
```
