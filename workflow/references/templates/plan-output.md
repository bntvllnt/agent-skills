# Plan Output Template

Edit this file to customize what the agent returns after `plan`. Decision logic: [actions/plan.md](../actions/plan.md).

---

```markdown
## Plan Complete: {title}

**Spec:** `specs/active/{filename}.md`
**Status:** READY / CONDITIONAL / NOT_READY
**Tier:** {tier} | **Estimate:** {X}h | **Scope:** {N} items

### Codebase Impact

| Area | Impact | Detail |
|------|--------|--------|
| {module} | CREATE/MODIFY/AFFECTED | {what and why} |

**Reuse:** {existing code to leverage}
**Breaking changes:** {none or list}

### Analysis

**Improvements:**
- {suggestion to strengthen spec, architecture, or approach}

**Gaps:**
- {unknown that could affect implementation}

**Questions:**
- {question for user — or "None — requirements clear"}

**Risks:**
- {risk}: {mitigation}

### Readiness

| Gate | Result |
|------|--------|
| Codebase analyzed | PASS/FAIL |
| User journey | PASS/FAIL |
| Error journeys | PASS/FAIL |
| Acceptance criteria | PASS/FAIL |
| Scope ↔ AC traceability | PASS/FAIL |
| Quality checklist | PASS/FAIL |
| Analysis complete | PASS/FAIL |

**Score:** {N}/{max} | **Verdict:** {READY/CONDITIONAL/NOT_READY/REVIEW_PENDING}

{READY → "Run `ship` to implement."
| CONDITIONAL → "Warnings exist. Proceed anyway?"
| NOT_READY → "Fix issues, then re-check."
| REVIEW_PENDING → "Standard tier — review spec before ship. Use [?][!][+][-][~][ok] notation, or say 'proceed'."}
```
