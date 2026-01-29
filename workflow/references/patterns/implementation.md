# Implementation Patterns

## Tracer Bullet

Build minimal end-to-end path first, then expand each layer.

**When:** Greenfield features, unknown integration points, proving architecture.

```
1. Identify the thinnest possible E2E path (DB → API → UI)
2. Build hardcoded/stubbed version that works end-to-end
3. Replace stubs with real implementation, one layer at a time
4. Each step: working software, not just working layer
```

**Template:**
```
Tracer: {feature} — thinnest E2E path
  Layer 1 (data): {hardcoded response}
  Layer 2 (API): {stub endpoint returning hardcoded}
  Layer 3 (UI): {display hardcoded data}
  → Verify E2E works
  → Replace Layer 1 with real DB query
  → Replace Layer 2 with real logic
  → Replace Layer 3 with real components
```

**Key rule:** Every step produces working software. Never build a layer in isolation.

---

## Vertical Slice

Complete one feature fully across all layers before starting the next.

**When:** Multiple features to build, cross-layer dependencies, team handoffs.

```
Feature A: DB schema → API endpoint → UI component → tests → DONE
Feature B: DB schema → API endpoint → UI component → tests → DONE
(NOT: all DB schemas → all APIs → all UIs)
```

**Good slice boundaries:**
- User-visible behavior change
- Independently deployable
- Has its own test cases
- Can be demo'd

**Bad slice boundaries:**
- "All the database work"
- "The API layer"
- "Frontend only" (unless pure UI)

---

## Strangler Fig

Gradually replace legacy system via facade routing.

**When:** Legacy replacement, large migrations, can't rewrite at once.

```
1. Create facade (proxy/router) in front of legacy system
2. Route first feature to new implementation
3. Verify new implementation matches legacy behavior
4. Route more features to new implementation
5. When all features migrated, remove legacy + facade
```

**Routing strategies:**
- Feature flag: toggle per feature
- Percentage: 10% → 50% → 100%
- User segment: internal → beta → all
- Request type: reads first, then writes

**Key rule:** Legacy and new system coexist. Never big-bang cutover.

---

## Inside-Out vs Outside-In

Choose starting point based on where complexity lives.

**Inside-out** (start from core logic, expand to boundaries):
- When: Complex algorithms, data transformations, business rules
- Pro: Core logic validated first
- Con: Integration discovered late

**Outside-in** (start from user interface, work inward):
- When: UI-driven features, clear user flows, API-first design
- Pro: User experience validated first
- Con: Core logic deferred

**Decision framework:**
```
Where is the complexity?
  Core logic/algorithm → Inside-out
  User interaction/flow → Outside-in
  Both equally complex → Meet in the middle
    (define interface between layers, build both toward it)
```
