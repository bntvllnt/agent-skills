# Prepare GitHub Repository

Apply a standard GitHub repository configuration in one idempotent pass, then verify it.

## What it sets

| Area | Result |
|---|---|
| Metadata | Description + topics/tags set |
| Features | Projects + Wiki disabled |
| Merges | Squash-only; auto-delete head branch on merge |
| Protection | `main` protected: PR required (0 approvals, Solo profile), strict status checks, no force-push/deletion, linear history, conversation resolution |
| Email privacy | Commit identity forced to your GitHub no-reply; server-side ruleset rejects any commit with a non-no-reply email (CI guard + account block-push as fallback layers) |
| Docs | `README.md` present; `CLAUDE.md` referencing `.claude/rules/*.md`; `AGENTS.md` as a byte-identical mirror of `CLAUDE.md`; starter `.claude/rules/*.md` |

Defaults baked in: **Solo** protection profile, **full content mirror** for AGENTS.md,
**auto-detect + require** CI status checks. All overridable per run.

## Entry points

```text
prepare owner/repo        # configure an existing repo
prepare                   # configure the current repo's origin
prepare new my-repo       # create, then configure
verify repo prep owner/repo   # read-only dry-run / drift report
```

Or target one stage: `apply repo settings`, `harden main`, `scaffold repo docs`.

## Requirements

- GitHub CLI (`gh`) authenticated with the `repo` scope.
- **Admin** on the target repo (branch protection). Without admin, protection is skipped and
  reported; the rest still applies.
- Optional: `git`, `jq`.

## Install

```bash
npx skills add bntvllnt/agent-skills --skill prepare-github-repository
```

## Safety

- Confirms the target `owner/repo` before any write.
- Existing `README.md` / `CLAUDE.md` / rule files are diffed and confirmed — never clobbered.
- Description and topics are never guessed from this skill's repo — they belong to the target.

See [SKILL.md](SKILL.md) for the full router, desired-state contract, and references.
