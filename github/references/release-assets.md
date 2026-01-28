# Release Assets (upload/download/verify)

Requires confirmation for upload/delete-asset.

## Upload assets

Upload a file:

```bash
gh release upload vX.Y.Z <file>
```

Overwrite existing asset name:

```bash
gh release upload vX.Y.Z <file> --clobber
```

Add a display label by appending `#`:

```bash
gh release upload vX.Y.Z "dist/app.zip#macOS build"
```

## Delete an asset (confirm first)

```bash
gh release delete-asset vX.Y.Z <asset-name>
```

## Download assets

All assets from a tag:

```bash
gh release download vX.Y.Z
```

Latest release by pattern:

```bash
gh release download --pattern '*.tgz'
```

Download source archive:

```bash
gh release download vX.Y.Z --archive=zip
```

## Verify release attestation

If your repo uses GitHub release attestations:

```bash
gh release verify vX.Y.Z
```

JSON output:

```bash
gh release verify vX.Y.Z --format json
```
