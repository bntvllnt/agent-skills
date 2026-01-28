# Manage Releases (list/view/edit/delete)

## List releases (read-only)

```bash
gh release list
```

Common filters:

```bash
gh release list --exclude-drafts
gh release list --exclude-pre-releases
gh release list --limit 50
```

## View a release (read-only)

```bash
gh release view vX.Y.Z
gh release view vX.Y.Z --web
```

## Edit a release (confirm first)

Update notes from a file:

```bash
gh release edit vX.Y.Z --notes-file release-notes.md
```

Publish a draft:

```bash
gh release edit vX.Y.Z --draft=false
```

Set prerelease:

```bash
gh release edit vX.Y.Z --prerelease
```

## Delete a release (confirm first)

```bash
gh release delete vX.Y.Z
```

If you explicitly want to also delete the tag:

```bash
gh release delete vX.Y.Z --cleanup-tag
```
