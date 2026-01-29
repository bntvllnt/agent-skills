# Decomposition Patterns

## First Principles

Break to fundamentals. Challenge assumptions. Rebuild from ground truth.

**When:** Novel problems, inherited constraints, "we've always done it this way."

```
1. IDENTIFY the problem clearly (one sentence)
2. LIST all assumptions
3. CHALLENGE each: Is this a law of physics or a convention?
   - Law of physics: keep (e.g., "network calls have latency")
   - Convention: question (e.g., "we need a separate auth service")
4. REBUILD from only the validated fundamentals
```

**Example:**
```
Problem: "Auth takes 500ms on every request"
Assumptions:
  ✓ Auth is required (law — security requirement)
  ✗ Auth must hit the database (convention — can use JWT/cache)
  ✗ Auth must happen per-request (convention — can use sessions)
  ✓ Token must be validated (law — security)
Rebuild: Validate JWT locally (no DB call), cache sessions → 5ms
```

**Key rule:** Most constraints are inherited conventions, not physical laws. Test them.

---

## Inversion

"What would guarantee failure?" Prevent those things.

**When:** Risk assessment, pre-mortems, defensive design, quality checklists.

```
1. Define success: {what you want to achieve}
2. Invert: "How do I guarantee this FAILS?"
   List 5-10 failure modes
3. For each failure mode:
   - How likely is it? (HIGH/MEDIUM/LOW)
   - How would we detect it?
   - How do we prevent it?
4. Build prevention into the plan
```

**Example:**
```
Success: "Reliable payment processing"
Guaranteed failure modes:
  1. No idempotency → duplicate charges → Add idempotency keys
  2. No timeout → hung requests → Add 30s timeout + retry
  3. No validation → bad amounts → Validate at boundary
  4. No logging → can't debug → Structured logging on all paths
  5. No rollback → partial state → Transaction wrapper
```

**Use for quality checklists:** Invert each scope item → "what breaks this?" → checklist item.

---

## MECE (Mutually Exclusive, Collectively Exhaustive)

Decompose without gaps or overlaps.

**When:** Problem decomposition, scope breakdown, categorization, test coverage.

```
MECE test:
  ME (Mutually Exclusive): No item belongs in two categories
  CE (Collectively Exhaustive): Every case is covered by some category
```

**How to MECE-decompose:**

```
1. Pick a dimension to split on (user type, data flow, lifecycle stage)
2. List categories along that dimension
3. ME test: Can any item fit in 2+ categories? → refine boundaries
4. CE test: Can you think of something not covered? → add category
```

**Common MECE frameworks:**

| Framework | Split By | Example |
|-----------|----------|---------|
| User lifecycle | Stage | Acquire → Activate → Retain → Revenue → Refer |
| Data flow | Direction | Input → Process → Output → Store |
| Error handling | Severity | Fatal → Recoverable → Warning → Info |
| Feature scope | Layer | Data → Logic → API → UI → Test |
| Time | Phase | Before → During → After |

**Anti-patterns:**
- Overlapping categories (item fits in 2 buckets)
- Missing the "other" bucket (edge cases uncovered)
- Too many categories (>7 = too granular, re-group)
- Too few categories (2-3 = probably missing nuance)

**Application to scope breakdown:**
```
Feature: User authentication
MECE by flow:
  1. Registration (new user → account created)
  2. Login (credentials → session)
  3. Session management (active → expired → refresh)
  4. Logout (session → destroyed)
  5. Recovery (forgot password → reset → login)

ME check: Each flow is distinct, no overlap ✓
CE check: All auth states covered ✓
```
