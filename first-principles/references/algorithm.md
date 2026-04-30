# The 5-Step Algorithm (Reference)

Musk's engineering algorithm, recorded during the Everyday Astronaut Starbase tour (2021). Five steps, in order. Reordering them is the single most common engineering failure.

## The Steps

```
1. MAKE THE REQUIREMENTS LESS DUMB
2. DELETE THE PART OR PROCESS
3. SIMPLIFY AND OPTIMIZE
4. ACCELERATE CYCLE TIME
5. AUTOMATE
```

## Why Order Matters

Each step exposes work that the next step would otherwise waste effort on:

- Step 1 catches dumb requirements before they become parts (step 2 work).
- Step 2 deletes parts before they get optimized (step 3 work).
- Step 3 simplifies what survives before it gets sped up (step 4 work).
- Step 4 reduces cycle time before it gets automated (step 5 work).

**Anti-pattern**: starting at step 5. You will automate the broken process at high speed, and the breakage will scale.

## Step 1 — Make the Requirements Less Dumb

> "The requirements are definitely dumb. It does not matter who gave them to you. It is particularly dangerous if a smart person gave them to you, because you may not question them enough."

### Process

For every requirement on the system:

| Field | Value |
|-------|-------|
| Requirement text | (verbatim) |
| Owner (who set it) | name |
| Origin date | when set |
| Original problem it was solving | what was true then? |
| Still true today? | yes / no / unknown |
| Verdict | keep / dumb / unknown — investigate |

### Pass Criterion

Every requirement traces to (a) physics, (b) regulation with cited statute, (c) explicit customer/market need, OR is removed.

### Watch For

- "We've always required this" — often a fence to investigate (Chesterton).
- "[Senior person] wanted it" — dangerous; smart-people requirements get over-respected.
- "Just to be safe" — quantify the unsafe scenario or remove.
- Specs lifted from a previous project — context-dependent; re-derive.

## Step 2 — Delete the Part or Process

> "If you are not occasionally adding things back in, you are not deleting enough."

### Process

For every part/step that survived Step 1:

1. Try to delete it entirely.
2. Build / run / test without it.
3. Measure: did anything actually break?
4. If no — keep deleted.
5. If yes — add back the *minimum* needed.

Track the **add-back rate**: number of deletions reverted / total deletions attempted.

### Pass Criterion

Add-back rate < 10%. Higher means you weren't aggressive enough.

### Watch For

- Parts whose only job is to fix other parts — delete the chain.
- Configuration that exists "in case someone needs it" — delete.
- Layers of abstraction with one consumer — delete the layer.
- Tests for deleted code — delete.
- Comments / docs about deleted code — delete.

## Step 3 — Simplify and Optimize

> "This step is third — not first — because the most common error of a smart engineer is to optimize a thing that should not exist."

### Process

For what survived Step 2:

1. Reduce parameter count / surface area.
2. Combine sequential operations that share state.
3. Eliminate vestigial branches (if A then... when A is no longer reachable).
4. Replace complex with simple where same outcome holds.

### Pass Criterion

Could a new engineer understand the system in one sitting?

### Watch For

- "Premature simplification" is also possible — don't merge things that *should* stay separate.
- Optimization for benchmarks that don't reflect real load.

## Step 4 — Accelerate Cycle Time

> "Every process can be sped up. But only after the first three steps. Going faster on a process that should not exist is foolish."

### Process

1. Map the critical path.
2. Identify wait states / serial dependencies.
3. Parallelize what can be parallelized.
4. Batch what's serial.
5. Cache what's recomputed.

### Pass Criterion

Critical path latency reduced measurably. Document baseline → after.

### Watch For

- Adding parallelism that introduces races without speedup.
- Caching adding stale-data bugs without measured win.
- Speeding up a step that wasn't on the critical path (no overall improvement).

## Step 5 — Automate

> "Last. Most people do this first."

### Process

For each step that has been:

- Stripped of dumb requirements (Step 1)
- Stripped of unneeded parts (Step 2)
- Simplified (Step 3)
- Sped up (Step 4)

…ask: is this stable enough that automating it locks in good behavior, not waste?

If yes, automate.

If unsure, leave manual until the process is stable.

### Pass Criterion

Automation reduces human-touch on stable, well-understood steps. Variability in upstream output is not absorbed by automation (that's automation as workaround — anti-pattern).

### Watch For

- Automating something that fails 5% of the time — you've automated the failure.
- Automation that requires constant config tweaks — process isn't stable.
- "We need automation to scale" without first asking *should we be doing this at all*.

## Per-System Output Template

```markdown
## 5-Step Pass: [System / Process Name]

**Baseline metrics**: [cycle time / cost / headcount / error rate]

### Step 1: Requirements
| Requirement | Owner | Origin | Still valid? | Verdict |
|-------------|-------|--------|--------------|---------|
| ... | ... | ... | ... | ... |
**Removed**: [list]
**Investigated**: [list of "unknown" requirements traced to source]

### Step 2: Deletions
| Part / step | Why removed | Add-back? | Reason for add-back |
|-------------|-------------|-----------|---------------------|
| ... | ... | yes/no | ... |
**Add-back rate**: X% (target <10%)

### Step 3: Simplifications
| Before | After | Why simpler |
|--------|-------|-------------|
| ... | ... | ... |

### Step 4: Cycle-Time Wins
| Stage | Before | After | Method |
|-------|--------|-------|--------|
| ... | ... | ... | parallelize / batch / cache |
**Critical path**: [before] → [after]

### Step 5: Automation
| Step | Automated? | Why / why not |
|------|------------|---------------|
| ... | yes/no | stable / unstable / human-judgment-required |

### Final Metrics
| Metric | Baseline | After |
|--------|----------|-------|
| Cycle time | ... | ... |
| Cost | ... | ... |
| Headcount | ... | ... |
| Error rate | ... | ... |
```

## Cross-Reference

- For *cost* / *constraint* beliefs (not process design), use `references/first-principles.md`.
- For worked examples, see `references/case-studies.md`.
