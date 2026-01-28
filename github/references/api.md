# API (gh api)

`gh api` is powerful and can mutate GitHub state. Confirm before any write.

## Read-only example

```bash
gh api repos/OWNER/REPO
```

## Notes

- Prefer the dedicated `gh` subcommands (issue/pr/release/repo) when they exist.
- Use `-R OWNER/REPO` with other commands instead of hardcoding URLs.
