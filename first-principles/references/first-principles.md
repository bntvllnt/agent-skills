# First-Principles Decomposition (Reference)

Loaded when user invokes first-principles thinking specifically (not the 5-step algorithm).

## Core Definition

**First principles** = a foundational proposition that cannot be deduced from any other (Aristotle).

In Musk's usage: the **physical or economic atoms** of a problem — the things that *must* be true because of physics, materials, or unavoidable economic inputs.

**Reasoning by analogy** = "X is like Y; do what Y does." Cheap, fast, and the source of most inherited cost.

## The 4-Step Process

### 1. STATE the Inherited Belief

Write the assumption verbatim, with quote marks. Examples:

- "Batteries will always cost $600/kWh."
- "Rockets are expendable."
- "Enterprise software has to take 18 months to deploy."
- "Customer support requires N people per X tickets."

If you cannot state it in one sentence with quote marks, you do not yet understand what you are challenging.

### 2. DECOMPOSE to Atoms

For each belief, list the **smallest physically/economically irreducible components**.

| Belief Type | Atoms To List |
|-------------|---------------|
| Cost belief | Raw materials, labor-hours at market rate, energy, capital amortized over volume |
| Time belief | Critical-path operations, physical limits (speed of light, chemical reaction time) |
| Capability belief | Physical laws, material properties, information-theoretic limits |
| Process belief | Inputs required by physics/regulation vs inputs required by current org |

**Rule**: Every atom must be defensible against the question *"is this required by physics, or by convention?"*

If the answer is "convention" — it is **not** an atom. It is a candidate for deletion.

### 3. PRICE / COMPUTE the Floor

Sum the atoms at their irreducible cost / time / size.

Sources:

- London Metal Exchange spot prices (materials)
- Energy markets (kWh, fuel)
- Physical constants (rocket equation, thermodynamics, information theory)
- Cloud commodity pricing (compute, storage, bandwidth)

The result is the **floor** — the lowest the thing can be without violating physics or markets.

### 4. RECONSTRUCT

The gap between the floor and the current reality is the opportunity.

```
Current Cost: $A
Floor:        $X
─────────────────
Gap:          $A − $X  ← this is the entire opportunity
```

Where the gap comes from (in order of typical magnitude):

1. **Inherited margin chains** — vendor → integrator → reseller, each adds 20-50%.
2. **Volume / scale** — the floor assumes scale; current may be sub-scale.
3. **Process design** — built around analog (the old way), not the floor.
4. **Smart-people overhead** — each layer of abstraction added by experts.
5. **Regulatory / safety floor** — sometimes real, often inherited.

The reconstructed path picks one or more of these to attack — directly, not by analog.

## Reasoning-by-Analogy Detector

When you (or anyone) say one of these, **stop**:

| Phrase | Analogy Hidden Inside |
|--------|------------------------|
| "Industry standard..." | The whole industry is the analogy |
| "Best practice..." | Best for whose problem? |
| "Vendors charge..." | Vendor pricing is a market analog, not a floor |
| "It's always been..." | Tradition is an analog |
| "Everyone does..." | The herd is an analog |
| "The textbook says..." | Curated past, not your problem |
| "In our industry..." | Industry boundaries are themselves analogs |

For each, ask: **what physical or economic atom forces this?** If none, it is a candidate for replacement.

## Output Template

```markdown
## First-Principles Brief: [Problem]

### Stated Constraint
"[verbatim quote of the inherited belief]"

### Atoms (Fundamentals)
| Component | Quantity | Unit Cost / Limit | Source | Required by physics? |
|-----------|----------|-------------------|--------|----------------------|
| ...       | ...      | ...               | ...    | yes/no                |

### Irreducible Floor
**[$X / Y units]**

### Current Reality
**[$A / B units]** — [ratio]× the floor.

### Gap Decomposition
1. [Inherited margin / scale / process / overhead] — ~$Z
2. ...

### Analogies Identified
- [Analogy 1]: [what's the underlying atom?] [is it real?]
- ...

### Reconstructed Path
[Step-by-step approach that targets the gap, not the analog]

### What Would Falsify This
[The specific evidence that would invalidate the floor or the gap analysis]
```

## Common Mistakes

| Mistake | Why it fails | Fix |
|---------|--------------|-----|
| Decomposing without re-pricing at floor | You restate the problem in atoms but inherit market price | Use commodity / spot prices, not vendor quotes |
| Stopping at decomposition | You found the floor but didn't reconstruct | Step 4 is mandatory; without it, this is just analysis |
| Treating "regulation" as physics | Some regulations are inherited; some are physical safety | Trace each regulation to its origin |
| Calling smart-people overhead "irreducible" | Smart additions feel necessary; usually aren't | Apply step 1 of the 5-step algorithm to them |

## Cross-Reference

- After running this on a problem, run `references/algorithm.md` on the *solution* you reconstruct.
- See `references/case-studies.md` for battery, SpaceX, Tesla worked examples.
