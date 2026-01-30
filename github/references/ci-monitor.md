# CI Monitor

Monitor CI check status for a PR or branch with live polling.

## Trigger

`ci`, `monitor ci`, `check ci`, `ci status`, `watch ci`

## Workflow

### 1. Resolve Target

Determine what to monitor. Try in order:

1. User provided PR number → use it
2. User provided branch → find latest run for that branch
3. Neither → auto-detect current branch, then find its PR or latest run

```bash
# Current branch:
git branch --show-current

# Find PR for current branch:
gh pr view --json number,headRefName --jq '.number'

# If PR exists:
gh pr checks <number> --json name,bucket,startedAt,completedAt,link,workflow

# If no PR (branch-only):
gh run list --branch <branch> --limit 5 --json status,conclusion,name,databaseId,url
```

### 2. Poll Loop

Poll every 30s. Max duration: 10 minutes. Each iteration: fetch status, display table.

```
┌─────────────────────────────────────────────────────┐
│                CI STATUS — PR #42                    │
├─────────────────────────────────────────────────────┤
│  Branch:  feature/auth-middleware                    │
│  PR:      https://github.com/owner/repo/pull/42     │
│  Poll:    30s interval | 1m30s elapsed | 10m max    │
└─────────────────────────────────────────────────────┘

 Check            Status        Duration
───────────────  ────────────  ────────
 lint             PASS          12s
 typecheck        PASS          28s
 test-unit        IN_PROGRESS   1m02s
 test-e2e         QUEUED        —

Links:
  lint:       <link field from gh pr checks>
  typecheck:  <link field from gh pr checks>
  test-unit:  <link field from gh pr checks>
  test-e2e:   <link field from gh pr checks>
```

Status: `QUEUED` | `IN_PROGRESS` | `PASS` | `FAIL` | `SKIPPED`

## URL Rules

All URLs MUST be real values from `gh` JSON output. Never fabricate or construct URLs.

| Source command | URL field |
|----------------|-----------|
| `gh pr checks --json link` | `link` — points to the check run |
| `gh run list --json url` | `url` — points to the workflow run |
| `gh pr list --json url` | `url` — points to the PR page |

### 3. Exit Conditions

| Condition | Action |
|-----------|--------|
| All checks complete (pass/fail/skipped) | Show final summary |
| Timeout reached | Report PENDING |
| User interrupt | Stop immediately |

### 4. Final Summary

On success:

```
CI RESULT: PASS — 4/4 checks green (2m14s)
  PR: https://github.com/owner/repo/pull/42
```

On failure — list each failed check with its `link` value, then auto-fetch logs:

```
CI RESULT: FAIL — 1/4 checks failed

  FAILED:
   test-e2e  <link value from gh pr checks>

  Logs (last 50 lines of failed output):
  ─────────────────────────────────────
  [truncated output from gh run view <run-id> --log-failed]
  ─────────────────────────────────────
```

Auto-fetch failed logs via `gh run view <run-id> --log-failed`.

### 5. Retry (Confirm First)

Only if user asks. This is a write operation — confirm before running.

```bash
gh run rerun <run-id>
```

Then resume polling loop.

## Defaults

| Parameter | Default | Range |
|-----------|---------|-------|
| Poll interval | 30s | 10s–120s |
| Max duration | 10min | 1min–30min |
| Failed log lines | 50 | 10–200 |

## Read-Only (No Confirmation)

```bash
gh pr checks <number> --json ...
gh run list --branch <branch> --json ...
gh run view <run-id>
gh run view <run-id> --log-failed
```

## Write (Confirm First)

```bash
gh run rerun <run-id>
gh run cancel <run-id>
```
