# Worktree Summary (Proactive Analysis)

Goal: show all worktrees with branch, PR status, change analysis, and safe-to-delete verdicts.

Read-only — no confirmation needed. Uses `WORKTREES_DIR` from `git/SKILL.md`.

## Triggers

`worktree summary`, `worktree status`, `worktree overview`, `show worktrees`

## Step 1: Inventory

```bash
git worktree list --porcelain
git branch --show-current
```

Parse each worktree entry: path, branch, HEAD commit.

Detect base branch: `main` or `master` (whichever exists).

If no worktrees besides main repo: output "No worktrees. Main repo only." and stop.

## Step 2: Per-Worktree Analysis

For each worktree (cap at 10, show "N more..." if exceeded):

### 2a. Branch + Commit Status

```bash
# From inside worktree path
git -C <worktree-path> status --porcelain
git -C <worktree-path> log --oneline <base>..HEAD
git -C <worktree-path> log --oneline HEAD..<base>
```

Derive:
- **Committed ahead**: N commits ahead of base (unpushed work)
- **Committed behind**: N commits behind base
- **Uncommitted**: count of modified/untracked files
- **Clean**: no uncommitted changes (working tree matches HEAD)
- **Fully merged**: branch HEAD is reachable from base (0 unique commits ahead)

### 2b. PR Lookup

```bash
gh pr list --head <branch-name> --state all --json number,state,title,url --limit 1
```

If gh unavailable: mark PR as "unknown (no gh)".

Derive:
- **PR merged**: branch work is in base
- **PR open**: work in progress, not merged
- **No PR**: no PR created for this branch

### 2c. Change Analysis (uncommitted + unpushed vs base)

**Only runs when worktree has uncommitted or unpushed changes.**

For each changed file (cap at 20 files, summarize rest):

```bash
# Get list of changed files (uncommitted)
git -C <worktree-path> diff --name-only
git -C <worktree-path> diff --cached --name-only
git -C <worktree-path> ls-files --others --exclude-standard

# Get list of changed files (unpushed commits)
git -C <worktree-path> diff --name-only <base>..HEAD
```

For each changed file, classify:

#### COVERED (safe to discard)

The same change exists in base branch. Check:

```bash
# Does base branch have equivalent changes to this file?
git log <base> --oneline -5 -- <file>
# Compare: does current base version already include the worktree's changes?
git -C <worktree-path> diff <base> HEAD -- <file>
```

If diff is empty or minimal (cosmetic only — whitespace, imports, formatting): **COVERED**.
If remaining diff is semantic (logic, behavior), classify as **UNIQUE** instead.
Note which commit in base covers it: `"same change in <base>@<short-sha> (<commit-msg>)"`.

#### OBSOLETE (safe to discard)

The changed file/code was removed or rewritten in base:

```bash
# Does the file still exist in base?
git show <base>:<file> 2>/dev/null
```

If file doesn't exist in base: check if it was intentionally deleted (git log).
If the specific code block was rewritten: **OBSOLETE**.
Note: `"file removed in <base>@<short-sha> (<commit-msg>)"` or `"code rewritten in <base>@<short-sha>"`.

#### UNIQUE (will lose work)

No match found in base branch or any open PR. This is original work.

Report: file path, line count of changes, brief description of what changed.

Mark: `"NOT in <base> or any open PR — WILL LOSE WORK if deleted"`.

### 2d. Verdict

| Condition | Verdict |
|-----------|---------|
| PR merged + clean + 0 unique files | **SAFE TO DELETE** |
| PR merged + only COVERED/OBSOLETE uncommitted | **SAFE TO DELETE** |
| Clean + branch merged into base (no PR) | **SAFE TO DELETE** |
| Has UNIQUE uncommitted/unpushed files | **BLOCKED** (will lose work) |
| PR open + clean (all pushed) | **CAUTION** (PR still open) |
| PR open + UNIQUE uncommitted | **BLOCKED** (unpushed unique work) |
| No PR + unpushed commits + no unique uncommitted | **CAUTION** (unpushed commits) |

## Step 3: Output

```
┌─────────────────────────────────────────────────────────────────┐
│                       WORKTREE SUMMARY                          │
├─────────────────────────────────────────────────────────────────┤
│ Main: <main-repo-path> (<base-branch>)                          │
│ Dir:  <WORKTREES_DIR>                                           │
│ Total: N worktrees (N safe, N caution, N blocked)               │
└─────────────────────────────────────────────────────────────────┘

 #  Worktree           Branch              PR         Verdict
─── ─────────────────── ─────────────────── ────────── ──────────────
 1  <path>              <branch>            #N merged  SAFE TO DELETE
 2  <path>              <branch>            #N open    CAUTION
 3  <path>              <branch>            —          BLOCKED
```

### Detailed Analysis (per worktree with changes)

Only shown for CAUTION and BLOCKED worktrees:

```
## N. <path> — <branch> -> <VERDICT>

  PR:          #N <state> | — (none)
  Committed:   N ahead, N behind base
  Uncommitted: N files modified

  ┌─ Change Analysis (vs <base>) ───────────────────────────────┐
  │                                                              │
  │ COVERED  <file>                                              │
  │          <description of what changed>                       │
  │          Same change in <base>@<sha> (<msg>)                 │
  │                                                              │
  │ OBSOLETE <file>                                              │
  │          <description>                                       │
  │          File removed in <base>@<sha> (<msg>)                │
  │                                                              │
  │ UNIQUE   <file>                                              │
  │          N lines changed (<brief description>)               │
  │          NOT in <base> or any open PR                        │
  │          !! WILL LOSE WORK if deleted                        │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  Verdict: N covered, N obsolete, N unique
  Action:  <recommended next step>
```

### Recommendations

```
  Recommendations:
    DELETE  #1 <path> -> `git worktree remove <path>`
    REVIEW  #2 <path> -> commit <unique-files> first
    BLOCKED #3 <path> -> rescue <unique-files> first
```

### Legend (always shown)

```
  Change Classifications:
    COVERED  — same change exists in base branch (safe to discard)
    OBSOLETE — targets code removed/rewritten in base (safe to discard)
    UNIQUE   — not found elsewhere (WILL LOSE WORK)

  Verdicts:
    SAFE TO DELETE — all work merged/covered, no unique changes
    CAUTION        — PR still open or unpushed commits (no data loss)
    BLOCKED        — has unique uncommitted/unpushed work (data loss risk)
```

## Limits

- Max 10 worktrees in summary (show "and N more..." for the rest)
- Max 20 files per worktree in change analysis (show "and N more files..." for the rest)
- If gh CLI unavailable: skip PR lookup, note "PR: unknown (gh unavailable)"
