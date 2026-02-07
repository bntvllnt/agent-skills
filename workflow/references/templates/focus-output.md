# Focus Output Template

> **Agent:** Use this template for all focus action output. Fill sections based on scan results.

---

## Template

```markdown
## Focus: {Goal}

**Baseline:** Production readiness | **Goal lens:** {selected goal}
**Scanned:** {N} files | **Perspectives:** {N} active | **Date:** {YYYY-MM-DD}

### Perspective Summary

| Perspective | Gaps Found | Severity | Top Issue |
|-------------|-----------|----------|-----------|
| {name} | {count} | {HIGH/MEDIUM/LOW} | {one-line description} |

{if existing specs found:}

### Existing Specs

| Spec | Status | Est | Relevance to Goal |
|------|--------|-----|-------------------|
| {spec title} | [ACTIVE] / [BACKLOG] / [DROPPED] | {time} | {how it relates} |

{if active spec:}
> **Active work:** {spec title} — consider finishing this first.

### Proposed Tasks

#### Do First (High Impact, Low Effort)

| # | Task | Perspective | Impact | Effort | Est | Key Files |
|---|------|-------------|--------|--------|-----|-----------|
| 1 | {actionable task} | {perspective} | H | L | {time} | `{file:line}` |

#### Plan Next (High Impact, Medium+ Effort)

| # | Task | Perspective | Impact | Effort | Est | Key Files |
|---|------|-------------|--------|--------|-----|-----------|
| 1 | {actionable task} | {perspective} | H | M/H | {time} | `{file:line}` |

#### Quick Wins

| # | Task | Perspective | Impact | Effort | Est | Key Files |
|---|------|-------------|--------|--------|-----|-----------|
| 1 | {actionable task} | {perspective} | M | L | {time} | `{file:line}` |

### Production Readiness Score

| Perspective | Score | Gaps |
|-------------|-------|------|
| Correctness | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Security | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Reliability | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Performance | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| DX | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Scalability | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Observability | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Testability | {GOOD/FAIR/POOR} | {brief gap summary or "—"} |
| Accessibility | {GOOD/FAIR/POOR/N/A} | {brief gap summary or "—"} |

**Overall:** {GOOD/FAIR/POOR} — {one-line summary}

### Next

Select tasks above → specs created in `specs/backlog/` → move to `specs/active/` when ready → `ship`
```

---

## Scoring Guide

| Score | Meaning |
|-------|---------|
| GOOD | No high-severity gaps, minor improvements only |
| FAIR | Some gaps, none critical, addressable in 1-2 tasks |
| POOR | Significant gaps, needs dedicated work before production |
| N/A | Perspective not applicable (e.g., Accessibility for CLI tools) |

---

## Rules

- **Tasks not findings:** Every row is an actionable task, not a passive observation
- **Evidence required:** Every task links to at least one `file:line`
- **Effort estimates:** Use aggressive AI-assisted estimates (manual 10h = AI 1-2h)
- **Max tasks:** 10-15 total across all tiers. Trim lowest-scored if more
- **Empty tiers:** Omit tier section entirely if no tasks in that tier
- **Existing specs:** Only show section if specs were found
- **Active spec warning:** Always show if active spec exists
