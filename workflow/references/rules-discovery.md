# Rules Discovery Protocol

> **Agent:** Load this file during `review` before dispatching perspectives. Read project/user agent config files, extract rules, and enforce them one by one against the changed scope.

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

Review reproducibility rule:
- Project-level rule files are the stable, repo-owned baseline.
- User-level rule files are environment-specific overlays and must be reported explicitly when loaded.
- Shared / CI review should default to project-level rules only.
- If a user-level rule source is unavailable in the current reviewer environment, do not pretend it was checked. Report it as unavailable and only claim coverage for the rule sources actually loaded.

(Canonical file list shared with `references/memory-update.md` Step 1.)

## Step 2: Extract & Prioritize Rules

1. Extract actionable rules: coding standards, conventions, anti-patterns, quality requirements, forbidden patterns
2. Normalize them into a numbered checklist with source attribution:
   - `RULE-1 | source | scope | strength | rule text`
   - Example: `RULE-3 | ~/.claude/CLAUDE.md | git | MUST | Use worktrees for parallel feature work`
3. **Precedence: project-level rules override user-level rules.** On conflict, project wins.
4. Merge non-conflicting rules from both levels into a single rules set

## Step 3: Filter for Relevance

Match rules against the action's scope:

| Signal | Filter |
|--------|--------|
| Language | Skip Python rules if only TypeScript files involved |
| Category | Skip UI rules if no UI files in scope |
| Path | Skip rules targeting specific paths not in scope |
| Changed hunk | Skip rules that do not apply to the changed line ranges being reviewed |
| Always-applicable | Naming, style, security, git rules apply to everything |

For `review`, filtering must stay explicit:
- Keep a `relevant_rules[]` list
- For each rule, note which changed files/hunks it applies to
- If applicability is unclear in Production mode, treat as relevant and fail closed

No relevant rules after filtering → skip rules enforcement.

## Step 4: Classify Severity

| Rule Signal | Severity |
|-------------|----------|
| MUST, ALWAYS, NEVER, REQUIRED, BLOCKING | FAIL |
| SHOULD, PREFER, RECOMMEND, AVOID | WARN (high) |
| No explicit strength signal | WARN (medium) |
| Production mode (review/focus only) | Ambiguous rules → FAIL |

For `review`, every relevant rule must end with an explicit verdict for the changed scope:
- `PASS` — checked and respected
- `WARN` — checked and partially respected / non-blocking deviation
- `FAIL` — checked and violated
- `NOT_APPLICABLE` — rule exists but does not apply to the specific changed files/hunks

Missing verdicts are process failures, not silent skips.

## How Review Uses This

| Phase | How Rules Apply |
|------|------------------|
| **Before perspective dispatch** | Discover project-level + user-level config files and extract rules. |
| **Before Rules perspective runs** | Filter rules to the changed files/hunks and assign explicit applicability. |
| **During review** | Check each relevant rule one by one against changed files/hunks. Missing rule verdicts are FAIL [Process]. |
| **In findings** | Rules violations use the `[Rules]` tag plus source-file attribution. |

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
