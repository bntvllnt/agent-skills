# Authentication (gh)

Goal: ensure `gh` is authenticated for the correct host/account.

## Read-only checks

```bash
gh auth status
```

## Interactive login

```bash
gh auth login
```

Notes (from the official gh docs):

- Default host is `github.com`; enterprise hosts can be selected with `--hostname`.
- For headless/automation, `gh` can use tokens from environment variables (see `gh help environment`).

Example: authenticate to a specific host:

```bash
gh auth login --hostname enterprise.internal
```

## Safety

- Never paste tokens into logs or commit them.
- Prefer `gh auth login` browser flow when possible.
