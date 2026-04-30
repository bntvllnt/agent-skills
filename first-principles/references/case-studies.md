# Case Studies (Reference)

Worked examples of both frameworks. Loaded when user asks for examples or wants to calibrate against real applications.

## 1. Tesla Battery Cost (Framework 1)

### Stated Constraint

> "Battery packs cost $600/kWh. They will always be expensive. EVs cannot scale because of battery cost."

(Industry consensus, ~2008.)

### Atoms

| Component | Source price | Required? |
|-----------|--------------|-----------|
| Cobalt | LME spot | yes |
| Nickel | LME spot | yes |
| Aluminum | LME spot | yes |
| Carbon | commodity | yes |
| Polymers | commodity | yes |
| Steel can | commodity | yes |

Sum at LME spot prices (Musk's quoted figure): **~$80/kWh**.

### Floor

**~$80/kWh** for raw materials. Manufacturing + cell design + scale on top.

### Current Reality (then)

**$600/kWh** — 7.5× the floor.

### Gap Decomposition

1. Sub-scale cell production (laptop-cell economics, not vehicle-scale).
2. Vendor margin chains.
3. Cell design optimized for consumer electronics, not automotive duty cycles.

### Reconstruction

Build cells at vehicle scale, integrate cell + pack + vehicle, remove vendor chain → Gigafactory.

### Outcome

Pack cost trended toward $100/kWh by ~2023. The "physics floor" was the right anchor.

---

## 2. SpaceX Reusability (Framework 1 → Framework 2)

### Framework 1 — Stated Constraint

> "Rockets are expendable. Launch costs are dominated by hardware. Nothing to be done."

### Atoms

| Component | Cost share |
|-----------|------------|
| Aluminum, copper, carbon fiber, propellant | ~2% of launch price |
| Manufacturing labor + facilities | ~30-40% of hardware cost |
| Hardware (one-shot use) | dominant |

### Floor

If hardware is reused N times: marginal cost approaches **fuel + refurb / N**, not full hardware.

### Gap

The entire price of the rocket, divided by 1 (uses) instead of N. Reasoning by analogy: "rockets are expendable, like all rockets before them."

### Reconstruction

Land + reuse the first stage → marginal cost trends toward fuel + refurbishment.

### Framework 2 — On the Landing Process

| Step | Application |
|------|-------------|
| 1. Requirements less dumb | Do we *need* legs, fins, throttleable engines? Trace each to physics. (Yes — physics-required.) |
| 2. Delete | Eliminate barge if RTLS is feasible for the trajectory. Eliminate auxiliary systems. |
| 3. Simplify | Single engine for landing burn (Merlin-1D throttle range). |
| 4. Accelerate | Refurb cycle time: from months to days to "fly within 24 hours." |
| 5. Automate | Autonomous landing — only after the trajectory was proven stable. |

### Outcome

Falcon 9 first-stage cost amortized over 10+ flights. Launch price dropped ~10×.

---

## 3. Tesla Manufacturing Line (Framework 2)

### Context

Model 3 production hell, 2018. Line was over-automated and stalling.

### What Happened

Musk's diagnosis publicly: he had skipped to step 5 (automate) before doing 1-3.

| Step | What had gone wrong |
|------|---------------------|
| 1 | Requirements inherited from premium-segment Model S — many didn't apply to Model 3 |
| 2 | Parts that could have been deleted were instead being assembled by robots |
| 3 | No simplification pass before the line was built |
| 4 | Cycle time targets were set against the un-simplified design |
| 5 | Automation was scaling the dumb requirements (the failure mode) |

### Recovery

Run the algorithm in order. Public quote: "Excessive automation at Tesla was a mistake. To be precise, my mistake. Humans are underrated."

### Lesson

Step 5 last. Always.

---

## 4. Software Example: Microservice Migration (Framework 2)

### Stated Goal

"Migrate the monolith to microservices because that's how modern systems scale."

### Framework 1 First (Catch the Analogy)

| Phrase | Analog |
|--------|--------|
| "Modern systems scale this way" | Industry analog. What does the *physics of your traffic* require? |
| "Microservices are best practice" | Best for what problem? Yours? |

If actual traffic is 100 RPS and the team is 5 engineers, the floor doesn't require microservices. The analog does.

### Framework 2 If You Decide to Restructure

| Step | Application |
|------|-------------|
| 1. Requirements | Which services *must* be separate (compliance? blast-radius? team-ownership?). Delete the rest. |
| 2. Delete | Half the services proposed in the migration plan. The ones with no independent owner. |
| 3. Simplify | Merge services that share data. One DB, not seven. |
| 4. Accelerate | Build pipelines, deploy times — only after the architecture is settled. |
| 5. Automate | Service templates, scaffolding — only once the boundaries are stable. |

### Lesson

Most "microservices migrations" automate (step 5) a poorly-decomposed system (steps 1-3 skipped). They scale the wrong boundaries.

---

## 5. Personal: "Should I Hire?" (Framework 2)

### Context

"We need to hire someone to handle X."

### Framework 2

| Step | Question | Outcome |
|------|----------|---------|
| 1. Requirements | What does X actually require? Trace. | Often: 30% is unnecessary, inherited from previous role spec. |
| 2. Delete | Can X be deleted entirely? | Sometimes: yes, the activity exists from inertia. |
| 3. Simplify | What survives — is it the simplest form? | Often: scope shrinks 50%. |
| 4. Accelerate | Existing team can do simplified X faster. | Sometimes: yes. |
| 5. Automate | Can it be automated / scripted / outsourced? | Often: yes for the routine 80%. |

If steps 1-5 leave no need, the hire is avoided. If they leave a real need, the role is *much smaller and more focused* than the original.

---

## How to Calibrate Your Own Cases

For any new problem:

1. State the inherited belief in one sentence.
2. List the atoms.
3. Compute the floor.
4. If the gap is >2×, run the algorithm on the path from current to floor.
5. If the gap is <2×, the analog is probably close to the floor — accept it and move on.

The skill is not to apply both frameworks to everything. It is to **detect when a constraint is inherited** and **only then** spend the effort.
