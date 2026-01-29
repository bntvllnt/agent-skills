# Review Action

> **Agent:** Load this file when `review` triggers or during ship loop review cycles.

Multi-perspective code review. Runs during ship loop or standalone.

---

## Modes

| Mode | Perspectives | When |
|------|-------------|------|
| Quick | Core 5 only | Small changes, single file |
| Standard | Core 5 + triggered conditionals | Default |
| Deep | All 9 | Large features, pre-production |

## Perspectives

### Core (Always)

| # | Perspective | Key Question |
|---|------------|--------------|
| 1 | Correctness | Does it do the right thing? Edge cases? Regressions? |
| 2 | Security | Input validated? Auth correct? Secrets safe? No injection? |
| 3 | Reliability | Error paths handled? Graceful degradation? Timeouts? Cleanup? |
| 4 | Performance | N+1 queries? Unnecessary computation? Bundle impact? Hot path? |
| 5 | DX | Readable? Good names? Actionable errors? Types guide usage? |

### Conditional (Add When Triggered)

| # | Perspective | Trigger | Key Question |
|---|------------|---------|--------------|
| 6 | Scalability | Shared state, DB, multi-instance | Thread safe? Works at 10x? Horizontally scalable? |
| 7 | Observability | Production service, background job | Structured logging? Metrics? Traceable? Health signals? |
| 8 | Testability | Complex branching, critical logic | Tests exist? Assert behavior not implementation? Coverage gaps? |
| 9 | Accessibility | UI components | Semantic HTML? Keyboard nav? Screen reader? Contrast? |

## Execution

For each active perspective:

```
1. Read all changed files
2. Evaluate against perspective checklist
3. Classify findings:
   - PASS: Meets criteria
   - WARN: Concern, not blocking (severity: low/medium/high)
   - FAIL: Must fix before shipping (BLOCKING)
4. Output structured findings
```

Run perspectives in parallel when possible.

## Output

Follow the output template in `references/templates/review-output.md`.

Key format: `{file}:{line} — FAIL/WARN [{perspective}] {description}` + `Fix: {action}`. Flat list, actionable only, no PASS noise.

## Iteration Limit

Max 3 review iterations per ship cycle. If still blocking after 3:
- Present remaining issues to user
- User decides: fix, defer, or accept risk

## When Review Triggers (During Ship Loop)

| Condition | Review? |
|-----------|---------|
| Every 2-3 implementation iterations | Yes (quick) |
| Before exit check | Yes (standard) |
| User requests `review` | Yes (user-chosen mode) |
| Security-sensitive code changed | Yes (standard, security focus) |
| Public API changed | Yes (standard) |
