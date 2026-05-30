# Email Privacy / No-Reply Enforcement

Covers desired-state items #14–#15. Goal: a personal email can **never** end up in a pushed
commit. Every commit must be authored + committed with the GitHub no-reply address, and pushes
that would expose a real email must be blocked.

The leak vector: `user.email` is embedded in every commit object and is public once pushed —
`git log`, the GitHub UI, the API, and the commits patch all expose it. Setting it after the fact
does not rewrite history.

## The allowed identity

GitHub no-reply: `<id>+<login>@users.noreply.github.com`. Resolve it (never hardcode in a public
repo, never write a personal email anywhere):

```bash
gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'
# also visible at https://github.com/settings/emails ("Keep my email addresses private")
```

`<login>@users.noreply.github.com` (no id prefix) is the legacy form; prefer the id-prefixed form,
which requires "Keep my email addresses private" enabled.

## Defense in depth (apply all that are available)

```text
A. Account setting  -> blocks the leak at the source, every repo, every push   (root cause)
B. Repo-local config -> commits start clean                                     (prevention)
E. Ruleset metadata  -> native server-side rule: GitHub rejects the push        (repo config, strongest)
C. CI guard          -> PR fails if any commit email is disallowed              (portable fallback)
D. Pre-push hook     -> local stop before the push leaves your machine          (optional)
```

### A. Account setting (root cause — set once, protects all repos)

`https://github.com/settings/emails`:

- [x] **Keep my email addresses private** — GitHub uses your no-reply for web Git ops + notifications.
- [x] **Block command line pushes that expose my email** — GitHub inspects the most recent commit;
  if its author email is one of your private account emails, the push is **rejected**.

This is the only layer that stops a leak even when local config is wrong. It is account-level (UI),
not a per-repo API call — the skill **instructs + verifies**, it cannot toggle it for you.
Add your real email(s) to the account so GitHub knows which addresses to block.

> Caveat: "Block pushes" checks the **most recent** commit only. Layers B/C catch the rest.

### B. Repo-local commit identity (prevention)

Set the prepared repo's identity to the no-reply so commits are clean from the first one:

```bash
NOREPLY=$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')
LOGIN=$(gh api user --jq '.login')
git config user.email "$NOREPLY"
git config user.name  "$LOGIN"
# verify
git config user.email
```

Optionally make it the machine-wide default so new clones inherit it:

```bash
git config --global user.email "$NOREPLY"
```

Worktrees inherit the repo config — confirm each worktree resolves the no-reply, not a personal email.

### C. CI guard (repo-level enforcement — require it on main)

Scaffold `templates/ci/email-guard.yml` into `.github/workflows/email-guard.yml`. It fails a PR if
any commit author **or** committer email in the PR range is not allowed. Then add its check name to
the required status checks in [branch-protection.md](branch-protection.md) (#9) so main cannot merge
a leaking commit.

Pattern modes (set `ALLOWED_EMAIL_PATTERN` at the top of the workflow):

| Mode | Pattern | Use when |
|---|---|---|
| Exact account ("only my account") | `^<ID>\+<LOGIN>@users\.noreply\.github\.com$` | solo repo — only your no-reply passes |
| Any no-reply | `@users\.noreply\.github\.com$` | you accept external PRs (contributors keep their own no-reply) |

Default to exact for solo repos. Switch to any-no-reply the moment you accept outside contributions,
or legitimate contributor PRs will fail the guard.

### D. Pre-push hook (optional, local belt-and-suspenders)

```bash
# .githooks/pre-push  (chmod +x)  -> enable with: git config core.hooksPath .githooks
#!/usr/bin/env sh
allowed='@users\.noreply\.github\.com$'   # or the exact ^<ID>+<LOGIN>...$
bad=$(git log --format='%ae%n%ce' @{push}..HEAD 2>/dev/null | sort -u | grep -vE "$allowed")
if [ -n "$bad" ]; then
  echo "push blocked: disallowed commit email(s):" >&2
  echo "$bad" >&2
  exit 1
fi
```

`core.hooksPath .githooks` makes the hook tracked + shareable (default `.git/hooks` is local-only,
not committed). Propose, do not auto-install hooks.

### E. Native ruleset metadata rule (strongest — server-side, recommended when available)

This is the actual GitHub **repo config** that enforces the email: a **repository ruleset** with a
`commit_author_email_pattern` (and `committer_email_pattern`) rule. GitHub evaluates it **on push**
and **rejects** any commit whose email doesn't match — before it ever lands. Unlike the CI guard (C),
which only fails the PR after the commit exists, this stops the leak server-side.

Availability: rulesets are free for **public** repos; **private** repos need GitHub Pro/Team/Enterprise.
Confirm the endpoint responds before relying on it: `gh api repos/{owner}/{repo}/rulesets` (read-only).

Create it (confirm first — state-changing). Target all branches so every push is checked:

```bash
gh api -X POST "repos/$REPO/rulesets" \
  -H "Accept: application/vnd.github+json" \
  --input - <<'JSON'
{
  "name": "no-reply-email-only",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~ALL"], "exclude": [] } },
  "rules": [
    {
      "type": "commit_author_email_pattern",
      "parameters": { "operator": "ends_with", "pattern": "@users.noreply.github.com", "negate": false, "name": "author email must be a GitHub no-reply" }
    },
    {
      "type": "committer_email_pattern",
      "parameters": { "operator": "ends_with", "pattern": "@users.noreply.github.com", "negate": false, "name": "committer email must be a GitHub no-reply" }
    }
  ]
}
JSON
```

Pattern modes:

| Mode | operator / pattern |
|---|---|
| Any no-reply (accepts contributors) | `"operator": "ends_with", "pattern": "@users.noreply.github.com"` |
| Exact account ("only my account") | `"operator": "regex", "pattern": "^<ID>\\+<LOGIN>@users\\.noreply\\.github\\.com$"` |

UI equivalent: Settings → Rules → Rulesets → New branch ruleset → enforcement Active → add
**Restrict commit metadata** → Commit author email + Committer email must match the pattern.

Prefer this ruleset as the baseline server-side guard where available; keep the CI guard (C) as the
portable fallback for repos where metadata rulesets aren't on the plan. They stack — run both.

## "Only my account" (push restriction)

For a solo repo, you are the only one with push access, so identity is the real control. To also
restrict who may push to `main` when collaborators exist, use branch-protection `restrictions`
(push allowlist) or a ruleset bypass list limited to your account — see
[branch-protection.md](branch-protection.md).

## Verify

```bash
NOREPLY=$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')
# repo identity is the no-reply
test "$(git config user.email)" = "$NOREPLY" && echo "identity OK" || echo "IDENTITY WRONG"
# no historical commit leaks a non-no-reply email
git log --format='%ae%n%ce' | sort -u | grep -vE '@users\.noreply\.github\.com$' \
  && echo "LEAK: non-no-reply email in history" || echo "history clean"
# CI guard present
test -f .github/workflows/email-guard.yml && echo "CI guard present" || echo "MISSING CI guard"
```

Account settings A cannot be read via API — verify manually at `https://github.com/settings/emails`
and record it as a manual check in the report.

## Never

- Never write a personal email into any file, commit, log line, PR, or example — use the no-reply or
  a placeholder. Avoiding the leak is the entire point of this reference.
- Never rewrite already-pushed history to "fix" a leak without explicit confirmation — and treat any
  exposed address as already public.
