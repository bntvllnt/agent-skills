# Branch Workflow

Goal: branch-first development; keep base branch clean.

Requires confirmation for branch creation/deletion/switching if it changes state.

## Conventions

- Names: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`
- Base branch: `main` or `master` (detect from repo)

## Flow

1. Update base

```bash
git fetch --all --prune
git switch <base>
git pull --ff-only
```

2. Create a feature branch

```bash
git switch -c <type>/<topic>
```

3. Verify

```bash
git status
git branch --show-current
```
