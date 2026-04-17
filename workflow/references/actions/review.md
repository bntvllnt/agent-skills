# Review Action

> **Agent:** Load this file when `review` triggers or during ship loop review cycles. Also load `references/rules-discovery.md` — discovered rules become the Rules perspective checklist.

Auto-selecting multi-perspective code review. Runs during ship loop or standalone.

**Portability rule:** this file defines the review contract, not a specific runtime implementation. Use `references/reviews/core-portable-review-spec.md` as the normative portable standard. Runtime-specific orchestration is optional and belongs in executor guidance, not in the core contract.

**Implementation note:** command snippets and tool names in this file are illustrative examples, not mandatory dependencies. Any executor may substitute equivalent mechanisms as long as it preserves the same coverage, rule-checking, and artifact requirements.

---

## Step 1: Change Overview (ALWAYS FIRST)

Before any review, build a change map **and a line-coverage ledger**:

```
1. git diff --name-status (vs base branch or last review)
2. git diff --unified=0 --no-color ...
   → enumerate every changed hunk with exact line ranges
   → build a ledger per file: added lines, modified lines, deleted lines
3. Per file, classify:
   - Category: auth/security | API/public | DB/schema | UI/component |
               config/infra | test | docs | internal logic
   - Risk: HIGH | MEDIUM | LOW
4. Detect primary language + framework from changed files
5. Detect context signals (see Step 2)
6. **TypeScript structural risk** (if CI available, see `references/codebase-intelligence.md`):
   Run: `npx codebase-intelligence changes --json`
   → Augments git diff with coupling score, blast radius, and complexity delta per file
   → Use to refine Risk Classification below (more precise than filename-based heuristics)
   If CI unavailable: use filename-based risk classification only
```

### Core Portable Review Contract (MANDATORY)

See `references/reviews/core-portable-review-spec.md` for the normative portable contract and `references/reviews/executor-patterns.md` for optional implementation examples.

This action file describes the workflow-level review policy. It must remain valid whether review is executed by one agent, many agents, a CI system, or a human operator.

### Coverage Contract (MANDATORY)

No sampling. No “looks fine overall.” No skipping low-risk hunks.

For `review`, the agent must prove two kinds of coverage before returning a clean verdict:

1. **Line coverage** — every changed line range in the diff ledger is checked at least once.
2. **Rule coverage** — every relevant discovered rule is checked one by one against the changed scope.

Minimum enforcement:

```
For each changed file:
  For each changed hunk / line range:
    assign ≥1 perspective owner
    inspect the exact changed lines, not just surrounding file context

For each relevant discovered rule:
  check it explicitly against each changed file/hunk it applies to
  record: PASS | WARN | FAIL | NOT_APPLICABLE
```

If any changed line range has no explicit review coverage, or any relevant rule is left unchecked, the review must emit a blocking process finding:

```
{file}:{line or range} — FAIL [Process] Changed lines not explicitly reviewed
  Fix: Review the uncovered lines and record perspective coverage
```

### Risk Classification

| Risk | File Categories |
|------|----------------|
| HIGH | auth, payments, DB schema/migrations, public API, delete operations, crypto |
| MEDIUM | config, new dependencies, performance-critical paths, CI/CD, infrastructure |
| LOW | internal logic, tests, docs, formatting, comments, private utilities |

### Output: Change Map

```
| File | Changed lines | Category | Risk | Language |
|------|---------------|----------|------|----------|
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

### Rules Discovery (MANDATORY — Before Perspective Dispatch)

Load `references/rules-discovery.md` and execute Steps 1-4. This discovers project/user agent config files, extracts rules, filters for relevance against the change map, and classifies severity. The discovered rules become the checklist for the Rules perspective (#10).

No config files found or no relevant rules → skip Rules perspective entirely.

**Important:** rules are not satisfied by a global statement like “follow project rules.” The review must check each relevant rule individually and mark it PASS/WARN/FAIL/NOT_APPLICABLE against the changed scope.

### Quick Mode

- **Perspectives:** Core 5 + Rules (if rules files exist)
- **Checklist depth:** 6 items per perspective (key questions below)
- **Context loaded:** This file only

### Standard Mode

- **Perspectives:** Core 5 + Rules (if rules files exist) + auto-triggered conditionals
- **Checklist depth:** 6 items per perspective
- **Context loaded:** This file only
- **Conditional triggers:**

| Perspective | Triggers On |
|-------------|-------------|
| Scalability | Shared state, DB queries, multi-instance deployment, pub/sub, queues |
| Observability | Production service, background job, API endpoint, webhook handler |
| Testability | Complex branching (>=3 paths), critical business logic, stateful flows |
| Accessibility | UI components, forms, navigation, interactive elements |

### Structural Context (TypeScript projects with CI or equivalent tooling)

Before dispatching perspectives in Standard/Deep/Production modes, gather structural data when compatible tooling exists.

**Example implementation:**
```
For each changed TS/TSX file:
  npx codebase-intelligence dependents --json <file>
    → Consumer awareness: who imports this? What could break?
  npx codebase-intelligence forces --json
    → Cohesion/coupling metrics for architectural review

Include in perspective agent context alongside file contents and diff.
If CI unavailable: perspectives rely on file contents + grep-based import tracing.
```

### Deep Mode

- **Perspectives:** All 9 + Rules (if rules files exist)
- **Checklist depth:** 6 items per perspective
- **Context loaded:** This file only

### Production Mode

- **Perspectives:** All 9 + Rules (if rules files exist; ambiguous rule signals → FAIL)
- **Checklist depth:** 15-20 items per perspective (extended checklists)
- **Context loaded:** This file + `references/reviews/production-standards.md`
- **Additional:** Expert personas, company bar evaluation, language-specific overlay

**Production execution (example implementation):**

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

### Rules (Active When Rules Files Exist)

| # | Perspective | Trigger | Key Questions |
|---|------------|---------|---------------|
| 10 | Rules | Any agent config found (AGENTS.md, CLAUDE.md, .cursorrules, codex.md, .opencode/config, etc.) | Violates project conventions? Contradicts user rules? Ignores documented anti-patterns? |

The Rules perspective uses discovered rules as its checklist (not a built-in checklist). Each finding cites the source file and violated rule text.

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
2. Use the diff ledger to inspect every changed line range owned by that perspective
3. Evaluate against perspective checklist (depth matches mode)
4. Classify findings:
   - PASS: Meets criteria (not shown in output)
   - WARN: Concern, not blocking (severity: low/medium/high)
   - FAIL: Must fix before shipping (BLOCKING)
   - BLOCKS_PRODUCTION: Violates production bar (Production mode only)
5. Update coverage ledger for the reviewed line ranges
```

Run perspectives in parallel when possible.

Parallelism is optional. Executors may review sequentially or in parallel as long as they preserve the same coverage and artifact requirements.

After all perspectives complete:

```
1. Verify every changed line range is covered
2. Verify every relevant rule has an explicit verdict
3. Emit FAIL [Process] for each uncovered line range or unchecked rule
4. Only return CLEAN / WARNINGS_ONLY when both coverage checks are complete and the output includes the rule coverage ledger
```

---

## Output

Follow `references/templates/review-output.md` for the human-readable summary.

In addition, emit a machine-readable artifact equivalent to the schema in `references/reviews/core-portable-review-spec.md`.

Key format: `{file}:{line} — {severity} [{perspective}] {description}` + `Fix: {action}`.

Process coverage gaps use the same format with `[Process]` as the perspective.

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
