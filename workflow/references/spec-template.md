# Spec Template (SINGLE SOURCE OF TRUTH)

> **Agent:** Load this file when `plan` triggers. Follow generation order exactly — each section feeds the next.

This file defines the spec structure, generation rules, and validation. All spec creation follows this template exactly. `plan.md` orchestrates WHEN — this file defines WHAT.

Save specs to: `specs/active/{YYYY-MM-DD}-{slug}.md`

---

## Generation Order

Sections MUST be generated in this order. Each section feeds the next.

```
1. Context           ← from user input
2. Codebase Impact   ← from reading the actual codebase (MANDATORY)
3. User Journey      ← from context + codebase understanding (MANDATORY)
4. Acceptance Criteria ← derived from journey steps (MANDATORY)
5. Scope             ← derived from ACs + codebase impact
6. Quality Checklist ← derived from scope + codebase patterns
7. Risks             ← from codebase impact + pre-mortem
8. State Machine     ← if stateful (from journey analysis)
9. Analysis          ← improvements, gaps, questions (MANDATORY output)
```

**Rule: Never skip ahead. Journey drives ACs. ACs drive scope. Codebase drives everything.**

---

## Template Sections

Each section below shows: the template (what goes in the spec) then the generation rules (how to write it).

<!-- TEMPLATE: Front Matter + Context -->

### Section: Front Matter + Context

**Spec output:**

    ---
    title: {Feature Title}
    status: active
    created: {YYYY-MM-DD}
    estimate: {N}h
    tier: {trivial|micro|mini|standard}
    ---

    # {Feature Title}

    ## Context

    {Why this feature exists. What problem it solves. 2-3 sentences max.}

**Generation rules:**
- Extract from user input: WHAT (feature), WHY (problem), WHO (persona)
- If user didn't state WHY → ask or infer and note the assumption

---

<!-- TEMPLATE: Codebase Impact -->

### Section: Codebase Impact

**Spec output:**

    ## Codebase Impact (MANDATORY)

    | Area | Impact | Detail |
    |------|--------|--------|
    | {file/module/area} | CREATE | {what and why} |
    | {file/module/area} | MODIFY | {what changes and why} |
    | {file/module/area} | AFFECTED | {indirect impact — consumers, imports, tests} |

    **Files:** {N} create | {N} modify | {N} affected
    **Reuse:** {existing patterns, utils, hooks, middleware, schemas to leverage — or "None identified"}
    **Breaking changes:** {none / list with migration path}
    **New dependencies:** {none / package name + justification + alternatives considered}

**Generation rules:**
- **MANDATORY: Read the codebase before writing anything else.**
- Search for related code: grep keywords, read affected files, check existing patterns
- Map every file that will be created, modified, or indirectly affected
- Identify code to reuse — never reinvent what exists
- Flag breaking changes to exports, APIs, schemas, config
- Flag new dependencies with justification
- **If agent hasn't read the codebase → spec is NOT_READY**
- **Fallback:** If code search tools are unavailable, ask the user to provide affected file paths and existing patterns

---

<!-- TEMPLATE: User Journey -->

### Section: User Journey

**Spec output:**

    ## User Journey (MANDATORY)

    ### Primary Journey

    ACTOR: {who — user type/persona}
    GOAL: {what they want to accomplish}
    PRECONDITION: {what must be true before starting}

    1. User {action}
       → System {response}
       → User sees {outcome}

    2. User {action}
       → System {response}
       → User sees {outcome}

    3. User {action}
       → System {response}
       → User sees {final outcome}

    POSTCONDITION: {what is now true}

    ### Error Journeys

    E1. {Error scenario name}
       Trigger: {what goes wrong}
       1. User {action}
          → System {detects error}
          → User sees {error message/state}
       2. User {recovery action}
          → System {recovers}
       Recovery: {end state after recovery}

    E2. {Error scenario name}
       Trigger: {what goes wrong}
       ...

    ### Edge Cases

    EC1. {Edge case}: {what happens}
    EC2. {Edge case}: {what happens}

**Generation rules:**
- Write BEFORE scope — journey drives scope, not the other way around
- Informed by codebase impact: what does the system already do? What's changing?
- Primary journey: happy path from start to finish
- Error journeys: at least 1 required (BLOCKING)
- Edge cases: empty inputs, boundaries, concurrent users, permissions
- Be specific: "{user sees error toast with message}" not "{user sees error}"
- ACTOR/GOAL/PRECONDITION/POSTCONDITION are all required

---

<!-- TEMPLATE: Acceptance Criteria -->

