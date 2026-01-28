# Tags Workflow

Goal: create consistent version tags safely.

Requires confirmation for any tag creation/deletion.

## Best Practices

- Prefer SemVer tags: `vMAJOR.MINOR.PATCH` (example: `v1.2.3`).
- Use annotated tags for releases (not lightweight tags).
- Tag the exact commit you want to release (usually the merge commit to the base branch).
- Do not move/retag public tags unless explicitly requested.

## Read-Only Checks

```bash
git status
git log --oneline -n 10
git tag -l
git describe --tags --always
```

## Create a Release Tag (Annotated)

1. Ensure you're on the intended branch/commit and the working tree is clean.
2. Choose the next version tag.

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
```

3. Push the tag:

```bash
git push origin vX.Y.Z
```

## Verify

```bash
git show vX.Y.Z
```

## Fixes / Recovery (Confirm First)

### Delete a local tag

```bash
git tag -d vX.Y.Z
```

### Delete a remote tag

Only if you understand consumers may already be using it.

```bash
git push --delete origin vX.Y.Z
```

### Move a tag (rewriting public history)

Avoid. Only do this if explicitly requested and after explaining impact.
