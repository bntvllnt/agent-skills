---
name: first-principles
description: |
  First-principles thinking + 5-step engineering algorithm (popularized by Elon Musk). Break problems down to fundamental physics/economics and rebuild solutions from scratch. Counters reasoning-by-analogy, inherited constraints, and premature optimization.
  Auto-activates on: "first principles", "first-principles", "boil down to fundamentals", "decompose to atoms", "physics first", "reasoning by analogy", "challenge industry norm", "5-step algorithm", "musk algorithm", "make requirements less dumb", "delete the part", "what does the physics say".
license: MIT
compatibility: Agent-agnostic. No external tools required.
metadata:
  version: "1.0"
allowed-tools: Read Glob Grep
---

# First Principles

Two complementary frameworks for cutting through inherited constraints:

1. **First-Principles Thinking** — *how to reason*: decompose to fundamentals, then reason up.
2. **The 5-Step Algorithm** — *how to engineer*: requirements → delete → simplify → accelerate → automate, in order.

Use Framework 1 when challenging assumptions and pricing/cost beliefs. Use Framework 2 when designing/optimizing a process or system. They compose: do (1) on the problem, then (2) on the solution.

## When to Use

| Situation | Framework | Why |
|-----------|-----------|-----|
| "We can't because [industry assumption]" | First Principles | Test if constraint is real or inherited |
| "It costs $X because that's the market price" | First Principles | Cost from materials + physics, not market |
| "Everyone does it like this" | First Principles | Reasoning-by-analogy detected |
| Designing a new process/system | 5-Step Algorithm | Order prevents premature optimization |
| Existing process is slow/expensive | 5-Step Algorithm | Most overhead is in step 1 (dumb requirements) |
| Both: a hard problem with cost + design | 1 then 2 | Reframe problem (1), then build solution (2) |

## Router

| User says | Load reference | Do |
|---|---|---|
| "elon first principles" / "musk first principles" / "boil down to fundamentals" | `references/first-principles.md` | Run 4-step decomposition |
| "what does the physics say" / "physics-first" / "decompose to atoms" | `references/first-principles.md` | Run physical-cost decomposition |
| "musk algorithm" / "5-step algorithm" / "make requirements less dumb" | `references/algorithm.md` | Run 5 steps in order |
| "delete the part" / "delete this step" | `references/algorithm.md` | Apply step 2 specifically |
| "reasoning by analogy" / "challenge industry norm" | `references/first-principles.md` | Surface analogy → replace with first-principles |
| Show worked examples | `references/case-studies.md` | Battery / SpaceX / Tesla manufacturing |

---

## Framework 1: First-Principles Thinking

> "Boil things down to their fundamental truths and reason up from there, as opposed to reasoning by analogy." — Musk

### The 4-Step Decomposition

```
┌──────────────────────────────────────────────────┐
│ 1. STATE the assumption / inherited belief        │
│    "X must cost / take / require Y"               │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 2. DECOMPOSE to fundamentals                      │
│    What atoms / physical quantities / unavoidable │
│    economic inputs is this actually made of?      │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 3. PRICE / COMPUTE the irreducible floor          │
│    Sum the fundamentals at market / physical limit│
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 4. RECONSTRUCT — figure out how to combine them   │
│    Gap between floor and current = opportunity    │
└──────────────────────────────────────────────────┘
```

### Reasoning-by-Analogy Detector

Stop and run Framework 1 when you hear:

- "Industry standard is..."
- "Everyone does it like this"
- "It's always been..."
- "Best practice says..."
- "The market price is..."
- "Vendors charge..."

These are analogy-flags. Each one is a candidate for decomposition.

### Output Template

```markdown
## First-Principles Brief: [Problem]

### Stated Constraint
[What everyone says is true / required / unavoidable]

### Fundamentals (Atoms)
| Component | Quantity | Unit Cost / Physical Limit | Source |
|-----------|----------|----------------------------|--------|
| ...       | ...      | ...                        | ...    |

### Irreducible Floor
**Total: [$X / Y kg / Z seconds]**

### Current Reality
**[$A / B kg / C seconds]** — gap of [ratio]× over the floor.

### Where the Gap Comes From
1. [Inherited assumption / margin / process step]
2. ...

### Reconstructed Path
[Solution that approaches the floor — not the analog]
```

---

## Framework 2: The 5-Step Algorithm

> "Most of these mistakes I will catch — but I cannot bat 1000." — Musk, on why order matters

Order is not optional. Run steps in sequence. Skipping ahead causes the most common failure mode: **optimizing or automating a dumb process**.

### Steps (in order)

```
1. MAKE THE REQUIREMENTS LESS DUMB
   Every requirement is wrong. Especially smart-people requirements.
   Question who set it, when, and what they actually needed.

2. DELETE THE PART OR PROCESS
   If you're not adding back at least 10% of what you delete, you didn't delete enough.

3. SIMPLIFY AND OPTIMIZE
   Only AFTER deleting. Otherwise you're polishing a vestige.

4. ACCELERATE CYCLE TIME
   Speed up what survived. Not before — you'll just speed up wasted work.

5. AUTOMATE
   Last. Automating a broken process scales the breakage.
```

