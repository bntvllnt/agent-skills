# Session Management

> **Agent:** Load this file when `ship` references session/resume/stuck logic. Also loaded by `done` for context reload.

Track progress, detect stuck states, resume across sessions.

## Progress Tracking

Update spec after each iteration with a progress summary:

```markdown
## Progress

| # | Scope Item | Status | Iteration |
|---|-----------|--------|-----------|
| 1 | {item} | [x] Complete | 2 |
| 2 | {item} | [~] In progress | 3 |
| 3 | {item} | [ ] Pending | - |
| 4 | {item} | [!] Blocked | 3 |

**Iteration:** 3/8 | **Progress:** 1/4 (25%) | **Quality:** lint OK, types OK
```

Status markers:
- `[ ]` Pending
- `[~]` In progress
- `[x]` Complete
- `[!]` Blocked (with reason)

## State Detection (On Resume)

When `ship` is invoked, detect current state:

```
1. Active spec exists in specs/active/?
   NO → FRESH (new work)
   YES → continue

2. Progress section has completed items?
   NO → FRESH (spec created but no work done)
   YES → continue

3. Check iteration count and progress ratio
   iteration >= stuck_threshold AND progress < 50%?
   YES → STUCK
   NO → continue

4. All scope items [x]?
   YES → READY_FOR_DONE
   NO → RESUMING
```

| State | Action |
|-------|--------|
| FRESH | Start from beginning |
| RESUMING | Resume from last incomplete scope item |
| STUCK | Present escalation options to user |
| READY_FOR_DONE | Suggest `done` |

## Resume Protocol

When RESUMING:

```
1. Read spec Progress section
2. Find first non-[x] scope item
3. Load context: what was last worked on, any notes
4. Continue from that point
5. Run quick quality pass before continuing implementation
```

## Context Reload Protocol

When starting a new session or after context loss (compaction, session restart), reload context efficiently:

```
Priority order (read these first):

1. SPEC FILE (source of truth)
   Read: specs/active/{slug}.md
   Get: scope, ACs, progress, notes, encountered bugs
   This tells you WHAT to build and WHERE you left off.

2. RECENT CHANGES
   Run: git diff (staged + unstaged)
   Run: git log --oneline -5
   This tells you WHAT was recently changed.

3. PROJECT CONFIG
   Read: skill reference files (quality-gates.md, action files)
   This tells you HOW quality gates and reviews are configured.

4. CHANGED FILES (only the ones in progress)
   Read files listed in Progress as [~] in-progress
   This gives you CODE CONTEXT for the current task.

5. TEST FILES (if mid-implementation)
   Read test files related to changed code
   This tells you what's TESTED and what's not.

DO NOT re-read:
  - Pattern references (load only when stuck)
  - Action references (you know the workflow)
  - All source files (only read what progress says is relevant)
```

### Context Summary Format

When resuming, output a brief context summary before continuing:

```markdown
## Resuming: {spec title}
**Progress:** {N}/{total} scope items complete
**Current:** Working on scope item {N}: {description}
**Last action:** {what was done last}
**Next:** {what to do next}
**Quality status:** lint {ok/fail}, types {ok/fail}
```

## Stuck Detection

**Metrics tracked per iteration:**
- Scope items completed (delta from last iteration)
- Quality gate results (improving or regressing?)
- Review blockers (decreasing or stable?)
- Time in current iteration

**Escalation triggers:**

| Level | Trigger | Action |
|-------|---------|--------|
| Warning | At stuck_threshold, progress < 50% | Log warning, continue |
| Pause | 2 more iterations, no progress | Present options to user |
| Hard stop | At max_iterations | Force exit with summary |

**Stuck recovery options (presented at Pause):**
1. **Continue** — try a different approach to the current blocker
2. **Reduce scope** — cut remaining items, ship what's done
3. **Defer** — save state, come back later (`ship` will resume)
4. **Drop** — abandon entirely (triggers `drop` action)

## Token Budget

Loading the full skill consumes tokens. Be intentional about what you load.

| Tier | Estimated load | What to load |
|------|---------------|--------------|
| trivial | ~1K tokens | SKILL.md only — implement directly |
| micro | ~2K tokens | SKILL.md + inline spec |
| mini | ~8K tokens | SKILL.md + action file + spec-template (mini) |
| standard | ~15K tokens | SKILL.md + action file + spec-template + quality-gates |

**Token-saving strategies:**
- Load action files on-demand (only when action triggers), not upfront
- Load patterns only when stuck — they're reference material, not required reading
- Skip output templates if using default format
- For trivial/micro tiers: SKILL.md alone has enough to execute
- If token-constrained mid-session: summarize spec progress, drop pattern references

**Rule:** Never load all 21 files at once. The routing table in SKILL.md tells you which file to load next.

## Prevention Tips

- Break large scope items into smaller pieces
- Run quality gates frequently (don't accumulate issues)
- Address blockers immediately, don't work around them
- If the same review issue appears 3 times, step back and rethink the approach
