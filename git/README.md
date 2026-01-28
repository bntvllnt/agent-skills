# Git

Unified git workflow skill: branch-first development, security-first commits, worktree workflows, and PR creation/review via `gh`.

## Quick Start

- Home/router: `git/SKILL.md`

Common workflows:

- Read-only inspection: `git/references/read-only.md`
- Commit flow + best practices: `git/references/commit-workflow.md`
- Branch flow: `git/references/branch-workflow.md`
- Worktrees (configurable root): `git/references/worktree-workflow.md`
- Worktree maintenance (cleanup + consolidation): `git/references/worktree-maintenance.md`
- PR create: `git/references/pr-workflow.md`
- PR review/fix: `git/references/pr-review-workflow.md`
- Advanced/recovery: `git/references/advanced-workflows.md`

## Worktree Path Config

Edit `WORKTREES_DIR` in `git/SKILL.md`.

## Install

```bash
npx skills add bntvllnt/agent-skills --skill git
```

Manual install (download this folder only):

- Copy the `git/` folder into your agent's skills directory.
- Ensure the folder name is `git` and includes `SKILL.md`.

## Requirements

- `git`
- `gh` is recommended for PR workflows (optional)
