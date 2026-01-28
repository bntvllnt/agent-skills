# GitHub

GitHub skill using GitHub CLI (`gh`): repos, issues, pull requests, Actions, releases, and more.

## Quick Start

- Home/router: `github/SKILL.md`
- Auth: `github/references/auth.md`
- Repos: `github/references/repo.md`
- Issues: `github/references/issue.md`
- PRs: `github/references/pr.md`
- Actions: `github/references/actions.md`
- Releases: `github/references/release.md`
- Advanced API: `github/references/api.md`

Release deep dives:

- Create: `github/references/release-create.md`
- Manage: `github/references/release-manage.md`
- Assets: `github/references/release-assets.md`

## Requirements

- `gh` (GitHub CLI)
- Authenticated session: `gh auth login`

## Install

```bash
npx skills add bntvllnt/agent-skills --skill github
```

Manual install (download this folder only):

- Copy the `github/` folder into your agent's skills directory.
- Ensure the folder name is `github` and includes `SKILL.md`.
