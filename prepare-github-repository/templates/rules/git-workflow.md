# Git Workflow

Mirrors the repository's enforced GitHub settings. Keep local habits aligned with branch protection.

- Branch from `{PRIMARY_BRANCH}`; never commit directly to it (protection rejects direct pushes).
- One focused PR per change. Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`,
  `test:`, `perf:`.
- **Squash merge only** — the repo allows no merge commits or rebase merges. Write a clean squash
  title; it becomes the `{PRIMARY_BRANCH}` history entry.
- Keep your branch **up to date** with `{PRIMARY_BRANCH}` before merge (status checks are strict).
- Resolve all PR conversations before merge (required).
- The head branch is **auto-deleted on merge** — no manual cleanup.
- Force-push and deletion of `{PRIMARY_BRANCH}` are blocked. Don't fight protection; open a PR.