### Common Failure Mode

```
WRONG ORDER (most common):
  AUTOMATE → SIMPLIFY → DELETE → REQUIREMENTS
  → automating dumb requirements at high speed.

RIGHT ORDER:
  REQUIREMENTS → DELETE → SIMPLIFY → ACCELERATE → AUTOMATE
```

### Per-Step Checklist

| Step | Question | Pass Criterion |
|------|----------|----------------|
| 1 | Is this requirement physically/economically necessary, or inherited? | Owner + reason traced; dumb ones removed |
| 2 | Can this part/step be removed entirely? | <10% add-back rate after deletion |
| 3 | Is what remains the simplest form? | No vestigial branches, configs, layers |
| 4 | Where is cycle time spent? Can it be parallelized? | Critical path measured + reduced |
| 5 | Is this stable enough to automate without locking in waste? | Steps 1-4 PASS first |

### Output Template

```markdown
## 5-Step Pass: [System / Process]

### 1. Requirements
| Requirement | Owner | Origin | Verdict (keep/dumb/unknown) |
|-------------|-------|--------|------------------------------|
| ...         | ...   | ...    | ...                          |
**Removed**: [list dumb requirements]

### 2. Deletions
| Part / Step | Why removed | Add-back? |
|-------------|-------------|-----------|
| ...         | ...         | yes/no    |
**Add-back rate**: X% (target <10% — if higher, delete more aggressively next pass)

### 3. Simplifications
[What survived deletion, simplified]

### 4. Cycle-Time Wins
| Stage | Before | After | Method |
|-------|--------|-------|--------|
| ...   | ...    | ...   | parallelize / batch / cache |

### 5. Automation
[What was stable + worth automating, and what was deliberately left manual]
```

---

## Composition: Framework 1 → Framework 2

For hard problems with both cost beliefs AND a process to build:

```
Framework 1 (decompose problem)
        │
        ▼
"The floor is $X. Current is $A. Gap = $A - $X."
        │
        ▼
Framework 2 (build the path to the floor)
        │
        ▼
Step 1: which requirements caused the gap?
Step 2: which parts/steps in the current process are the gap?
Step 3-5: simplify, accelerate, automate the survivors.
```

---

## Quick Examples

### Battery Cost (Framework 1)

| Stated | "Batteries cost $600/kWh, will always be expensive" |
| Atoms | Cobalt + nickel + aluminum + carbon + polymers + steel can |
| Floor | ~$80/kWh at LME spot prices for the raw materials |
| Gap | 7.5× — comes from cell design, manufacturing scale, vendor margins |
| Reconstruct | Gigafactory: own the cell + scale + integrate |

### Rocket Cost (Framework 1 → 2)

| Stated | "Rockets cost $65M, single-use, that's just how it is" |
| Atoms | Aluminum + copper + carbon fiber + propellant ≈ ~2% of price |
| Floor | Materials + fuel ≈ low-single-digit millions |
| Gap | Throwing the rocket away. Reasoning by analogy: "rockets are expendable" |
| Reconstruct | Land + reuse → 5-Step Algorithm on landing process (delete legs? no — required by physics) |

### Manufacturing Line (Framework 2)

| 1. Requirements | "Body panels need 4 fasteners here" — origin: legacy CAD → reduce to 2 |
| 2. Delete | Remove 30% of stations after audit; add-back rate 8% |
| 3. Simplify | Merge two welding steps; eliminate one fixture |
| 4. Accelerate | Parallelize paint cure with sub-assembly |
| 5. Automate | Only the survived, simplified stations |

---

## Anti-Patterns (NEVER)

- NEVER apply step 4 or 5 of the algorithm before steps 1-3 — you scale waste.
- NEVER accept "industry standard" as a fundamental — it is an analogy by definition.
- NEVER decompose to fundamentals and stop there — you must reconstruct (step 4 of Framework 1).
- NEVER use first-principles to justify ignoring physical limits. The floor is real; the inherited markup is not.
- NEVER skip step 1 of the algorithm because requirements "came from someone smart". Smart-people requirements are the hardest to question and the most expensive to keep.
- NEVER delete a Chesterton's Fence requirement without tracing its origin. If origin = "physics" or "regulation", keep. If origin = "we always did it" — delete.

---

## Smoke Test

User: *"This service costs us $50k/month. Vendors all charge in that range — what can we do?"*

Expected activation: First Principles.

Expected response: Decompose the $50k into compute + storage + bandwidth + vendor margin. Compute the cloud-floor at on-demand pricing. Identify gap. Then run 5-Step Algorithm on the integration to approach the floor.

---

## References

- `references/first-principles.md` — full decomposition workflow + analogy detector
- `references/algorithm.md` — 5-step algorithm with deeper checklists per step
- `references/case-studies.md` — battery, SpaceX, Tesla manufacturing, software examples
