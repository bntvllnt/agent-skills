# Version Sync

Version detection, public-metadata scanning, and doc bumping logic for the version-sync flow (`/oss bump` or equivalent natural-language request).

## Scope

This flow updates more than raw version strings. It also audits public install/publish metadata so docs match the real package manifest, registry, release URLs, and homepage/docs domain.

Targets:

- stale version strings
- package install commands (`npm`, `pnpm`, `yarn`, `pip`, `cargo`, `go get`)
- published package/module name mismatches
- registry URL mismatches
- homepage/docs domain mismatches
- release/download/tag URL mismatches

## Current Metadata Detection

| Field | Source | Detection |
|--------|--------|-----------|
| Current version | `package.json` | `node -e "console.log(require('./package.json').version)"` |
| Current version | `Cargo.toml` | `grep '^version' Cargo.toml \| head -1` |
| Current version | `pyproject.toml` | `grep '^version' pyproject.toml \| head -1` |
| Current version | `go.mod` / tags | `git describe --tags --abbrev=0` |
| Package name | `package.json` | `node -e "console.log(require('./package.json').name)"` |
| Package name | `Cargo.toml` / `pyproject.toml` | parse `name = "..."` |
| Registry URL | `package.json.publishConfig.registry` | parse JSON |
| Homepage/docs URL | `package.json.homepage` or repo metadata | parse JSON / `gh repo view` |
| Repo URL | manifest repo URL or `git remote get-url origin` | normalize to canonical source URL |

### Previous Version Detection

```bash
# Get semver-ish tags sorted descending
TAGS=$(git tag --sort=-v:refname | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+' | head -5)

# V_CURRENT = manifest version first, falling back to the newest tag
# V_PREV = next newest tag when present
V_PREV=$(echo "$TAGS" | sed -n '2p')
```

If no tags exist: use the manifest version as `V_CURRENT` and skip the previous-version diff preview when `V_PREV` is unknown.

## Files to Scan

```text
README.md
docs/**/*.md
llms.txt
llms-full.txt
AGENTS.md
selected harness aliases (for example: CLAUDE.md, .cursorrules, .windsurfrules, codex.md, .opencode/config)
CHANGELOG.md (verify V_CURRENT entry exists)
```

## Metadata to Match

### Versions

```regex
{V_PREV}
npm install {package}@{V_PREV}
pip install {package}=={V_PREV}
cargo add {package}@{V_PREV}
go get {module}@v{V_PREV}
badge/v{V_PREV}
:{V_PREV}
/releases/tag/v{V_PREV}
```

### Package / Module Names

Check install snippets and release docs for references to an old package name or module path.

Examples:

```text
npm install old-name
pnpm add @old-scope/pkg
pip install old-package
cargo add old-crate
go get github.com/old-org/old-module
```

### Registry and Publish Targets

Check for mismatches between docs and actual publish destination.

Examples:

```text
https://registry.npmjs.org
https://npm.pkg.github.com
https://pypi.org/project/...
crates.io/crates/...
proxy.golang.org/...
```

### Homepage / Docs / Release URLs

Check for stale domains or repo slugs in public docs.

Examples:

```text
https://old-docs.example.com
https://github.com/old-org/old-repo
/releases/tag/v...
/download/...
```

## Scan Commands

```bash
V_BARE=$(echo "$V_PREV" | sed 's/^v//')
ALIASES=$(find . -maxdepth 2 \( \
  -name 'CLAUDE.md' -o \
  -name '.cursorrules' -o \
  -name '.windsurfrules' -o \
  -name 'codex.md' -o \
  -path './.opencode/config' -o \
  -name '.aider.conf.yml' \
\) 2>/dev/null)

printf '%s\n' README.md docs/ llms.txt llms-full.txt AGENTS.md $ALIASES |
  xargs -r grep -rn "$V_BARE" 2>/dev/null
```

Also search for the previous package name, stale registry hostname, stale homepage hostname, and stale repo slug when those values are known.

## Mismatch Detection Rules

### Package Name / Install Guidance

Flag docs when:

- install instructions use a package name different from the manifest name
- import examples use a stale package/module name after a rename
- publish docs reference the wrong registry for the current package metadata

### Registry Guidance

Flag docs when:

- README says GitHub Packages but `publishConfig.registry` targets npm
- docs still mention a private registry after moving to a public registry
- publish workflow and public docs disagree on target registry

### Homepage / Docs Domain

Flag docs when:

- manifest homepage and README/docs point at different domains
- release workflow publishes to one docs domain while docs still mention another
- repo slug changed but public links still use the old owner/repo path

## Bump Preview

Present matches before applying:

```text
Version + metadata sync preview
Current version: {V_CURRENT}
Previous version: {V_PREV or "unknown"}
Package name: {PKG_NAME}
Registry: {REGISTRY_URL or "default"}
Homepage/docs: {HOMEPAGE_URL or "not set"}

Found {N} updates:

  README.md:15     npm install foo@1.2.3     →  npm install foo@1.3.0
  README.md:18     npm install old-name      →  npm install @scope/foo
  README.md:42     npm.pkg.github.com        →  registry.npmjs.org
  docs/api.md:3    https://old-docs.example  →  https://docs.example
  llms.txt:2       > foo v1.2.3              →  > foo v1.3.0

Apply all? [yes / pick / cancel]
```

## Apply

After confirmation:

1. Replace stale version strings with `V_CURRENT`
2. Replace stale package/module names with the current manifest/module name
3. Replace stale registry URLs with the actual publish target
4. Replace stale homepage/docs/release URLs with the current canonical values
5. Verify `CHANGELOG.md` has an entry for `V_CURRENT`
6. Regenerate `llms.txt` and `llms-full.txt` if they exist
7. Re-scan to verify no stale version/package/registry/homepage references remain

## CHANGELOG Verification

```bash
grep -q "$V_CURRENT" CHANGELOG.md
```

If missing, suggest:

```text
## [{V_CURRENT}] - YYYY-MM-DD

### Added
- 

### Changed
- 

### Fixed
- 
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No version in manifest | Use git tags. If none: report `No version detected.` |
| No tags exist | Still run metadata scan; skip previous-version-only preview lines |
| `V_PREV` not found anywhere | Report `No stale version references found` but still scan package/registry/homepage metadata |
| Package rename with same version | Flag/install guidance mismatches even when version strings already match |
| Repo/domain rename with same version | Flag stale repo slug or docs hostname references even when version strings already match |
| Monorepo | Detect package scope from pwd and only scan docs owned by that package |
| Pre-release versions | Match the full pre-release suffix |
