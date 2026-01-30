# Create Release (gh)

Goal: create a GitHub Release for a specific tag with correct notes and safe defaults.

**MANDATORY: Follow `release-strategy.md` for versioning, title format, and description format.** Never publish a release without the enforced description structure (summary + New Files table + Changed Files table).

Requires confirmation before running `gh release create`.

## Important Safety Fact

Per the official `gh release create` docs: if the tag does not exist yet, `gh` may create it automatically from the default branch.

Default safe behavior for this skill:

- Prefer creating the git tag first (outside this workflow), then create the release.
- Use `--verify-tag` to abort if the tag doesn't already exist in the remote.

## Pre-flight (read-only)

```bash
gh auth status
gh release list
```

## Create a release (recommended)

Generated notes:

```bash
gh release create vX.Y.Z --verify-tag --title "vX.Y.Z" --generate-notes
```

Custom notes:

```bash
gh release create vX.Y.Z --verify-tag --title "vX.Y.Z" --notes "<notes>"
```

Notes from annotated tag (or commit message if lightweight tag):

```bash
gh release create vX.Y.Z --verify-tag --notes-from-tag
```

## Common options

- Pre-release:

```bash
gh release create vX.Y.Z --verify-tag --prerelease --generate-notes
```

- Draft (publish later):

```bash
gh release create vX.Y.Z --verify-tag --draft --generate-notes
```

- Fail when there are no new commits since last release:

```bash
gh release create vX.Y.Z --verify-tag --generate-notes --fail-on-no-commits
```

- Control "Latest":

```bash
gh release create vX.Y.Z --verify-tag --generate-notes --latest=false
```

- Create a discussion:

```bash
gh release create vX.Y.Z --verify-tag --generate-notes --discussion-category "General"
```

## Different repository

Use `-R` / `--repo` to target a different repo:

```bash
gh release create vX.Y.Z --verify-tag --generate-notes -R OWNER/REPO
```

## Verify

```bash
gh release view vX.Y.Z
```
