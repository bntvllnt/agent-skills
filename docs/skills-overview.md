# Skills Overview

Agent Skills is a collection of reusable AI agent capabilities, distributed via [skills.sh](https://skills.sh).

## Available Skills

| Skill | Description |
|-------|-------------|
| [analyze](../analyze/SKILL.md) | Universal multi-perspective analyzer (quick/standard/deep modes) |
| [skill-builder](../skill-builder/SKILL.md) | Create/update/delete skills with validated templates |
| [oss-readiness](../oss-readiness/SKILL.md) | OSS/public release audit, scaffolding, llms docs, CI checks |
| [git](../git/SKILL.md) | Git workflow: branch-first commits, worktrees, PRs |
| [github](../github/SKILL.md) | GitHub CLI operations: repos, issues, PRs, Actions, releases |
| [convex](../convex/SKILL.md) | Convex backend: functions, schemas, auth, scheduling |
| [workflow](../workflow/SKILL.md) | High-velocity solo development: plan, ship, fix, review, done |
| [tmux](../tmux/SKILL.md) | Terminal multiplexer: sessions, windows, panes, layouts |
| [first-principles](../first-principles/SKILL.md) | First-principles thinking + 5-step engineering algorithm |

## How Skills Work

Skills are Markdown files that provide structured instructions to AI agents. Each skill has:

1. **SKILL.md** — Main entry point with YAML frontmatter and action router
2. **references/** — On-demand docs loaded by the action router when needed
3. **README.md** — Human-readable documentation

## Installation

```bash
# Install all skills
npx skills add bntvllnt/agent-skills

# Install a specific skill
npx skills add bntvllnt/agent-skills --skill workflow
npx skills add bntvllnt/agent-skills --skill oss-readiness

# Install globally
npx skills add bntvllnt/agent-skills --skill workflow -g

# Install for a specific agent
npx skills add bntvllnt/agent-skills --skill workflow --agent claude-code
```

## Compatibility

Skills are agent-agnostic and work with any agent that supports SKILL.md loading:
- Claude Code
- OpenCode
- Windsurf
- Cursor
- Codex
- Aider
