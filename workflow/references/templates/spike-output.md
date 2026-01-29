# Spike Output Template

Edit this file to customize what the agent returns after `spike`. Decision logic: [actions/spike.md](../actions/spike.md).

---

```markdown
## Spike: {question}

**Time box:** {X}h | **Actual:** {Y}h
**Decision:** GO / NO-GO / NEEDS_MORE_INFO

### Findings
- {what we discovered}
- {evidence for/against}

### Decision Rationale
{why GO or NO-GO, with evidence}

### Next Step
- GO → `plan {follow-up idea}`
- NO-GO → {alternative approach or why we're stopping}
- NEEDS_MORE_INFO → {what additional spike or info is needed}
```
