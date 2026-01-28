# Worktree Maintenance (Auto-Clean + Consolidate)

This workflow makes worktrees resilient:
- auto-clean stale metadata
- detect multiple worktree root folders
- propose consolidation into `WORKTREES_DIR` (from `git/SKILL.md`)

Requires confirmation before any state-changing command.

## Step 1: Inventory

```bash
git worktree list
git branch --show-current
git status
```

## Step 2: Detect Problems

Look for:

- Worktree paths spread across multiple root folders (example: both `./.worktrees/` and `../repo-foo/`).
- Registered worktree paths that no longer exist on disk.
- Orphan directories that look like old worktrees but are not registered.

## Step 3: Safe Auto-Clean Plan

### A) Prune stale metadata (registered but missing)

Propose (confirm first):

```bash
git worktree prune
```

Then re-run:

```bash
git worktree list
```

### B) Consolidate multiple roots into `WORKTREES_DIR`

Rule: do not delete anything by default.

For each worktree whose working directory is outside `WORKTREES_DIR`, propose one of:

1) Move (preferred):

```bash
git worktree move <old-path> <worktrees-dir>/<topic>
```

2) Remove + re-add (fallback):

```bash
git worktree remove <old-path>
git worktree add <worktrees-dir>/<topic> <branch>
```

Block consolidation if the worktree has uncommitted changes.

### C) Orphan directories (not registered)

If a directory looks like an old worktree but is not in `git worktree list`, propose:

- verify what's inside (read-only)
- either delete it (confirm) or move it to a quarantine folder

Never delete directories automatically.
