# Workflow - High-Velocity Solo Development

Idea to production same-day. Spec-first, quality-gated, pattern-driven.

## Install

```bash
npx skills add bntvllnt/agent-skills --skill workflow
```

Global:
```bash
npx skills add bntvllnt/agent-skills --skill workflow -g
```

## Commands

| Command | What |
|---------|------|
| `plan {idea}` | Create spec with user journey, ACs, scope |
| `spike {question}` | Time-boxed exploration, produces go/no-go |
| `ship` or `ship {idea}` | Implement with build/review/fix loop |
| `review` | Multi-perspective code review (5-9 perspectives) |
| `done` | Validate, retro, archive, propose memory update |
| `drop` | Abandon with learnings preserved |
| `workflow` | Show current state, suggest next action |

No flags needed — the agent auto-detects intent from your natural language (e.g., "review the spec", "skip tests", "emergency fix", "production ready").

## Quickstart

Here's what a real workflow looks like end-to-end:

```
You:   plan add JWT authentication

Agent: Parsing idea...
       Tier: mini (estimated ~80 LOC)

       Writing user journey...
         ACTOR: Authenticated user
         GOAL: Log in with email/password, receive JWT
         1. User submits credentials → System validates → User receives token
         2. User sends request with token → System verifies → User gets response
         E1. Invalid credentials → System returns 401 → User sees error message

       Writing acceptance criteria...
         AC-1: GIVEN valid credentials WHEN POST /auth/login THEN returns JWT token
         AC-2: GIVEN valid JWT WHEN GET /api/protected THEN returns 200
         AC-E1: GIVEN invalid credentials WHEN POST /auth/login THEN returns 401

       Mapping scope to ACs...
         1. Create auth middleware → AC-2
         2. Create login endpoint → AC-1, AC-E1
         3. Add tests → AC-1, AC-2, AC-E1

       Running dev-readiness check...
         User journey:       PASS
         Acceptance criteria: PASS
         Scope ↔ AC:         PASS (3 scope → 3 ACs, 0 orphans)
         Quality checklist:   PASS

       Dev-ready: READY
       Spec: specs/active/2025-01-29-jwt-auth.md

       Next: Run `ship` to implement.

You:   ship

Agent: Loading spec... mode: LOOP (3 scope items, max 5 iterations)

       Iteration 1: Implementing scope item 1 (auth middleware → AC-2)
         ✓ Created src/middleware/auth.ts
         Quick pass: lint ✓ typecheck ✓
         Scope item 1 [x]

       Iteration 2: Implementing scope item 2 (login endpoint → AC-1, AC-E1)
         ✓ Created src/routes/auth.ts
         Quick pass: lint ✓ typecheck ✓
         Scope item 2 [x]
         Running dev review (5 perspectives)...
           Correctness: PASS
           Security: WARN — add rate limiting to login (medium)
           Reliability: PASS
           Performance: PASS
           DX: PASS

       Iteration 3: Implementing scope item 3 (tests → AC-1, AC-2, AC-E1)
         ✓ Created src/__tests__/auth.test.ts
         Quick pass: lint ✓ typecheck ✓
         Scope item 3 [x]

       Running full pass...
         Lint: ✓  Typecheck: ✓  Build: ✓  Tests: 3/3 passing ✓

       Exit check:
         Must Have ACs: 2/2 ✓  Error ACs: 1/1 ✓  Scope: 3/3 ✓
         Gates: green  Blockers: 0

       CLEAN — Ready. Run `done`.

You:   done

Agent: Validating...
         All Must Have ACs [x] ✓
         All Error ACs [x] ✓
         New tests for new behavior ✓ (3 tests added)
         Existing tests passing ✓
         No lint/typecheck errors ✓
         No hardcoded secrets ✓

       Retro:
         Estimate: 2h → Actual: 1.5h (75%)
         Worked: Clean scope-to-AC mapping, no orphan work
         Didn't: Missed rate limiting — caught in review
         Next time: Add security checklist for auth features

       Proposing memory update...
         "Auth features should include rate limiting in quality checklist"
         → Update project agent config? [yes/no]

       Archived: specs/shipped/2025-01-29-jwt-auth.md

       Human actions: commit → push → deploy → verify
```

