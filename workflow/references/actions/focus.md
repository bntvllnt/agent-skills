# Focus Action

> **Agent:** Load this file when `focus` triggers. Also load `references/reviews/production-standards.md` — it provides extended checklists for scanning. Also load `references/rules-discovery.md` — scan checks existing code against project/user rules.

Scan codebase against review perspectives, surface prioritized tasks toward production readiness. Output: ranked task proposals, user selects, specs created in `specs/backlog/`.

---

## Task Tracking (MANDATORY)

Before starting, create tasks in your agent's built-in task/todo system:

```
[ ] Detect project (Step 0)
[ ] Scan existing specs (Step 1)
[ ] Ask goal (Step 2)
[ ] Dispatch perspective agents (Step 3)
[ ] Synthesize findings (Step 4)
[ ] Rank and present (Steps 5-6)
[ ] User selects → create specs (Step 7)
```

---

## Step 0: Detect Project

Reuse from plan.md:

```
Check project for:
  - Monorepo (turbo.json)
  - Package manager (pnpm/yarn/bun/npm from lockfile)
  - Test runner (vitest/jest/pytest from config)
  - Framework (next/expo/convex from package.json)
  - Primary language (from file extensions, tsconfig, pyproject.toml)
```

Also estimate codebase size:

| Size | Files | Agent Count |
|------|-------|-------------|
| Small | <50 source files | 2-3 agents |
| Medium | 50-200 source files | 3-4 agents |
| Large | 200+ source files | 4-5 agents |

Count source files only (exclude `node_modules`, `dist`, `.git`, lockfiles, generated).

### TypeScript Structural Snapshot (Optional)

If TypeScript detected (`tsconfig.json` exists):

```
Load references/codebase-intelligence.md for detection gate.
Run: npx codebase-intelligence overview --json <project-root>
  → Accurate file/module count (replaces manual estimation)
  → Dependency graph shape informs agent count decision
If CI unavailable: use file count estimation above
```

---

## Step 1: Scan Existing Specs

Scan all `specs/` subfolders for existing work:

```
specs/active/    → Tag: [ACTIVE] — current work, show prominently
specs/backlog/   → Tag: [BACKLOG] — queued work, check for overlap with new findings
specs/dropped/   → Tag: [DROPPED] — abandoned, note learnings
specs/shipped/   → Tag: [SHIPPED] — last 10 by modification date only, context only
```

For each spec found, extract:
- Title, status, estimated effort
- Key scope items (what it covers)

**Rules:**
- If active spec exists, show it first — user may want to finish it before new work
- Dropped specs with relevant learnings: note what was learned, don't re-propose same approach
- Shipped specs: context only, never re-proposed
- Backlog specs that overlap with new findings: tag as `[BACKLOG]`, link to spec, skip duplicate proposal

---

## Step 2: Ask Goal

Use interactive question (AskUserQuestion or equivalent):

```
What should we focus on?

1. Production readiness — Harden: tests, security, error handling, monitoring
2. MVP / ship value — Quickest path to user-visible value: TODOs, incomplete features, UX gaps
3. Infrastructure — Scale foundation: patterns, deps, type safety, duplication
4. Other — Custom focus (describe)
```

**Production readiness is ALWAYS the underlying lens.** Goal selection changes weighting, not the baseline. Every scan checks production bar as minimum.

---

## Step 3: Dispatch Perspective Agents

Dispatch parallel Explore agents. Each agent scans the codebase against assigned perspectives using checklists from `references/reviews/production-standards.md`.

**This is NOT a diff review — agents scan the WHOLE codebase against perspective checklists.**

### Agent Assignment by Goal

| Goal | Primary Perspectives (weighted high) | Secondary (still checked) |
|------|--------------------------------------|--------------------------|
| Production | Security, Reliability, Observability, Testability | Correctness, Performance, DX, Scalability |
| MVP | Correctness, DX, Performance | Security, Reliability, Testability |
| Infra | Scalability, DX, Testability | Performance, Reliability, Security |
| Custom | Agent picks based on user description | Production baseline always |

### Agent Distribution

Distribute 9 perspectives across agents (2-3 perspectives per agent):

```
Small codebase (2-3 agents):
  Agent 1: Security, Reliability, Observability
  Agent 2: Correctness, Performance, DX
  Agent 3 (if needed): Scalability, Testability, Accessibility

Medium codebase (3-4 agents):
  Agent 1: Security, Reliability
  Agent 2: Correctness, Performance
  Agent 3: DX, Scalability
  Agent 4 (if needed): Observability, Testability, Accessibility

Large codebase (4-5 agents):
  Agent 1: Security, Reliability
  Agent 2: Correctness, Performance
  Agent 3: DX, Testability
  Agent 4: Scalability, Observability
  Agent 5 (if needed): Accessibility + overflow
```

Skip Accessibility unless UI components detected in codebase.

### Agent Prompt Template

Each agent receives:

