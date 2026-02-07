# Review Action

> **Agent:** Load this file when `review` triggers or during ship loop review cycles.

Auto-selecting multi-perspective code review. Runs during ship loop or standalone.

---

## Step 1: Change Overview (ALWAYS FIRST)

Before any review, build a change map:

```
1. git diff --name-status (vs base branch or last review)
2. Per file, classify:
   - Category: auth/security | API/public | DB/schema | UI/component |
               config/infra | test | docs | internal logic
   - Risk: HIGH | MEDIUM | LOW
3. Detect primary language + framework from changed files
4. Detect context signals (see Step 2)
```

### Risk Classification

| Risk | File Categories |
|------|----------------|
| HIGH | auth, payments, DB schema/migrations, public API, delete operations, crypto |
| MEDIUM | config, new dependencies, performance-critical paths, CI/CD, infrastructure |
| LOW | internal logic, tests, docs, formatting, comments, private utilities |

### Output: Change Map

```
| File | Category | Risk | Language |
|------|----------|------|----------|
```

This table appears in the review output (see `references/templates/review-output.md`).

---

## Step 2: Auto-Select Mode

Mode is determined by signals from the change map. **Agent selects — not the user.**

| Signal | Mode |
|--------|------|
| 1-2 files, all LOW risk, no API changes | Quick |
| 3-5 files OR any MEDIUM risk | Standard |
| 6+ files OR any HIGH risk file | Deep |
| Deploy context detected (see below) | Production |

### Deploy Context Signals (ANY ONE triggers Production)

- User said: "production ready", "pre-deploy", "deploy", "release", "production review"
- Merging to main/master branch (detected from git context)
- Ship loop exit check (final review before `done`)
- Changed files include: CI/CD config, Dockerfile, k8s manifests, terraform
- User explicitly requests: "review production"

**Multiple signals: highest mode wins.**

Announce selection before reviewing:

```
Review mode: {MODE} — {reason}
```

Example: `Review mode: Deep — HIGH risk file detected (src/api/auth.ts: auth/security)`

---

## Step 3: Execute Review

### Quick Mode

- **Perspectives:** Core 5 (Correctness, Security, Reliability, Performance, DX)
- **Checklist depth:** 6 items per perspective (key questions below)
- **Context loaded:** This file only

### Standard Mode

- **Perspectives:** Core 5 + auto-triggered conditionals
- **Checklist depth:** 6 items per perspective
- **Context loaded:** This file only
- **Conditional triggers:**

| Perspective | Triggers On |
|-------------|-------------|
| Scalability | Shared state, DB queries, multi-instance deployment, pub/sub, queues |
| Observability | Production service, background job, API endpoint, webhook handler |
| Testability | Complex branching (>=3 paths), critical business logic, stateful flows |
| Accessibility | UI components, forms, navigation, interactive elements |

### Deep Mode

- **Perspectives:** All 9 active (no conditional skipping)
- **Checklist depth:** 6 items per perspective
- **Context loaded:** This file only

### Production Mode

- **Perspectives:** All 9 active
- **Checklist depth:** 15-20 items per perspective (extended checklists)
- **Context loaded:** This file + `references/reviews/production-standards.md`
- **Additional:** Expert personas, company bar evaluation, language-specific overlay

**Production execution:**

```
1. Load references/reviews/production-standards.md
2. IF WebSearch/web capabilities available:
     Search in parallel:
       "{language} production code review checklist {year} best practices"
       "{framework} production best practices {year} common mistakes"
       "{language} anti-patterns production code {year}"
     Synthesize into language-specific overlay
   ELSE:
     Use fallback language standards from production-standards.md Section D
3. Per perspective:
   a. Adopt expert persona (Section B)
   b. Apply extended checklist (Section C)
   c. Apply language-specific overlay (dynamic or fallback)
   d. Evaluate against production bar (Section A)
4. Output with production format (BLOCKS_PRODUCTION severity)
```

---

## Perspectives

### Core (Always Active)

| # | Perspective | Key Questions |
|---|------------|---------------|
| 1 | Correctness | Does it do the right thing? Edge cases? Regressions? |
| 2 | Security | Input validated? Auth correct? Secrets safe? No injection? |
| 3 | Reliability | Error paths handled? Graceful degradation? Timeouts? Cleanup? |
| 4 | Performance | N+1 queries? Unnecessary computation? Bundle impact? Hot path? |
| 5 | DX | Readable? Good names? Actionable errors? Types guide usage? |

### Conditional (Add When Triggered)

| # | Perspective | Trigger | Key Questions |
|---|------------|---------|---------------|
| 6 | Scalability | Shared state, DB, multi-instance | Thread safe? Works at 10x? Horizontally scalable? |
| 7 | Observability | Production service, background job | Structured logging? Metrics? Traceable? Health signals? |
| 8 | Testability | Complex branching, critical logic | Tests exist? Assert behavior not implementation? Coverage gaps? |
| 9 | Accessibility | UI components | Semantic HTML? Keyboard nav? Screen reader? Contrast? |

---

## Execution (All Modes)

For each active perspective:

```
1. Read all changed files
2. Evaluate against perspective checklist (depth matches mode)
3. Classify findings:
   - PASS: Meets criteria (not shown in output)
   - WARN: Concern, not blocking (severity: low/medium/high)
   - FAIL: Must fix before shipping (BLOCKING)
   - BLOCKS_PRODUCTION: Violates production bar (Production mode only)
4. Output structured findings per review-output.md template
```

Run perspectives in parallel when possible.

---

## Output

Follow `references/templates/review-output.md`.

Key format: `{file}:{line} — {severity} [{perspective}] {description}` + `Fix: {action}`.

Production mode adds: `Standard: {Company} — {rule violated}` line under BLOCKS_PRODUCTION findings.

---

## Iteration Limit

Max 3 review iterations per ship cycle. If still blocking after 3:
- Present remaining issues to user
- User decides: fix, defer, or accept risk

---

## Review Triggers (During Ship Loop)

| Condition | Review? |
|-----------|---------|
| Every 2-3 implementation iterations | Yes (auto-select) |
| Before exit check | Yes (auto-select, leans Production) |
| User requests `review` | Yes (auto-select, user can override mode) |
| Security-sensitive code changed | Yes (auto-select, min Standard) |
| Public API changed | Yes (auto-select, min Standard) |
