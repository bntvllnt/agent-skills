# PR Review Workflow

Goal: see PR feedback, apply fixes on the same branch, keep commits intentional.

## Flow

1. Sync

```bash
git fetch origin
```

2. Review PR

```bash
gh pr view --comments
gh pr checks
```

3. Fix

- Make code changes
- Use commit workflow for each coherent fix
- Push updates

```bash
git push
```

## Threads

If you need to resolve threads / request reviews, use `gh` subcommands when possible.
