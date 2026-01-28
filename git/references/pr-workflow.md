# PR Workflow (gh)

Goal: push branches and open PRs with a clear title/body.

Requires confirmation before push.

## Flow

1. Confirm state

```bash
git status
git branch --show-current
```

2. Push branch

```bash
git push -u origin HEAD
```

3. Create PR

```bash
gh pr create --title "<title>" --body "<body>" --base <base>
```

If `gh` is not installed, push the branch and open a PR in your Git hosting UI.

4. Check CI

```bash
gh pr checks
```
