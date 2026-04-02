# Rules Discovery Protocol

> **Agent:** Load this file at the start of any action that produces or evaluates code: `plan`, `ship`, `fix`, `review`, `spec-review`, `focus`. Read project/user agent config files, extract rules, and enforce throughout the action.

Agent-agnostic. Works with any coding agent ecosystem.

---

## Step 1: Discover Config Files

Read **all** that exist at both levels:

```
Project-level (check all):
  {project}/CLAUDE.md                  (Claude Code)
  {project}/.claude/CLAUDE.md          (Claude Code)
  {project}/.claude/rules/*            (Claude Code sub-rules)
  {project}/AGENTS.md                  (universal — any agent)
  {project}/.cursorrules               (Cursor)
  {project}/.windsurfrules             (Windsurf)
  {project}/.aider.conf.yml            (Aider)
  {project}/.continue/config.json      (Continue)
  {project}/codex.md                   (Codex)
  {project}/.opencode/config           (OpenCode)

User-level (check all):
  ~/.claude/CLAUDE.md                  (Claude Code)
  ~/.claude/rules/*                    (Claude Code sub-rules)
  ~/.cursorrules                       (Cursor)
  ~/.windsurfrules                     (Windsurf)
  ~/.aider.conf.yml                    (Aider)
  ~/.continue/config.json              (Continue)
  ~/.codex/config or ~/codex.md        (Codex)
  ~/.opencode/config                   (OpenCode)
```

No files found at either level → skip rules enforcement for this action.

(Canonical file list shared with `references/memory-update.md` Step 1.)

## Step 2: Extract & Prioritize Rules

1. Extract actionable rules: coding standards, conventions, anti-patterns, quality requirements, forbidden patterns
2. **Precedence: project-level rules override user-level rules.** On conflict, project wins.
3. Merge non-conflicting rules from both levels into a single rules set

## Step 3: Filter for Relevance

Match rules against the action's scope:

| Signal | Filter |
|--------|--------|
| Language | Skip Python rules if only TypeScript files involved |
| Category | Skip UI rules if no UI files in scope |
| Path | Skip rules targeting specific paths not in scope |
| Always-applicable | Naming, style, security, git rules apply to everything |

No relevant rules after filtering → skip rules enforcement.

## Step 4: Classify Severity

| Rule Signal | Severity |
|-------------|----------|
| MUST, ALWAYS, NEVER, REQUIRED, BLOCKING | FAIL |
| SHOULD, PREFER, RECOMMEND, AVOID | WARN (high) |
| No explicit strength signal | WARN (medium) |
| Production mode (review/focus only) | Ambiguous rules → FAIL |

## How Actions Use This

| Action | When to Run | How Rules Apply |
|--------|-------------|-----------------|
| **plan** | After loading spec-template | Plans must respect project conventions. Flag rule conflicts in spec. |
| **ship** | Before first implementation task | Code written must follow rules. Violations caught in quick pass. |
| **fix** | Before investigating bug | Fix must follow rules. Regression test must follow testing rules. |
| **review** | Before perspective dispatch (MANDATORY) | Rules become the 10th perspective checklist. Findings use `[Rules]` tag. |
| **spec-review** | Before evaluating spec | Spec must not propose patterns that violate rules. |
| **focus** | Before codebase scan | Scan checks existing code against rules. |

### Actions That Skip

| Action | Why |
|--------|-----|
| **spike** | Exploratory — velocity over compliance |
| **done** | Retro/validation — no code written |
| **drop** | Cleanup — no code written |

## Output Format (When Reporting Violations)

```
{file}:{line} — {FAIL|WARN} [Rules] {violation description}
  Fix: {concrete action}
  Rule: {source file} § {section} — "{rule text}"
```

Example:
```
src/api/users.ts:5 — FAIL [Rules] Missing explicit return type on exported function
  Fix: Add return type annotation to `getUsers()`
  Rule: AGENTS.md § TypeScript — "Explicit return types on public APIs"
```
