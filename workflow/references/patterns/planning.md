# Planning Patterns

## Working Backwards

Start from the end state, work backward to tasks. (Amazon PR/FAQ method.)

**When:** Unclear requirements, stakeholder alignment needed, outcome-driven features.

```
1. Write the announcement: "We shipped {feature}. It does {X}."
2. Define "True When": List 3-5 testable statements that prove it works
3. Gap analysis: What exists today vs what's needed?
4. Work backward: From gaps → tasks → dependencies → order
5. FAQ: Answer likely questions (technical, user, business)
```

**Template:**
```markdown
## Announcement
We shipped {feature}. Users can now {capability}.

## True When
- [ ] User can {action} and see {result}
- [ ] System handles {edge case} gracefully
- [ ] Performance: {metric} under {threshold}

## Gaps (current → needed)
- {what exists} → {what's needed} → {task}

## FAQ
Q: Why not {alternative}?
A: {reason}
```

---

## Constraint Mapping

Identify fixed vs flexible constraints before planning.

**When:** Hard deadlines, resource limits, regulatory requirements, unclear boundaries.

```
1. List ALL constraints (technical, time, budget, legal, people)
2. Classify each: FIXED (can't change) vs FLEXIBLE (can negotiate)
3. Challenge "fixed" constraints: Is this truly immovable?
4. Build plan around fixed constraints, optimize flexible ones
```

**Iron triangle:** Scope, Time, Quality — pick 2, the third adjusts.

**Common false constraints:**
- "We need all features for launch" → Do we? MVP?
- "It has to use {technology}" → Why? What problem does it solve?
- "We need it by Friday" → What happens if Monday? What's the real deadline?

**Negotiability matrix:**
```
              Can't Change    Can Negotiate
High Impact   [FIXED]         [OPTIMIZE]
Low Impact    [ACCEPT]        [IGNORE]
```

---

## Risk-First Planning

Order work by risk, not by ease or dependency.

**When:** High-uncertainty projects, new technology, tight deadlines.

```
1. List risks (technical, schedule, scope, external)
2. Score each: Impact (1-5) × Likelihood (1-5)
3. Order work: highest risk score first
4. Define kill criteria: "If {condition}, abandon this approach"
5. Spike pattern: time-boxed exploration before committing
```

**Risk categories:**
- Technical: "Can we even build this?"
- Integration: "Will it work with {system}?"
- Performance: "Will it be fast enough?"
- Scope: "Is the scope realistic?"
- External: "Will the API/service/team deliver?"

**Spike pattern:**
```
Spike: {question to answer}
Time box: {hours}
Success: {what we'd learn/prove}
Kill criteria: {when to stop and reconsider}
Output: Go/no-go decision + evidence
```

**Key rule:** Attack the scariest unknown first. If it fails, fail early.