## User Journey: Spec to Production

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SPEC TO PRODUCTION                          │
│                                                                     │
│  YOU                           AGENT                     OUTPUT     │
│  ───                           ─────                     ──────     │
│                                                                     │
│  "plan add rate limiting"                                           │
│       │                                                             │
│       ├──────────────────▶  Parse idea                              │
│                             Select tier: mini                       │
│                             Write user journey:                     │
│                               ACTOR: API consumer                   │
│                               GOAL: Protected from abuse            │
│                               1. Client sends request               │
│                               2. System checks rate                 │
│                               3. Under limit → process              │
│                               E1. Over limit → 429 + Retry-After   │
│                             Write ACs (GIVEN/WHEN/THEN)             │
│                             Map scope ↔ ACs                         │
│                             Quality checklist                       │
│                             Dev-readiness: READY ──────▶ spec file  │
│                                                                     │
│  "ship"                                                             │
│       │                                                             │
│       ├──────────────────▶  Load spec, create tasks                 │
│                             Iteration 1: middleware ──▶ lint ✓      │
│                             Iteration 2: config ──────▶ lint ✓      │
│                                Dev review (5 perspectives)          │
│                             Iteration 3: tests ───────▶ lint ✓      │
│                             Full pass: lint ✓ types ✓               │
│                                         build ✓ test ✓              │
│                             Exit: all ACs ✓ ──────────▶ CLEAN      │
│                                                                     │
│  "also add per-user limits"   (MID-LOOP CHANGE)                    │
│       │                                                             │
│       ├──────────────────▶  PAUSE implementation                    │
│                             Update spec:                            │
│                               + scope item 4: per-user config      │
│                               + AC-4: GIVEN user config WHEN...     │
│                               + journey step 4                      │
│                             Re-check traceability                   │
│                             Update tasks                            │
│                             RESUME loop ───────────────▶ continues  │
│                                                                     │
│  "done"                                                             │
│       │                                                             │
│       ├──────────────────▶  Validate all ACs ✓                     │
│                             New tests exist ✓                       │
│                             No lint/type errors ✓                   │
│                             Retro captured                          │
│                             Memory update proposed                  │
│                             Spec archived ─────────────▶ shipped/   │
│                                                                     │
│  YOU (manual)                                                       │
│       │                                                             │
│       ├─ git commit + push                                          │
│       ├─ deploy                                                     │
│       └─ verify in production                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Key: The spec is updated at every stage. Mid-loop changes are captured in the spec BEFORE implementation. The spec is always the source of truth.

## Reading Order

```
Start here
    │
    ▼
┌──────────┐     Already know           ┌──────────────────────┐
│ README   │──── the basics? ──────────▶│ SKILL.md             │
│ (you are │                            │ (agent instructions)  │
│  here)   │                            └──────────────────────┘
└────┬─────┘
     │ Want to understand a phase?
     │
     ├── Plan:    references/actions/plan.md
     ├── Spike:   references/actions/spike.md
     ├── Ship:    references/actions/ship.md
     ├── Review:  references/actions/review.md
     ├── Done:    references/actions/done.md
     ├── Drop:    references/actions/drop.md
     └── Memory:  references/memory-update.md

     │ Need a pattern?
     │
     ├── Building: references/patterns/implementation.md
     ├── Planning: references/patterns/planning.md
     ├── Debugging: references/patterns/debugging.md
     ├── Deciding: references/patterns/decisions.md
     └── Decomposing: references/patterns/decomposition.md

     │ Want to customize output?
     │
     ├── Plan:    references/templates/plan-output.md
     ├── Spike:   references/templates/spike-output.md
     ├── Ship:    references/templates/ship-output.md
     ├── Review:  references/templates/review-output.md
     ├── Done:    references/templates/done-output.md
     ├── Drop:    references/templates/drop-output.md
     └── Status:  references/templates/status-output.md
```

**You don't need to read everything.** SKILL.md is the only file the agent loads. References are loaded on-demand when a phase triggers.

## How It Works

```
 YOU                          WORKFLOW                         OUTPUT
──────                        ────────                         ──────

 "plan {idea}"
      │
      ├───────────────────▶  Parse idea
                             User journey (MANDATORY)
                             Acceptance criteria (MANDATORY)
                             Scope ↔ AC mapping
                             Quality checklist
                             Plan review
                             Dev-readiness check ──────────▶  specs/active/{slug}.md
      │
 "ship"
      │
      ├───────────────────▶  Detect mode (ONE-SHOT / LOOP)
                             Resume state check
                             ┌─────────────────────┐
                             │     SHIP LOOP       │
                             │ build → review → fix│◄──┐
                             │ exit check (ACs)    │───┘ not clean
                             │ stuck detection     │
                             └────────┬────────────┘
                                      │ clean
                             Quality gates ────────────────▶  All ACs + scope [x]
      │
 "done"
      │
      ├───────────────────▶  Validate (ACs + tests + gates)
                             Capture retro
                             Propose memory update ────────▶  Agent config learning
                             Archive spec ─────────────────▶  specs/shipped/{slug}.md
      │
 YOU (manual)
      │
      ├─ git commit + push
      ├─ deploy
      └─ verify in production
```

### Lifecycle