```
Scan this codebase against the following review perspectives.
You are scanning the WHOLE codebase, not reviewing a diff.

Perspectives assigned: {perspective names}

For each perspective, use this checklist:
{paste extended checklist items from production-standards.md for assigned perspectives}

Instructions:
1. Use Glob to find relevant source files (skip node_modules, dist, .git, generated)
2. Use Grep to search for patterns related to checklist items
3. Use Read to examine files with potential issues
4. For each finding, propose a CONCRETE TASK (not an observation):
   - BAD: "Missing error handling detected"
   - GOOD: "Add error handling to database queries in src/db/users.ts"
{if TypeScript project with CI available, add to each agent prompt:}
5b. Use these pre-computed structural insights (from codebase-intelligence --json):
   - HOTSPOTS: {output of `npx codebase-intelligence hotspots --json --metric complexity --limit 20`}
   - DEAD EXPORTS: {output of `npx codebase-intelligence dead-exports --json --limit 20`}
   - FORCES: {output of `npx codebase-intelligence forces --json`}
   - MODULES: {output of `npx codebase-intelligence modules --json`}
   Cross-reference these with your Glob/Grep/Read findings.
   Hotspots data replaces sampling strategy for TypeScript files.
5. Score each task:
   - Impact: H (affects users/security/data) / M (affects DX/maintainability) / L (cosmetic/minor)
   - Effort: L (<1h) / M (1-4h) / H (4h+)
   - Risk-if-ignored: H (will cause incidents) / M (will slow team) / L (annoyance)
6. Include file evidence: path:line for each finding
7. Focus on {primary perspectives} — these are weighted highest for the "{goal}" goal

Output format per task:
  Task: {actionable task description}
  Perspective: {which perspective flagged this}
  Impact: H/M/L
  Effort: L/M/H
  Risk: H/M/L
  Evidence: {file:line — brief description}
```

### Sampling Strategy (Large Codebases)

For 500+ source files, agents should focus on:
1. Files changed in last 30 days (recent activity = higher relevance)
2. Entry points (main files, route handlers, API endpoints)
3. Critical paths (auth, payments, data mutations)
4. Files with TODOs/FIXMEs/HACKs
5. Files without test coverage (look for missing `*.test.*` counterparts)

**TypeScript projects with CI:** `hotspots` data from codebase-intelligence replaces sampling heuristics for TS/TSX files. Non-TS files in the same project still use the sampling strategy above.

---

## Step 4: Synthesize

Collect results from all agents. Process:

1. **Deduplicate:** Merge tasks pointing at same file/issue from different perspectives
2. **Cross-reference with existing specs:** If a finding overlaps with a backlog/active spec, tag it `[BACKLOG]`/`[ACTIVE]` instead of proposing as new
3. **Merge related tasks:** Group small tasks into logical units (e.g., "Add error handling to 3 DB query files" → one task)
4. **Validate evidence:** Ensure file:line references are real (agents may hallucinate)

---

## Step 5: Rank

### Scoring Formula

```
score = (w_impact * impact) + (w_effort * (4 - effort)) + (w_risk * risk)
```

Where impact/effort/risk are: H=3, M=2, L=1

### Goal Weights

| Goal | w_impact | w_effort | w_risk |
|------|----------|----------|--------|
| Production | 3 | 1 | 5 |
| MVP | 5 | 3 | 1 |
| Infra | 2 | 2 | 2 |
| Custom | 3 | 2 | 3 |

### Tier Assignment

Sort by score descending, then group:

| Tier | Criteria | Description |
|------|----------|-------------|
| Do First | High impact + Low effort | Maximum value, minimum cost |
| Plan Next | High impact + Medium/High effort | Needs spec, worth the investment |
| Quick Wins | Medium impact + Low effort | Easy improvements, good momentum |

Cap at 10-15 tasks total. If more found, keep highest-scored.

---

## Step 6: Present

Output per `references/templates/focus-output.md`.

Include:
- Perspective summary (gaps per perspective)
- Existing specs (if any found in Step 1)
- Ranked task tables by tier
- Production readiness score (quick health check per perspective)
- Effort estimates use same calibration as plan.md: aggressive, AI-assisted

---

## Step 7: User Selects

Use interactive multi-select (AskUserQuestion multiSelect or equivalent):

```
Select tasks to plan (select multiple):
  1. {task description} (Effort: {est}, Perspective: {name})
  2. ...
```

For each selected task:

1. Invoke `plan` action with the task as the idea
2. Spec created in `specs/backlog/` (NOT `specs/active/`)
3. User manually moves to `specs/active/` when ready to `ship`

If user selects a task that overlaps with existing backlog spec, note it instead of creating duplicate.

---

## Edge Cases

| Case | Handle |
|------|--------|
| Empty codebase (no source files) | "No code to analyze. Run `plan {idea}` to start." |
| No findings | "Production-ready baseline met. Run `plan {idea}` for new features." |
| All tasks >4h effort | Flag: "Large scope tasks — will split during plan phase." |
| Existing spec covers finding | Tag `[BACKLOG]`/`[DROPPED]`, link to spec, skip duplicate |
| Active spec exists | Show prominently: "Active work in progress — finish first?" |
| Many shipped specs (>10) | Only load last 10 by modification date |
| No test runner detected | Note in testability perspective: "No test infrastructure — propose setup as task" |

---

## Lifecycle Position

```
focus → plan → ship → done → focus (repeat)
  │                              ▲
  └──────────────────────────────┘
```

Focus is the entry point when you don't know what to work on next. It completes the cycle by feeding back into `plan`.
