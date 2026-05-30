# Verify (dry-run + post-run drift)

Read-only. Run it twice: once as a dry-run before changes (shows the gap), once after (proves the
result). Compares live state against the Desired State table in `SKILL.md`.

```bash
REPO="owner/repo"
BRANCH=$(gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name)
```

## Settings (#1–#6)

```bash
gh repo view "$REPO" --json \
  description,repositoryTopics,hasProjectsEnabled,hasWikiEnabled,\
squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge \
  --jq '{
    description: (.description | length > 0),
    topics: (.repositoryTopics | length),
    projects_off: (.hasProjectsEnabled == false),
    wiki_off: (.hasWikiEnabled == false),
    squash_only: (.squashMergeAllowed and (.mergeCommitAllowed | not) and (.rebaseMergeAllowed | not)),
    delete_on_merge: .deleteBranchOnMerge
  }'
```

Expected: `description: true`, `topics >= 1`, all booleans `true`.

## Protection (#7–#9)

```bash
gh api "repos/$REPO/branches/$BRANCH/protection" --jq '{
  pr_required: (.required_pull_request_reviews != null),
  approvals: .required_pull_request_reviews.required_approving_review_count,
  dismiss_stale: .required_pull_request_reviews.dismiss_stale_reviews,
  admins_enforced: .enforce_admins.enabled,
  strict_checks: .required_status_checks.strict,
  contexts: .required_status_checks.contexts,
  linear: .required_linear_history.enabled,
  force_push: .allow_force_pushes.enabled,
  deletions: .allow_deletions.enabled,
  conversation: .required_conversation_resolution.enabled
}' 2>/dev/null || echo "no protection (or no admin access)"
```

Expected (Solo): `pr_required: true`, `approvals: 0`, `admins_enforced: false`,
`strict_checks: true`, `linear: true`, `force_push: false`, `deletions: false`,
`conversation: true`.

## Docs (#10–#13) — run in the repo working copy

```bash
for f in README.md CLAUDE.md AGENTS.md; do
  test -f "$f" && echo "present: $f" || echo "MISSING: $f"
done
diff -q CLAUDE.md AGENTS.md >/dev/null 2>&1 && echo "mirror OK" || echo "MIRROR DRIFT"
ls .claude/rules/*.md >/dev/null 2>&1 && echo "rules present" || echo "MISSING: .claude/rules/*.md"
```

## Email privacy (#14–#15) — run in the repo working copy

```bash
NOREPLY=$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')
test "$(git config user.email)" = "$NOREPLY" && echo "identity OK" || echo "IDENTITY WRONG"
git log --format='%ae%n%ce' | sort -u | grep -vE '@users\.noreply\.github\.com$' \
  && echo "LEAK: non-no-reply email in history" || echo "history clean"
test -f .github/workflows/email-guard.yml && echo "CI guard present" || echo "MISSING CI guard"
```

The account setting ("Block command line pushes that expose my email") has no read API — verify it
manually at `https://github.com/settings/emails` and record it as a MANUAL check.

## Report format

```text
PREPARE GITHUB REPOSITORY — owner/repo (branch: main)
  #1  description ............ PASS
  #2  topics ................. PASS (3)
  #3  projects disabled ...... PASS
  #4  wiki disabled .......... PASS
  #5  squash-only ............ PASS
  #6  delete-on-merge ........ PASS
  #7  main protection ........ PASS
  #8  PR required (0 appr) .... PASS
  #9  status checks (strict).. WARN (no contexts — CI not run yet)
  #10 README.md .............. PASS
  #11 CLAUDE.md .............. PASS
  #12 AGENTS.md mirror ....... PASS
  #13 .claude/rules/*.md ..... PASS (3)
```

Mark any non-PASS with the exact remediation step (which reference + command).
