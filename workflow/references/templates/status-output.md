# Status Output Template

Edit this file to customize what the agent returns for `workflow` / status check. Decision logic: inline in [SKILL.md](../../SKILL.md#status-action).

---

```markdown
## Workflow Status

**State:** {IDLE / SPEC_READY / IN_PROGRESS / READY_FOR_DONE / STUCK}

{If active spec:}
**Spec:** `specs/active/{filename}`
**Progress:** {N}/{total} scope items ({percent}%)
**Current:** {what's in progress or next up}

{If uncommitted changes:}
**Uncommitted:** {N} files changed

{If tasks exist:}
**Tasks:** {N} pending | {N} in_progress | {N} completed

### Suggested Next Action
{suggestion based on state — e.g. "Run `ship` to continue" or "Run `done` to validate and close"}
```
