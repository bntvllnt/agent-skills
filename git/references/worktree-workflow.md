# Worktree Workflow

Goal: parallel work without stashing.

Important fact: `.git/worktrees/` is git's internal metadata directory.
- You do NOT put a worktree working directory inside `.git/worktrees/`.
- Git automatically creates/updates `.git/worktrees/<name>/` metadata when you add a worktree.

Recommended working directory target (repo-local): `./.worktrees/<topic>`.

Config: use `WORKTREES_DIR` from `git/SKILL.md`.
- Default: `WORKTREES_DIR=./.worktrees`
- Worktree path shape: `$WORKTREES_DIR/<topic>`

Requires confirmation for `git worktree add/remove`.

## Worktree Health Check (Resilience)

Run these first when anything looks off:

```bash
git worktree list
git status
```

If the repo has worktree folders outside `WORKTREES_DIR` (for example `../repo-feature-x/`), do not delete them.
Instead, consolidate into `WORKTREES_DIR` (see below).

## Create worktree

From the main repo worktree:

```bash
mkdir -p <worktrees-dir>
git worktree add -b <type>/<topic> <worktrees-dir>/<topic> <base>
```

If the branch already exists:

```bash
git worktree add <worktrees-dir>/<topic> <type>/<topic>
```

## List worktrees

```bash
git worktree list
```

## Remove worktree

```bash
git worktree remove <worktrees-dir>/<topic>
```

Optionally delete branch (only if merged / no longer needed):

```bash
git branch -d <type>/<topic>
```

## Troubleshooting

- If removal fails due to modifications: commit/stash inside that worktree first.
- If a worktree is missing on disk but still registered: `git worktree prune` (confirm first).

## Consolidate Into `WORKTREES_DIR`

Goal: keep worktree working directories under one root (`WORKTREES_DIR`) while letting git manage internal metadata under `.git/worktrees/`.

### Detect multiple worktree roots

If `git worktree list` shows worktrees under different parent folders, treat that as "multiple roots".

### Preferred: move an existing worktree

When supported, use git's built-in move (keeps registration intact):

```bash
git worktree move <old-path> <worktrees-dir>/<topic>
```

### Fallback: remove + re-add

If move isn't possible (or user wants a clean reattach):

```bash
git worktree remove <old-path>
git worktree add <worktrees-dir>/<topic> <branch>
```

Never remove a worktree that has uncommitted changes.
