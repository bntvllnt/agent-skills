# Pull Requests (gh pr)

List PRs:

```bash
gh pr list
```

View PR:

```bash
gh pr view <number>
gh pr view <number> --comments
gh pr view <number> --web
```

Create PR (always assign; label when possible):

Prefer a two-step flow so PR creation never fails if a label doesn't exist:

```bash
gh pr create --assignee "@me"
gh pr edit --add-label "<label1>,<label2>"
```

If the user explicitly names a different assignee (e.g. `@alice`), use that instead of `@me`:

```bash
gh pr create --assignee "@alice"
```

If the user doesn't specify labels, auto-pick from existing repo labels using PR context (title/body/branch + changed paths).

Heuristics (best-effort; don't block PR creation):

- Prefer labels that match touched areas (e.g. `docs`, `backend`, `frontend`, `ci`, `infra`, `api`) or package/app names.
- If the repo uses standard labels, map PR intent:
  - bugfix -> `bug`
  - docs-only -> `documentation`
  - feature -> `enhancement`
- If it's ambiguous, add fewer labels rather than the wrong ones.

Retrieve existing labels:

```bash
gh label list --limit 200
gh label list --search "docs" --limit 200
gh label list --search "backend" --limit 200
```

If you must create new labels (confirm first), keep it minimal and consistent with the repo's naming style:

```bash
gh label create "<label>" --description "<description>" --color 0E8A16
```

Then apply labels to the PR:

```bash
gh pr edit --add-label "<label1>,<label2>"
```

Checks:

```bash
gh pr checks
```

Review / comment:

```bash
gh pr review <number> --comment --body "<comment>"
```

Merge (confirm first):

```bash
gh pr merge <number>
```

## Auto-Monitor CI After PR Creation

After `gh pr create` succeeds, check if repo has CI workflows:

```bash
gh workflow list
```

If workflows exist, ask the user:

> CI detected. Monitor checks? [Y/n]

If yes, run the CI Monitor workflow (`ci status` for the new PR number).
If no, return control immediately.
