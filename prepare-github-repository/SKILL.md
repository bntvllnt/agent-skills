---
name: prepare-github-repository
description: |
  Apply a standard GitHub repository configuration in one pass: description + topics, disable
  projects/wiki, squash-only merges, auto-delete branch on merge, main-branch protection with
  required PR + status checks, and scaffold required docs (README.md, CLAUDE.md mirrored to
  AGENTS.md, .claude/rules/*.md).
  Triggers: "prepare github repository", "prepare repo", "prepare repository", "standardize repo",
  "apply repo preferences", "repo standards", "bootstrap repo settings", "repo defaults",
  "harden main branch", "enforce branch protection".
license: MIT
compatibility: |
  Requires GitHub CLI (gh) authenticated with a token that has the `repo` scope (admin on the
  target repo for branch protection). Targets GitHub-hosted repos. Optional: git, jq.
metadata:
  version: "0.1"
---

# Prepare GitHub Repository

Bring a GitHub repo to a known-good baseline in one pass — settings + protection + required docs.
Idempotent: safe to re-run; re-running reconciles drift back to the desired state.

## Boundary vs the `github` skill

- `github` = general, ad-hoc `gh` operations (one issue, one PR, one setting).
- `prepare-github-repository` = apply the **whole standard preference set** at once and verify it.

Route here only when the intent is "make this repo match my standards", not a single `gh` call.

## Desired State (source of truth)

This table is the contract. Every workflow and the verifier check against it.

| # | Setting | Desired value | Mechanism |
|---|---|---|---|
| 1 | Description | set (non-empty) | `gh repo edit --description` |
| 2 | Topics / tags | set (>= 1) | `gh repo edit --add-topic` |
| 3 | Projects | disabled | `gh repo edit --enable-projects=false` |
| 4 | Wiki | disabled | `gh repo edit --enable-wiki=false` |
| 5 | Merge methods | squash only | `--enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false` |
| 6 | Delete branch on merge | enabled | `gh repo edit --delete-branch-on-merge` |
| 7 | Main protection | enabled (Solo profile) | `gh api PUT .../branches/<main>/protection` |
| 8 | PR required | yes, 0 required approvals | protection: `required_pull_request_reviews` |
| 9 | Status checks | required, strict, auto-detected | protection: `required_status_checks` |
| 10 | README.md | present | scaffold if missing |
| 11 | CLAUDE.md | present, references `.claude/rules/*.md` | scaffold from template |
| 12 | AGENTS.md | full content mirror of CLAUDE.md | `cp CLAUDE.md AGENTS.md` + verify |
| 13 | `.claude/rules/*.md` | present (>= 1) | scaffold starter rules |

**Solo protection profile** (the default this skill applies):

```text
required_pull_request_reviews:
  required_approving_review_count: 0     # PR required, you can self-merge
  dismiss_stale_reviews: true
enforce_admins: false                    # you keep a hotfix escape hatch
required_status_checks:
  strict: true                           # branch must be up to date
  contexts: [<auto-detected>]
required_conversation_resolution: true
required_linear_history: true           # compatible with squash-only
allow_force_pushes: false
allow_deletions: false
restrictions: null
```

PR is enforced by presence of `required_pull_request_reviews`: direct pushes to `main` are
rejected even with 0 required approvals.

## Entry Points (router)

| Intent | Example prompt | Route |
|---|---|---|
| Configure existing repo | `prepare owner/repo` | run full sequence on existing repo |
| Configure current repo | `prepare` (inside a git repo) | resolve `origin` -> run full sequence |
| Create + configure | `prepare new my-repo` | `gh repo create` -> run full sequence |
| Settings only | `apply repo settings owner/repo` | [references/repo-settings.md](references/repo-settings.md) |
| Protection only | `harden main owner/repo` | [references/branch-protection.md](references/branch-protection.md) |
| Docs only | `scaffold repo docs` | [references/docs-scaffold.md](references/docs-scaffold.md) |
| Verify / dry-run | `verify repo prep owner/repo` | [references/verify.md](references/verify.md) |

### Full sequence

```text
0. Resolve target (owner/repo, current origin, or create new)
1. Preflight: gh auth status; confirm admin on repo; resolve default branch name
2. Verify (dry-run) -> report current vs desired (references/verify.md)
3. Repo settings   (references/repo-settings.md)   <- one gh repo edit call
4. Branch protection (references/branch-protection.md) <- detect checks, confirm, PUT
5. Docs scaffold    (references/docs-scaffold.md)   <- README, CLAUDE.md, AGENTS.md mirror, rules
6. Verify again -> report final state + any remaining drift
```

## Inputs to gather first

Ask only for what is missing; never invent these.

| Input | Required | Default |
|---|---|---|
| Target repo (`owner/repo`) | yes | current `origin` if inside a git repo |
| Description (#1) | yes | none — ask the user, do not guess |
| Topics / tags (#2) | yes | none — propose from repo content, confirm |
| Default branch | yes | auto-detect via `gh repo view --json defaultBranchRef` |
| Status-check contexts (#9) | yes | auto-detect from recent runs, confirm; if none yet, see note |
| New repo visibility (create flow) | when creating | ask: private (recommended) / public |

## Safety Rules

- Every step is **state-changing on someone's repo** — confirm the target `owner/repo` before any write.
- Branch protection needs admin. If `gh` lacks admin, report and skip protection (don't fail the rest).
- Never overwrite an existing README.md, CLAUDE.md, or rule file without showing a diff and confirming.
- `enforce_admins: false` (Solo) is intentional — do not silently flip to strict without asking.
- Squash-only + `required_linear_history` are consistent; do not enable merge commits alongside linear history.
- Never set topics/description from this skill's repo as defaults — they belong to the target repo.

## Confirmation Policy

Read-only (no confirmation):

```bash
gh auth status
gh repo view owner/repo --json defaultBranchRef,description,repositoryTopics,hasProjectsEnabled,hasWikiEnabled,squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge
gh api repos/owner/repo/branches/<main>/protection
gh run list --branch <main> --json name,workflowName,conclusion
```

Require confirmation (state-changing):

```bash
gh repo create ...
gh repo edit owner/repo ...
gh api -X PUT repos/owner/repo/branches/<main>/protection ...
# writing README.md / CLAUDE.md / AGENTS.md / .claude/rules/*.md
```

## Idempotency

- `gh repo edit` and the protection `PUT` are declarative — re-running converges to desired state.
- Docs scaffolding is create-if-missing; existing files are diffed, never clobbered silently.
- The AGENTS.md mirror is regenerated from CLAUDE.md each run; verify `diff -q CLAUDE.md AGENTS.md` is empty.

## References

- [Repo settings](references/repo-settings.md) — description, topics, projects/wiki, squash-only, delete-on-merge
- [Branch protection](references/branch-protection.md) — Solo profile PUT + status-check auto-detection
- [Docs scaffold](references/docs-scaffold.md) — README, CLAUDE.md + AGENTS.md mirror, `.claude/rules/*.md`
- [Verify](references/verify.md) — dry-run + post-run drift report

## Templates

- `templates/CLAUDE.md` — canonical agent-instructions file referencing `.claude/rules/*.md`
- `templates/rules/*.md` — generic starter rules (git workflow, code style, security)

AGENTS.md is not a template — it is generated as a byte-identical copy of CLAUDE.md.
