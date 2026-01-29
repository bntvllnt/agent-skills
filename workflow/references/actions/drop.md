# Drop Action

> **Agent:** Load this file when `drop` triggers.

Abandon feature, preserve learnings. Nothing is wasted.

---

## Step 1: Confirm

Ask before dropping:
- Why dropping? (Categories: too complex, wrong approach, no longer needed, blocked, time constraint)
- Any reusable pieces? (Code, patterns, research)

## Step 2: Capture Learnings

Write drop retro to spec Notes:

```markdown
### Drop Retro ({DATE})
**Reason:** {category} — {details}
**Time spent:** {hours}
**Reusable pieces:**
- {code/pattern/insight that can be reused}
**What we learned:**
- {key insight from the attempt}
**If revisited:**
- {what to do differently next time}
```

## Step 3: Record Timestamp

Add drop entry to spec Timeline:
```markdown
| dropped | {ISO_TIMESTAMP} | {time_spent} | {reason} |
```

## Step 4: Archive Spec

```
mkdir -p specs/dropped
mv specs/active/{spec-file}.md specs/dropped/
Update spec: status → dropped, dropped → {YYYY-MM-DD}
```

## Step 5: Log to History

Append to `specs/history.log`:
```
{DATE} | dropped | {slug} | {estimate}h→{actual}h | {reason} | {key_learning}
```

## Step 6: Output

Follow the output template in `references/templates/drop-output.md`.