### Section: Acceptance Criteria

**Spec output:**

    ## Acceptance Criteria (MANDATORY)

    ### Must Have (BLOCKING — all must pass to ship)

    - [ ] AC-1: GIVEN {context from journey step} WHEN {action} THEN {observable result}
    - [ ] AC-2: GIVEN {context} WHEN {action} THEN {result}
    - [ ] AC-3: GIVEN {context} WHEN {action} THEN {result}

    ### Error Criteria (BLOCKING — all must pass)

    - [ ] AC-E1: GIVEN {error context from E1} WHEN {trigger} THEN {graceful handling}
    - [ ] AC-E2: GIVEN {error context} WHEN {trigger} THEN {handling}

    ### Should Have (ship without, fix soon)

    - [ ] AC-4: GIVEN {nice-to-have context} WHEN {action} THEN {result}

**Generation rules:**
- Derive directly from user journey — every journey step → at least 1 AC
- Every error journey → at least 1 AC-E
- Format: GIVEN/WHEN/THEN — no exceptions
- Every AC must be pass/fail — no ambiguity, no "should feel smooth"
- Every AC must be testable (manual or automated)
- Minimum: 1 Must Have AC + 1 Error Criterion
- ACs are the EXIT GATE for `ship` — work is DONE when all Must Have + Error ACs pass

---

<!-- TEMPLATE: Scope -->

### Section: Scope

**Spec output:**

    ## Scope

    - [ ] 1. {First deliverable — verb + noun} → AC-1, AC-2
    - [ ] 2. {Second deliverable} → AC-3
    - [ ] 3. {Third deliverable} → AC-E1, AC-E2

    ### Out of Scope

    - {What this feature does NOT include — set boundaries}

**Generation rules:**
- Derive from ACs + codebase impact — scope items are implementation tasks
- Each item: verb + noun + measurable outcome
- Each item MUST map to at least 1 AC (no orphan scope)
- Each Must Have AC MUST map to at least 1 scope item (no uncovered AC)
- Inform by codebase: if existing code handles part of it, scope is smaller
- Out of Scope: explicitly state what's NOT included to prevent scope creep

**Traceability Check (BLOCKING):**

```
orphan_scope = scope items with no AC mapping     → CUT
uncovered_ac = Must Have ACs with no scope item    → ADD scope item
Result: every scope ↔ at least 1 AC, bidirectional
```

---

<!-- TEMPLATE: Quality Checklist -->

### Section: Quality Checklist

**Spec output:**

    ## Quality Checklist

    ### Blocking (must pass to ship)

    - [ ] All Must Have ACs passing
    - [ ] All Error Criteria ACs passing
    - [ ] All scope items implemented
    - [ ] No regressions in existing tests
    - [ ] Error states handled (not just happy path)
    - [ ] No hardcoded secrets or credentials
    - [ ] {Domain-specific blocking item from codebase analysis}

    ### Advisory (should pass, not blocking)

    - [ ] All Should Have ACs passing
    - [ ] Code follows existing project patterns
    - [ ] {Domain-specific advisory item}

**Generation rules:**
- Always include the 6 baseline blocking items above
- Add domain-specific items using Socratic questions per scope item:
  - "What would make this FAIL in production?"
  - "What edge case would a user hit first?"
  - "What would break if this input were empty/null/huge?"
- Informed by codebase: what patterns does this project enforce?
- Mark each item `[blocking]` or `[advisory]`

---

<!-- TEMPLATE: Risks -->

### Section: Risks

**Spec output:**

    ## Risks

    | Risk | Impact | Likelihood | Mitigation |
    |------|--------|------------|------------|
    | {risk from codebase impact} | HIGH/MED/LOW | HIGH/MED/LOW | {mitigation} |
    | {risk from pre-mortem} | HIGH/MED/LOW | HIGH/MED/LOW | {mitigation} |

    **Kill criteria:** {When to abandon this approach entirely}

**Generation rules (standard tier):**
- Pre-mortem: assume the feature failed — why?
- Informed by codebase: breaking changes, migration risks, dependency risks
- Every HIGH risk MUST have a mitigation
- Kill criteria: define when to stop and rethink

---

<!-- TEMPLATE: State Machine -->

### Section: State Machine

**Spec output:**

    ## State Machine

    {For stateful features only. Delete section if stateless.}

    ┌────────┐   event    ┌─────────┐
    │ STATE1 │───────────▶│ STATE2  │
    └────────┘            └─────────┘

    States: {list with data shapes}
    Transitions: {triggers + guards}
    Invalid transitions: {prevention strategy}
    Race conditions: {analysis}

