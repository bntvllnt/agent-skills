# Decision Patterns

## Second-Order Thinking

Think 2-3 steps ahead. "And then what?"

**When:** Architecture decisions, technology choices, process changes.

```
Decision: {what you're choosing}

First-order effects (immediate):
  + {benefit}
  - {cost}

Second-order effects (weeks later):
  + {downstream benefit}
  - {downstream cost}

Third-order effects (months later):
  + {compounding benefit}
  - {compounding cost}
```

**Template:**
```markdown
| Order | Positive | Negative |
|-------|----------|----------|
| 1st (now) | {immediate win} | {immediate cost} |
| 2nd (weeks) | {downstream win} | {downstream cost} |
| 3rd (months) | {compounding win} | {compounding cost} |
```

**Common traps:**
- Optimizing for first-order only (short-term thinking)
- Ignoring negative second-order effects (hidden costs)
- Assuming positive effects compound but negative ones don't

---

## Reversibility Test

Classify decisions as one-way or two-way doors.

**When:** Any significant technical decision. Default mental model.

**Type 1 (one-way door):** Irreversible or very costly to reverse.
- Database schema in production with data
- Public API contract with external consumers
- Framework/language choice for large codebase
- Deleting user data

→ **Slow down.** Gather more information. Get review. Prototype first.

**Type 2 (two-way door):** Easily reversible, low cost to change.
- Internal API design (refactorable)
- UI layout (shippable, measurable)
- Library choice for isolated feature
- Feature flag rollout

→ **Decide fast.** Ship, measure, adjust. Don't over-analyze.

**Classification questions:**
1. What does it cost to reverse this? (hours? days? weeks?)
2. Who is affected if we reverse? (just us? users? partners?)
3. Is data involved? (data migrations are expensive)
4. Are external contracts involved? (APIs, integrations)

**Effort matching:**
```
Type 1: hours of analysis → days of implementation
Type 2: minutes of analysis → hours of implementation
```

---

## Opportunity Cost

Every choice excludes alternatives. What are you NOT doing?

**When:** Prioritization, resource allocation, scope decisions.

```
Option A: {what you'd do}
  Value: {expected outcome}
  Cost: {time + resources}
  Value/hour: {value ÷ hours}

Option B: {alternative}
  Value: {expected outcome}
  Cost: {time + resources}
  Value/hour: {value ÷ hours}

Opportunity cost of A = Value of best alternative not chosen
```

**Common traps:**
- **Sunk cost:** "We already spent 3 days on this" → Irrelevant. Only future costs matter.
- **Urgency bias:** "This is urgent!" → Urgent ≠ important. What's the actual deadline?
- **Completion bias:** "We're 80% done" → Is the remaining 20% worth finishing vs switching?
- **Default bias:** "We've always done it this way" → Is there a better way now?

**Quick test:** "If I hadn't started this, would I start it today given what I know now?"
If no → consider dropping (see `actions/drop.md`).
