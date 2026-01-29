# Debugging Patterns

## Scientific Method

Hypothesis-driven debugging. No random changes.

**When:** Any non-trivial bug. Default approach.

```
Phase 1: SYMPTOM CAPTURE
  - Exact error message/behavior
  - Steps to reproduce
  - When it started (last known good state)
  - Environment details

Phase 2: HYPOTHESIS FORMATION
  Rank by likelihood:
  H1: {most likely cause} (probability: X%)
  H2: {second most likely} (probability: Y%)
  H3: {least likely} (probability: Z%)

Phase 3: TEST HYPOTHESES
  For each hypothesis (highest probability first):
    Design minimal test that proves/disproves
    Execute test
    Record result: CONFIRMED / ELIMINATED
    If confirmed → Phase 5
    If eliminated → next hypothesis

Phase 4: BINARY SEARCH (if no hypothesis confirmed)
  git bisect or manual binary elimination:
    Find last known good commit
    Bisect to identify breaking change

Phase 5: ROOT CAUSE CONFIRMATION
  - Can you explain WHY it broke, not just WHERE?
  - Does the fix make the reproduction case pass?
  - Are there related occurrences of the same pattern?
```

**Key rule:** Never make a change without a hypothesis for why it will fix the bug.

---

## Root Cause Analysis

Go deeper than the immediate fix. Prevent recurrence.

**When:** Bug keeps coming back, systemic issues, post-incident review.

### 5 Whys

```
Problem: {symptom}
Why 1: {immediate cause}
Why 2: {cause of cause}
Why 3: {deeper cause}
Why 4: {systemic cause}
Why 5: {root cause}
→ Fix at level 4-5, not level 1
```

### Fishbone (Ishikawa) Diagram

```
                    ┌──── Code ────── {cause}
                    ├──── Data ────── {cause}
{symptom} ◄─────────┤
                    ├──── Environment ── {cause}
                    ├──── Config ───── {cause}
                    └──── External ─── {cause}
```

**Root cause test:** If you fix this, does the problem NEVER recur? If not, dig deeper.

**Contributing causes:** Multiple factors that must all be present. Fix any one to prevent.

---

## Minimal Reproduction

Reduce the problem to its smallest form.

**When:** Complex bugs, hard to isolate, environment-dependent issues.

```
Strategy: BINARY REMOVAL
1. Start with full reproduction case
2. Remove half the code/config/data
3. Bug still present? Remove another half of remaining
4. Bug gone? Restore last removal, remove other half
5. Repeat until minimal case found
```

**Reproduction patterns by bug type:**

| Bug Type | Isolation Technique |
|----------|-------------------|
| UI rendering | Single component in isolation (Storybook) |
| API error | Standalone request (curl/httpie) |
| State bug | Minimal state + single action |
| Race condition | Add delays to force ordering |
| Data corruption | Minimal dataset that triggers issue |
| Environment | Docker/devcontainer with minimal config |

---

## Instrumentation Patterns

Add observability to understand behavior.

**When:** Bug not reproducible, need runtime evidence, production debugging.

**4 levels:**

| Level | What | When |
|-------|------|------|
| 1. Console | console.log/print at key points | Quick local debugging |
| 2. Structured | JSON logs with context (request ID, user, timestamp) | Multi-step flows |
| 3. Tracing | Span-based tracing across functions/services | Distributed systems |
| 4. Metrics | Counters, histograms, gauges | Performance/capacity issues |

**Strategic placement:**
- Function entry/exit with arguments and return values
- Branch points (which path was taken?)
- External calls (request + response + timing)
- State mutations (before + after)
- Error catch blocks (full context)

**Cleanup rule:** Remove debug instrumentation before committing. Use feature flags for persistent observability.
