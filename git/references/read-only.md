# Read-Only Inspection

These are safe to run without confirmation.

```bash
git status
git diff
git diff --cached
git log --oneline -n 20
git show
git tag -l
git describe --tags --always
git branch --show-current
git remote -v
git fetch --all --prune
git worktree list
```

If you need to understand "what changed" quickly:

```bash
git status
git diff
git diff --cached
git log --oneline -n 10
```