**Generation rules:**
- Required for stateful features (forms, wizards, async flows, status tracking)
- Stateless features: delete section or write "N/A — stateless feature"
- Include ASCII transition diagram
- Map all valid + invalid transitions

---

<!-- TEMPLATE: Analysis + Tracking -->

### Section: Analysis + Tracking

**Spec output:**

    ## Analysis

    ### Improvements
    - {Suggestion to strengthen the spec, architecture, or approach}
    - {Alternative approach worth considering}

    ### Gaps
    - {Unknown that could affect implementation}
    - {Assumption that needs validation}

    ### Questions
    - {Question for the user — answer before ship or accept defaults}
    - {Clarification needed on ambiguous aspect}

    ## Notes

    {Empty at creation. Filled during implementation. Retro goes here.}

    ## Progress

    | # | Scope Item | Status | Iteration |
    |---|-----------|--------|-----------|

    ## Timeline

    | Action | Timestamp | Duration | Notes |
    |--------|-----------|----------|-------|
    | plan | {ISO_TIMESTAMP} | - | Created |

**Generation rules (MANDATORY output):**
- **Improvements**: proactive suggestions the user hasn't considered
  - Better patterns, simpler approaches, existing code to leverage
  - Architectural alternatives worth weighing
- **Gaps**: unknowns that won't block dev but should be tracked
  - Assumptions made that could be wrong
  - Areas where requirements are ambiguous
- **Questions**: things the agent can't resolve alone
  - Preference decisions, business logic clarifications
  - If no questions: "None — requirements are clear"
- **Be proactive**: flag edge cases, perf concerns, security implications, UX issues the user hasn't mentioned

---

## Mini Tier Template

For <100 LOC features. Same rules, shorter format. Codebase Impact + Journey + ACs still MANDATORY.

**Spec output:**

    ---
    title: {Title}
    status: active
    created: {YYYY-MM-DD}
    estimate: {N}h
    tier: mini
    ---

    # {Title}

    ## Codebase Impact

    | Area | Impact | Detail |
    |------|--------|--------|
    | {area} | CREATE/MODIFY | {detail} |

    **Reuse:** {what to leverage}

    ## User Journey

    1. User {action} → sees {result}
    2. User {action} → sees {result}
    Error: {what goes wrong} → sees {error state}

    ## Acceptance Criteria

    - [ ] AC-1: GIVEN {context} WHEN {action} THEN {result}
    - [ ] AC-2: GIVEN {context} WHEN {action} THEN {result}
    - [ ] AC-E1: GIVEN {error} WHEN {trigger} THEN {handling}

    ## Scope

    - [ ] 1. {deliverable} → AC-1
    - [ ] 2. {deliverable} → AC-2

    ## Quality Checklist

    - [ ] All ACs passing
    - [ ] No regressions
    - [ ] Error states handled

    ## Analysis

    **Improvements:** {or "None"}
    **Gaps:** {or "None"}
    **Questions:** {or "None — requirements clear"}

    ## Notes

    ## Timeline

    | Action | Timestamp | Duration | Notes |
    |--------|-----------|----------|-------|
    | plan | {ISO_TIMESTAMP} | - | Created |

---

## Validation Rules (BLOCKING for dev-readiness)

A spec missing ANY of these cannot proceed to `ship`.

| # | Rule | Check | Blocking |
|---|------|-------|----------|
| 1 | Codebase analyzed | `## Codebase Impact` is non-empty, files listed | YES |
| 2 | Journey exists | `## User Journey` section is non-empty | YES |
| 3 | Journey has actor + goal | ACTOR and GOAL defined | YES |
| 4 | Journey has error path | At least 1 error journey (E1) | YES |
| 5 | ACs exist | `## Acceptance Criteria` section is non-empty | YES |
| 6 | ACs use GIVEN/WHEN/THEN | Every AC follows the format | YES |
| 7 | ACs have Must Have | At least 1 Must Have AC | YES |
| 8 | ACs have Error Criteria | At least 1 AC-E error criterion | YES |
| 9 | Scope maps to ACs | Every scope item references an AC | YES |
| 10 | ACs map to scope | Every Must Have AC is covered by scope | YES |
| 11 | No orphan scope | Scope item with no AC mapping → cut | YES |
| 12 | No uncovered AC | Must Have AC with no scope item → add scope | YES |
| 13 | Analysis present | Improvements + Gaps + Questions sections exist | YES |

---

## Plan Output

Follow the output template in `references/templates/plan-output.md`.
