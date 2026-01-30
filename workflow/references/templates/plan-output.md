# Plan Output Template

Unified output for `plan` and `spec-review` actions. Same template = same decision point.

- **`plan`** populates all sections during spec creation. Decision logic: [plan.md](../actions/plan.md).
- **`spec-review`** re-runs Analysis + Readiness on an existing spec. Decision logic: [spec-review.md](../actions/spec-review.md).

---

```markdown
## {Plan Complete / Spec Review}: {title}

**Problem:** {1-2 sentence description of the real problem being solved}
**Approach:** {1-2 sentence description of how it will be solved}
**Spec:** `specs/active/{filename}.md`
**Tier:** {tier} | **Estimate:** {X}h | **Scope:** {N} items
**Perspectives:** {Role 1, Role 2, ...} (spec-review only — omit this line for plan)

### Codebase Impact

| Area | Impact | Files |
|------|--------|-------|
| {module} | CREATE/MODIFY/AFFECTED | `{path}`, `{path}` |

**Reuse:** {existing code to leverage}
**Breaking changes:** {none or list}

### Analysis

#### Assumptions Challenged

| # | Assumption | Evidence For | Evidence Against | Verdict | Action |
|---|------------|-------------|-----------------|---------|--------|
| 1 | {assumption} | {evidence} | {counter-evidence} | VALID/RISKY/WRONG | → {update spec / explore / question / no action} |

#### Blind Spots

| # | Category | Blind Spot | Impact If Ignored | Suggested Spec Change |
|---|----------|-----------|-------------------|----------------------|
| 1 | [{category}] | {what's missing} | {consequence} | {specific change or "N/A"} |

#### Failure Hypotheses

| # | IF | THEN | BECAUSE | Severity | Mitigation Status |
|---|-----|------|---------|----------|-------------------|
| 1 | {trigger} | {failure} | {root cause} | HIGH/MED/LOW | Added / Missing / N/A |

#### The Real Question

{Reframe the problem or confirm it's correct.}
**Recommendation:** {what to do about it}

#### Open Items

- [{tag}] {finding} → {action}

Tags: `[risk]` `[gap]` `[question]` `[improvement]`
Actions: `→ update spec` | `→ explore` | `→ question` | `→ no action`

Omit tags with no items. If none: "None — ready to ship."
Every item MUST end with an action suffix.

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

**Score:** {N}/{max} | **Verdict:** {READY / CONDITIONAL / NOT_READY / REVIEW_PENDING}

Verdicts:
- **READY**: Ship it. `→ ship`
- **CONDITIONAL**: Warnings exist. Proceed or address. `→ ship` or fix first.
- **NOT_READY**: Blockers found. Fix issues, re-run. `→ fix, then plan --recheck` or `spec-review`
- **REVIEW_PENDING**: Needs human review. `→ Use [?][!][+][-][~][ok] or say 'proceed'.`

**Next:** {explicit action}

### Action Items

- [ ] {finding} → {update spec / explore / question}
(Only items requiring action. Omit `→ no action` items.)
```
