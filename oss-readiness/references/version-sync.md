# Version Sync

Version detection, reference scanning, and doc bumping logic for the version-sync flow (`/oss bump` or equivalent natural-language request).

## Version Detection

| Source | Detection | Parse |
|--------|-----------|-------|
| package.json | `node -e "console.log(require('./package.json').version)"` | Direct JSON |
| Cargo.toml | `grep '^version' Cargo.toml \| head -1` | `version = "x.y.z"` |
| pyproject.toml | `grep '^version' pyproject.toml \| head -1` | `version = "x.y.z"` |
| go.mod | `git describe --tags --abbrev=0` | Tag-based |
| git tags | `git tag --sort=-v:refname \| head -1` | Fallback for all |

### Previous Version Detection

```bash
# Get all semver tags sorted descending
TAGS=$(git tag --sort=-v:refname | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+' | head -5)

# V_CURRENT = first tag (or from manifest)
# V_PREV = second tag
V_PREV=$(echo "$TAGS" | sed -n '2p')
```

If no tags exist: skip version bump, report "No version tags found. Tag a release first."

## Version Reference Scanning

### Files to Scan

```text
README.md
docs/**/*.md
llms.txt
llms-full.txt
AGENTS.md
selected harness aliases (for example: CLAUDE.md, .cursorrules, .windsurfrules, codex.md, .opencode/config)
CHANGELOG.md (verify V_CURRENT entry exists)
```

### Patterns to Match

```regex
# Exact version string (most common)
{V_PREV}

# Common version patterns in docs:
npm install {package}@{V_PREV}
pip install {package}=={V_PREV}
cargo add {package}@{V_PREV}
go get {module}@v{V_PREV}

# Badge URLs
badge/v{V_PREV}
shields.io/.*{V_PREV}

# Docker tags
:{V_PREV}

# CDN/download URLs
/v{V_PREV}/
/download/{V_PREV}/
/releases/tag/v{V_PREV}
```

### Scan Command

```bash
# Strip 'v' prefix for matching both v1.2.3 and 1.2.3
V_BARE=$(echo "$V_PREV" | sed 's/^v//')

ALIASES=$(find . -maxdepth 2 \( \
  -name 'CLAUDE.md' -o \
  -name '.cursorrules' -o \
  -name '.windsurfrules' -o \
  -name 'codex.md' -o \
  -path './.opencode/config' -o \
  -name '.aider.conf.yml' \
\) 2>/dev/null)

# Scan all target files
printf '%s\n' README.md docs/ llms.txt llms-full.txt AGENTS.md $ALIASES |
  xargs -r grep -rn "$V_BARE" 2>/dev/null
```

## Bump Preview

Present matches to user before applying:

```
Version bump: {V_PREV} → {V_CURRENT}

Found {N} references to update:

  README.md:15     npm install foo@1.2.3     →  npm install foo@1.3.0
  README.md:42     badge/v1.2.3              →  badge/v1.3.0
  docs/api.md:3    Since v1.2.3              →  Since v1.3.0
  llms.txt:2       > foo v1.2.3              →  > foo v1.3.0

Apply all? [yes / pick / cancel]
```

## Bump Apply

After user confirmation:

1. For each match, replace V_PREV with V_CURRENT using the agent's file-edit capability
2. Verify CHANGELOG.md has entry for V_CURRENT
   - If missing: warn "CHANGELOG.md has no entry for {V_CURRENT}. Add one?"
3. If llms.txt or llms-full.txt exist: regenerate via the llms generation flow
4. Re-scan to verify 0 stale references remain

## CHANGELOG Verification

```bash
# Check CHANGELOG has current version
grep -q "$V_CURRENT" CHANGELOG.md

# If missing, suggest entry:
echo "## [{V_CURRENT}] - $(date +%Y-%m-%d)"
echo ""
echo "### Added"
echo "- "
echo ""
echo "### Changed"
echo "- "
echo ""
echo "### Fixed"
echo "- "
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No version in manifest | Use git tags. If none: "No version detected." |
| V_PREV not found anywhere | "No stale version references found. Docs are up to date." |
| Version in code (not docs) | Skip — code versions are managed by package manager, not docs |
| User provides explicit V_PREV | Use provided version instead of auto-detecting |
| Monorepo | Detect package scope from pwd, only scan that package's docs |
| Pre-release versions (1.0.0-beta.1) | Match including pre-release suffix |
