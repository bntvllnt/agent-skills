# Advanced / Recovery Workflows

These are easy to misuse; confirm intent and show consequences before running.

## Undo staging (safe)

```bash
git restore --staged <path>
```

## Revert a commit (safe history)

```bash
git revert <sha>
```

## Reset (local history rewrite; dangerous)

Only when commits are not pushed and user explicitly wants it.

```bash
git reset --soft <sha>
```

## Rebase (history rewrite)

Only when branch state is understood and user explicitly requests.

## Worktree maintenance

Prune stale metadata (confirm first):

```bash
git worktree prune
```