```
┌──────────┐  plan   ┌──────────┐ review? ┌───────────┐ ready? ┌───────────┐
│   IDEA   │────────▶│  DRAFT   │────────▶│ REVIEWING │───────▶│ DEV_READY │
└──────────┘         └──────────┘         └───────────┘        └─────┬─────┘
                          ▲                    │                     │ ship
                          │ revise [?][!]      │                     ▼
                          └────────────────────┘               ┌───────────┐
                                                               │IMPLEMENTING│
┌──────────┐  done   ┌──────────┐  clean  ┌───────────┐       └─────┬─────┘
│ SHIPPED  │◄────────│  READY   │◄────────│   SHIP    │◄────────────┘
└──────────┘         └──────────┘         │   LOOP    │──── iterate
      │                                   └─────┬─────┘
      │              ┌──────────┐               │ stuck
      │              │ DROPPED  │◄── drop ──────┘
      ▼              └──────────┘
 specs/shipped/                   specs/dropped/
```

### Quality Gates

```
 Quick Pass (per edit)                Full Pass (before exit)
┌──────────────────────┐     ┌─────────────────────────────────────────┐
│ LINT ──▶ TYPECHECK   │     │ LINT ──▶ TYPECHECK ──▶ BUILD ──▶ TEST  │
│(changed)  (changed)  │     │(changed)   (full)      (full)  (related)│
└──────────────────────┘     └─────────────────────────────────────────┘
```

### Review Notation

```
[?] unclear    [!] risk    [+] add to scope
[-] cut scope  [~] rephrase   [ok] approved
```

## Customization

Edit the skill files directly. Install at user-level or project-level, then modify to match your needs.

```
workflow/
├── SKILL.md ──────────────────── Task templates, review systems, risk thresholds
├── references/
│   ├── actions/                  ← Action logic (what the agent does)
│   │   ├── plan.md ───────────── Spec requirements, dev-readiness gates, review rounds
│   │   ├── ship.md ───────────── Quality gates, iteration limits, exit criteria
│   │   ├── review.md ─────────── Perspectives (add/remove/change levels)
│   │   ├── done.md ───────────── Validation checklist, memory update settings
│   │   └── drop.md ───────────── Drop flow
│   │
│   ├── templates/                ← Output templates (what the agent returns to you)
│   │   ├── plan-output.md ────── Spec summary, codebase impact, analysis, readiness
│   │   ├── spike-output.md ───── Decision, findings, next step
│   │   ├── ship-output.md ────── Iteration progress, exit states, spec mutations
│   │   ├── review-output.md ──── Per-file findings, fix actions, verdict
│   │   ├── done-output.md ────── Validation results, retro, memory updates
│   │   ├── drop-output.md ────── Drop reason, learnings, reusable pieces
│   │   └── status-output.md ──── Current state, progress, suggested next action
│   │
│   ├── spec-template.md ─────── Spec structure, generation rules, validation
│   ├── quality-gates.md ──────── Gate levels (BLOCKING/ADVISORY/SKIP), commands
│   ├── session-management.md ── Progress tracking, resume, stuck detection
│   └── memory-update.md ─────── Memory update protocol, agent config targets
```

**Two layers of customization:**

| Layer | What to edit | Controls |
|-------|-------------|----------|
| **Actions** (`actions/*.md`) | Logic, gates, perspectives, limits | What the agent does |
| **Templates** (`templates/*-output.md`) | Output format, sections, wording | What the agent returns to you |

### Examples

**Change what the agent shows after plan:** Edit `templates/plan-output.md` — add/remove sections, change format.

**Change what review findings look like:** Edit `templates/review-output.md` — change format, add fields, adjust rules.

**Change quality gate commands:** Edit `quality-gates.md` — update auto-detection tables or add explicit commands.

**Add review perspectives:** Edit `actions/review.md` — add rows to the perspectives table.

**Skip typecheck:** Edit `quality-gates.md` — set Typecheck level to SKIP.

**Require manual spec review:** Edit `actions/plan.md` — set manual review gate to BLOCKING.

**Change iteration limits:** Edit `actions/ship.md` — update the "Default Iterations by Size" table.

**Change memory update behavior:** Edit `memory-update.md` — adjust categories, agent targets, or disable proposals.

---

## Key Principles

- **Spec = source of truth**: Always updated, always reflects reality
- **ACs define done**: Work finishes when all Must Have + Error ACs pass
- **New code = new tests**: Every new behavior must have tests (BLOCKING)
- **Two review systems**: Plan review (specs) + dev review (code)
- **Quality gates**: Auto-detected, skippable — edit skill files to configure
- **Ship loop**: Build → review → fix with stuck detection + escalation
- **Risk-aware**: Agent flags HIGH risk changes for human review
- **Context-aware memory updates**: Done phase reads existing rules, proposes thinking patterns + coding rules + project rules
- **Human controls deployment**: Agent codes and validates, you push and deploy
- **16 patterns**: Implementation, planning, debugging, decisions, decomposition
- **Agent-portable**: Capability fallbacks for agents without task tracking or shell access
