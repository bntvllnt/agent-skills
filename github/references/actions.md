# Actions (gh workflow / gh run)

List workflows:

```bash
gh workflow list
```

View a workflow:

```bash
gh workflow view <workflow>
```

Run a workflow (confirm first):

```bash
gh workflow run <workflow>
```

List runs:

```bash
gh run list
```

View a run:

```bash
gh run view <run-id>
```

Download artifacts:

```bash
gh run download <run-id>
```

Rerun or cancel (confirm first):

```bash
gh run rerun <run-id>
gh run cancel <run-id>
```
