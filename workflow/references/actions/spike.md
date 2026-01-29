# Spike Action

> **Agent:** Load this file when `spike` triggers.

Time-boxed exploration. Answers a question, produces go/no-go. NOT a shippable feature.

---

## When to Spike

- Unknown technology: "Can we use X for this?"
- Feasibility: "Is this approach even possible?"
- Performance: "Will this be fast enough?"
- Integration: "Does X work with Y?"
- Architecture: "Which pattern fits best?"

## Flow

```
spike {question}
     │
     ▼
┌──────────────────────────┐
│ 1. DEFINE                │
│    Question: {what}      │
│    Time box: {hours}     │
│    Success: {go criteria} │
│    Kill: {stop criteria}  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 2. EXPLORE               │
│    Research / prototype   │
│    Track findings         │
│    Check kill criteria    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 3. DECIDE                │
│    GO / NO-GO / UNCLEAR  │
│    Evidence summary       │
│    Next step              │
└──────────────────────────┘
```

## Task Template

```
[ ] Define question and success/kill criteria
[ ] Set time box (default 1h, max 4h)
[ ] Explore: research and prototype
[ ] Document findings
[ ] Decision: GO / NO-GO / NEEDS_MORE_INFO
[ ] Clean up: delete prototype code
[ ] Log to history
```

## Output

Follow the output template in `references/templates/spike-output.md`.

## Rules

- Spike code is THROWAWAY. Delete before proceeding.
- Never ship spike code directly. If GO, start fresh with `plan`.
- Time box is hard. If kill criteria hit, stop immediately.
- Log spike to `specs/history.log`:
  ```
  {DATE} | spike | {slug} | {time}h | {GO/NO-GO} | {key finding}
  ```
