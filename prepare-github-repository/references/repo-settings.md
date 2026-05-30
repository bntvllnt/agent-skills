# Repo Settings (`gh repo edit`)

Covers desired-state items #1–#6. All of it is one declarative `gh repo edit` call, so it is
idempotent — re-running reconciles drift.

## Preflight

```bash
gh auth status                                   # confirm authenticated
REPO="owner/repo"                                # or: gh repo view --json nameWithOwner -q .nameWithOwner
gh repo view "$REPO" --json nameWithOwner,visibility,description,repositoryTopics
```

## One-shot (recommended)

Confirm `$REPO`, `DESCRIPTION`, and `TOPICS` with the user first — never invent them.

```bash
gh repo edit "$REPO" \
  --description "$DESCRIPTION" \
  --add-topic topic-a --add-topic topic-b \
  --enable-projects=false \
  --enable-wiki=false \
  --enable-squash-merge=true \
  --enable-merge-commit=false \
  --enable-rebase-merge=false \
  --delete-branch-on-merge=true
```

## Per-setting breakdown

| # | Setting | Flag |
|---|---|---|
| 1 | Description | `--description "$DESCRIPTION"` |
| 2 | Topics / tags | `--add-topic <t>` (repeat per topic) |
| 3 | Disable Projects | `--enable-projects=false` |
| 4 | Disable Wiki | `--enable-wiki=false` |
| 5 | Squash only | `--enable-squash-merge=true --enable-merge-commit=false --enable-rebase-merge=false` |
| 6 | Delete branch on merge | `--delete-branch-on-merge=true` |

## Topics / tags notes

- `--add-topic` only adds. To get an exact set, read current topics and remove the unwanted ones:

```bash
# Current topics
gh repo view "$REPO" --json repositoryTopics -q '.repositoryTopics[].name'

# Remove a stale topic
gh repo edit "$REPO" --remove-topic old-topic
```

- Topic rules (GitHub): lowercase, digits, hyphens; start with a letter/number; max 50 chars; up to 20 topics.
- Propose topics from repo content (language, framework, domain) and **confirm** before applying.

## Verify

```bash
gh repo view "$REPO" --json \
  description,repositoryTopics,hasProjectsEnabled,hasWikiEnabled,\
squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge
```

Desired result:

```json
{
  "hasProjectsEnabled": false,
  "hasWikiEnabled": false,
  "squashMergeAllowed": true,
  "mergeCommitAllowed": false,
  "rebaseMergeAllowed": false,
  "deleteBranchOnMerge": true
}
```

Plus a non-empty `description` and `repositoryTopics`.

## Gotchas

- Disabling Projects/Wiki hides existing content; it is not deleted. Re-enabling restores it.
- If the org disables repo-level Projects centrally, the flag is a no-op — note it, don't fail.
- `gh repo edit` needs push/admin access; read-only tokens fail here.
