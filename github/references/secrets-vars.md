# Secrets and Variables

Use these for GitHub Actions and repository configuration.

List:

```bash
gh secret list
gh variable list
```

Set (confirm first):

```bash
gh secret set NAME
gh variable set NAME
```

Delete (confirm first):

```bash
gh secret delete NAME
gh variable delete NAME
```

Safety:

- Never print secret values.
- Avoid using command history to pass secrets inline.
