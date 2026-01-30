# PR Dashboard

Overview of all open PRs with status classification and next actions.

## Trigger

`pr dashboard`, `pr overview`, `open prs`, `my prs`, `pr status`

## Workflow

### 1. Fetch Open PRs

```bash
# Default: current user's PRs
gh pr list --state open --author "@me" \
  --json number,title,state,isDraft,author,labels,reviewRequests,reviewDecision,statusCheckRollup,updatedAt,comments,url

# All authors (user says "all prs" or "team prs"):
gh pr list --state open \
  --json number,title,state,isDraft,author,labels,reviewRequests,reviewDecision,statusCheckRollup,updatedAt,comments,url
```

### 2. Classify Each PR

Priority order (show highest priority classification per PR):

| Status | Condition | Priority |
|--------|-----------|----------|
| Ready | `reviewDecision=APPROVED` + all checks pass | 1 |
| CI Fail | Any check failed | 2 |
| Changes | `reviewDecision=CHANGES_REQUESTED` | 3 |
| Review | No reviews yet, not draft | 4 |
| Draft | `isDraft=true` | 5 |
| Stale | No activity >7 days (any state) | 6 |

### 3. Output — Summary + Table

```
┌────────────────────────────────────────────────────┐
│                  PR DASHBOARD                       │
├────────────────────────────────────────────────────┤
│  Repo:   owner/repo                                │
│  Total:  5 open (1 ready, 1 failing, 1 review,    │
│          1 draft, 1 stale)                          │
└────────────────────────────────────────────────────┘

 PR     Title                   Status    CI     Age  Action
─────  ──────────────────────  ────────  ─────  ───  ─────────────────────
 #27    Add caching             Ready     PASS   1d   Merge now
 #38    Fix rate limiter        Approved  FAIL   5d   Fix CI then merge
 #29    Refactor auth           Changes   PASS   3d   Address feedback
 #42    Add auth middleware     Review    PASS   2d   Request reviewer
 #35    Update docs             Draft     —      8d   Stale — finish or close

Links:
  #27  <url from gh pr list>
  #38  <url from gh pr list>
  #29  <url from gh pr list>
  #42  <url from gh pr list>
  #35  <url from gh pr list>
```

Table sorted by priority (most actionable at top).

### 4. Per-PR Detail

For PRs with CI failures, fetch check details to get clickable failure links:

```bash
gh pr checks <number> --json name,state,link,bucket
```

Show for each PR that needs action:

```
#42 — Add auth middleware
  URL:      <url from gh pr list>
  Author:   @me
  Labels:   enhancement, backend
  Reviews:  0/1 required
  CI:       3/3 passed
  Updated:  2 days ago
  Action:   Request review from @teammate

#38 — Fix rate limiter
  URL:      <url from gh pr list>
  Author:   @me
  Labels:   bug
  Reviews:  1/1 approved
  CI:       2/4 failed
  Failed:   test-e2e  <link from gh pr checks>
            lint      <link from gh pr checks>
  Updated:  5 days ago
  Action:   Fix CI, then merge
```

### 5. Action Map

| Status | Action | Offer |
|--------|--------|-------|
| Ready | Merge now | `gh pr merge <number>` |
| CI Fail | Fix CI | Run CI monitor (`references/ci-monitor.md`) |
| Changes | Address feedback | Show review comments |
| Review | Request reviewer | `gh pr edit --add-reviewer <user>` |
| Draft | Finish or mark ready | `gh pr ready <number>` |
| Stale | Update or close | `gh pr close <number>` |

## URL Rules

All URLs MUST be real values from `gh` JSON output. Never fabricate or construct URLs.

| Source command | URL field |
|----------------|-----------|
| `gh pr list --json url` | `url` — points to the PR page |
| `gh pr checks --json link` | `link` — points to the check run |

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--author` | `@me` | Filter by author. `""` for all |
| `--include-drafts` | yes | Include draft PRs |

## Read-Only (No Confirmation)

```bash
gh pr list --state open --json ...
gh pr checks <number> --json ...
gh pr view <number> --json ...
```

## Write (Confirm First)

```bash
gh pr merge <number>
gh pr close <number>
gh pr ready <number>
gh pr edit <number> --add-reviewer <user>
```
