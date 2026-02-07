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

**CLAUDE.md** ({project}/CLAUDE.md):
- ADD rule: "{exact rule text}" → Section: {section name}
- ADD anti-pattern: "{exact anti-pattern}" → Section: {section name}
- {or "No updates needed"}

**AGENTS.md** ({project}/AGENTS.md):
- ADD rule: "{exact rule text}" → Section: {section name}
- ADD coding standard: "{exact standard}" → Section: {section name}
- {or "File not found — propose creating with initial rules? [y/n]"}

**User-level** (~/.claude/CLAUDE.md):
- ADD pattern: "{exact pattern}" → Section: {section name}
- {or "No universal learnings this session"}

Update? [apply all / select / skip]

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

**Critical anti-patterns detected (add to agent config):**
- {anti-pattern}: {what went wrong and how to prevent}
- {or "None"}

Run `ship` to fix remaining issues.
```
