# LLMs Generation

Algorithm for generating llms.txt and llms-full.txt files per the llmstxt.org specification.

## Overview

```
/oss llms
  │
  ├─ 1. Detect metadata (name, description, version)
  ├─ 2. Discover documentation files
  ├─ 3. Generate llms.txt (index with links)
  ├─ 4. Generate llms-full.txt (full content)
  └─ 5. Report results
```

## Step 1: Metadata Detection

```bash
# Package name
NAME=$(
  node -e "console.log(require('./package.json').name)" 2>/dev/null ||
  grep '^name' Cargo.toml 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)"/\1/' ||
  grep '^name' pyproject.toml 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)"/\1/' ||
  basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)
)

# Description
DESC=$(
  node -e "console.log(require('./package.json').description || '')" 2>/dev/null ||
  gh repo view --json description -q '.description' 2>/dev/null ||
  head -5 README.md 2>/dev/null | grep -v '^#' | head -1
)

# Version
VERSION=$(
  node -e "console.log(require('./package.json').version)" 2>/dev/null ||
  grep '^version' Cargo.toml 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)"/\1/' ||
  grep '^version' pyproject.toml 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)"/\1/' ||
  git describe --tags --abbrev=0 2>/dev/null ||
  echo "0.0.0"
)
```

## Step 2: Content Discovery

Scan repo for documentation files in priority order:

```bash
# Core docs (always included)
README="README.md"
CONTRIBUTING=$(test -f CONTRIBUTING.md && echo "CONTRIBUTING.md")
CHANGELOG=$(test -f CHANGELOG.md && echo "CHANGELOG.md")
LICENSE=$(ls LICENSE* 2>/dev/null | head -1)

# Documentation directory
DOCS=$(find docs/ -name "*.md" -type f 2>/dev/null | sort)

# API documentation
API_DOCS=$(
  find docs/api* -name "*.md" 2>/dev/null ||
  find api-docs/ -name "*.md" 2>/dev/null ||
  find docs/ -name "api*.md" 2>/dev/null
)

# Examples
EXAMPLES=$(find examples/ -type f 2>/dev/null | sort)

# Additional docs
SECURITY=$(test -f SECURITY.md && echo "SECURITY.md")
COC=$(test -f CODE_OF_CONDUCT.md && echo "CODE_OF_CONDUCT.md")
AGENTS=$(test -f AGENTS.md && echo "AGENTS.md")
```

## Step 3: Generate llms.txt

Format per llmstxt.org specification:

```markdown
# {NAME}

> {DESC}

{First paragraph of README.md — extract text between H1 and first H2, strip markdown formatting}

## Docs

- [README](README.md): Project overview, installation, and usage guide
- [Contributing](CONTRIBUTING.md): How to contribute to this project
- [Changelog](CHANGELOG.md): Version history and release notes

## API Reference

- [{doc_name}]({doc_path}): {first line of file or generated description}

## Examples

- [{example_name}]({example_path}): {description from first comment or filename}

## Optional

- [Security Policy](SECURITY.md): Vulnerability reporting and disclosure policy
- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines
- [License](LICENSE): {license type} license
```

### llms.txt Format Rules

1. **H1** (required): Package/project name — the only mandatory element
2. **Blockquote** (optional): One-line description with key context
3. **Body** (optional): Paragraphs/lists but NO headings — project overview
4. **H2 sections** (optional): Each contains a markdown list of resources
5. Each list item: `- [name](url): description` format (colon + description optional)
6. **"Optional" section**: If included, signals these URLs can be skipped for shorter contexts
7. Use relative paths for repo files (not absolute URLs)

### Section Selection Logic

```
Always include:
  - Docs section (README, CONTRIBUTING, CHANGELOG — if they exist)

Include if files exist:
  - API Reference (docs/api*.md or similar)
  - Examples (examples/ directory)

Always include as Optional:
  - Security, Code of Conduct, License
```

### Description Generation

For each linked file, generate a concise description:
- README.md: "Project overview, installation, and usage guide"
- CONTRIBUTING.md: "Contribution guidelines and development setup"
- CHANGELOG.md: "Version history and release notes"
- API docs: Extract first line/heading of the file
- Examples: Use filename or first comment line
- If unknown: "{filename} documentation"

## Step 4: Generate llms-full.txt

Same H1 + blockquote header as llms.txt, but embeds full content:

```markdown
# {NAME}

> {DESC}

{First paragraph of README.md}

## Docs

### README
{Full README.md content — strip badges/shields if desired}

### Contributing
{Full CONTRIBUTING.md content}

### Changelog
{CHANGELOG.md content — TRUNCATED to last 5 versions if file >20KB}

## API Reference

### {API Doc Title}
Source: {relative_path}

{Full content of API doc file}

## Examples

### {Example Name}
Source: {relative_path}

```{language}
{Full content of example file}
```

## Optional

### Security Policy
Source: SECURITY.md

{Full SECURITY.md content}

### Code of Conduct
Source: CODE_OF_CONDUCT.md

{Full CODE_OF_CONDUCT.md content}
```

### Content Embedding Rules

1. Each document becomes an H3 under its parent H2 section
2. Add `Source: {path}` line for attribution
3. Preserve all original markdown formatting
4. Code files wrapped in fenced code blocks with language tag
5. Binary files skipped with note: "Binary file — see source"

### Size Management

```
TARGET_MAX = 100KB

If total size > 100KB:
  1. Truncate CHANGELOG to last 3 versions (not 5)
  2. Truncate examples to first 5 files
  3. Remove Optional section content (keep links only)
  4. If STILL > 100KB: truncate longest docs to first 500 lines each
  5. Add footer: "Full documentation available at {repo_url}"
```

### CHANGELOG Truncation

```bash
# Extract last N version entries from CHANGELOG.md
# Versions detected by: ## [x.y.z] or ## x.y.z or ### [x.y.z]
# Keep everything from start of file to Nth version heading
```

## Step 5: Report

After generation, output:

```
Generated:
  llms.txt     — {entry_count} entries, {size}KB
  llms-full.txt — {doc_count} documents, {size}KB

Files included:
  - README.md (core)
  - CONTRIBUTING.md (core)
  - CHANGELOG.md (core, last 5 versions)
  - docs/api.md (API reference)
  - examples/basic.ts (example)
  ...

Size budget: {used}KB / 100KB
```

## Regeneration

When called:
- If llms.txt/llms-full.txt already exist, overwrite them
- After `/oss bump`, regenerate both files automatically
- After `/oss fix` scaffolds new docs, regenerate both files

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No README.md | Error: "README.md required. Create it first or run `/oss fix`." |
| No docs/ directory | Skip API Reference section, note in output |
| No examples/ | Skip Examples section |
| Monorepo | Generate for current package (pwd), not repo root |
| Very large docs (>50 files) | Include top 20 by directory depth (shallower = higher priority), note truncation |
| Non-markdown docs (.rst, .txt) | Include with appropriate formatting, convert .rst headings to markdown |
