# Branch Protection (`gh api`)

Covers desired-state items #7–#9. `gh repo edit` cannot set protection — use the protection API.
Requires **admin** on the repo. The `PUT` is declarative (full replace), so it is idempotent.

## 1. Resolve the default branch

```bash
REPO="owner/repo"
BRANCH=$(gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name)
echo "$BRANCH"   # usually main
```

## 2. Auto-detect required status checks (#9)

Collect check names from recent runs on the default branch, then **confirm the set** with the user.

```bash
# Check runs on the latest commit of the default branch
gh api "repos/$REPO/commits/$BRANCH/check-runs" --jq '.check_runs[].name' | sort -u

# Fallback: workflow run / job names
gh run list --repo "$REPO" --branch "$BRANCH" --limit 20 \
  --json workflowName,name -q '.[].name' | sort -u
```

- Present the detected names; let the user trim/confirm. These strings are the `contexts`.
- **No checks yet** (fresh repo, CI never ran): you cannot require a context that has never reported.
  Options:
  - Apply protection now with `required_status_checks: null`, then re-run this skill after the
    first CI run to add contexts, OR
  - Ask the user to name the expected check(s) and require them up front (they will block merges
    until the first run reports — acceptable if CI is already wired in `.github/workflows`).
  Pick with the user; default to `null` + a note to re-run.

## 3. Apply the Solo profile

Build the payload, then PUT. Replace `<CHECKS>` with a JSON array of confirmed contexts, or use
`null` for `required_status_checks` if none.

```bash
cat > /tmp/protection.json <<JSON
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci", "lint"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
JSON

gh api -X PUT "repos/$REPO/branches/$BRANCH/protection" \
  -H "Accept: application/vnd.github+json" \
  --input /tmp/protection.json
```

If there are no detectable checks and the user opts for none, set:

```json
"required_status_checks": null,
```

## Field rationale (Solo)

| Field | Value | Why |
|---|---|---|
| `required_pull_request_reviews` | present | Enforces PR — direct push to `main` is rejected |
| `required_approving_review_count` | `0` | Solo can self-merge; PR still mandatory |
| `dismiss_stale_reviews` | `true` | New commits invalidate old approvals |
| `enforce_admins` | `false` | Keeps a hotfix escape hatch for the maintainer |
| `required_status_checks.strict` | `true` | Branch must be up to date before merge |
| `required_linear_history` | `true` | Clean history; consistent with squash-only merges |
| `allow_force_pushes` / `allow_deletions` | `false` | Protect `main` history and existence |
| `required_conversation_resolution` | `true` | All review threads resolved before merge |
| `restrictions` | `null` | No push allowlist (solo / small repo) |

For **Solo-strict**, set `enforce_admins: true`. For **Team**, set
`required_approving_review_count: 1` and `require_code_owner_reviews: true`. Ask before changing
the profile — Solo is this skill's default.

## 4. Verify

```bash
gh api "repos/$REPO/branches/$BRANCH/protection" --jq '{
  pr: .required_pull_request_reviews.required_approving_review_count,
  dismiss_stale: .required_pull_request_reviews.dismiss_stale_reviews,
  admins: .enforce_admins.enabled,
  strict_checks: .required_status_checks.strict,
  contexts: .required_status_checks.contexts,
  linear: .required_linear_history.enabled,
  force: .allow_force_pushes.enabled,
  deletions: .allow_deletions.enabled,
  conversation: .required_conversation_resolution.enabled
}'
```

## Gotchas

- Protection requires admin; a non-admin token returns 403 — report and skip, don't abort the run.
- The protection `PUT` is a **full replace** of these fields — always send the complete payload.
- `required_status_checks` cannot list a context that has never reported on the branch.
- Rulesets (`repos/$REPO/rulesets`) are a newer alternative; classic protection above is sufficient
  and simpler for a single-branch policy. Don't mix both on `main` — they can double-enforce.
