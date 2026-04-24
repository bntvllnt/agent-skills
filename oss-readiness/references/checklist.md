# OSS Readiness Checklist

Detection logic, fix actions, and README quality sub-checks for all 23 items.

## Placeholder Policy

Scaffolded files must stay portable:

- Use placeholders such as `{PROJECT_REPO_URL}`, `{COMMUNITY_SUPPORT_URL}`, `{SECURITY_REPORTING_URL}`, `{CODE_OF_CONDUCT_CONTACT}`, and `{MAINTAINER_CONTACT_URL}` until the target repo provides real values.
- Do not hardcode maintainer links, social handles, org names, or inboxes from this skill repository.
- Prefer an explicitly provided private security channel. If none exists, leave a placeholder and flag it for maintainer input.

## Visibility-Aware GitHub Metadata Checks

When a repo is intentionally private or `gh` is unavailable/auth missing, GitHub-hosted metadata checks should become `MANUAL` instead of `FAIL`:

- item 9: GitHub description
- item 13: GitHub topics/tags
- optional branch-protection checks in CI validation

`MANUAL` and `N/A` items are excluded from score denominators. Use them for staged private repos that are not ready to expose public metadata yet.

## BLOCKING Items (12)

For each item, provide: detection command, pass/fail criteria, and fix action.

### 1. LICENSE
- Detection: `test -f LICENSE -o -f LICENSE.md -o -f LICENSE.txt`
- Pass: file exists and is non-empty
- Fix: ask user for license type (MIT, Apache-2.0, ISC, GPL-3.0, BSD-3-Clause). Never default.

### 2. README.md Exists
- Detection: `test -f README.md && test -s README.md`
- Pass: file exists and >100 bytes
- Fix: scaffold from `templates/README.md`.

### 3. README.md Quality
Sub-checks (parse README.md content):

| Section | Detection Pattern | Required |
|---|---|---|
| Title (H1) | `^# ` at start of file | BLOCKING |
| Description | Paragraph after H1, >20 chars | BLOCKING |
| Installation | `## Install` or `## Getting Started` or install command/code block | BLOCKING |
| Usage | `## Usage` or `## Quick Start` or runnable examples | BLOCKING |
| License section | `## License` or link to LICENSE file | BLOCKING |
| API/Reference | `## API` or `## Reference` or link to docs | WARN |
| Contributing link | `CONTRIBUTING` anywhere | WARN |
| Badges | `![` or `shields.io` or badge URL patterns | WARN |

### 4. CONTRIBUTING.md
- Detection: `test -f CONTRIBUTING.md`
- Pass: file exists and >100 bytes
- Fix: scaffold from `templates/CONTRIBUTING.md`, fill placeholders.

### 5. .gitignore
- Detection: `test -f .gitignore`
- Pass: file exists
- Fix: generate stack-appropriate ignores (`node_modules`, `dist`, `.venv`, `.env*`, target artifacts, etc.).

### 6. No Secrets in Repo
- Detection:
  ```bash
  git ls-files | grep -E '\.env$|\.env\.' | grep -v '.env.example'
  git grep -l -E '(AKIA|sk-|ghp_|gho_|github_pat_|xox[bpas]-|Bearer [A-Za-z0-9])'
  git ls-files | grep -E '\.pem$|\.key$|id_rsa'
  ```
- Pass: all three return empty
- Fix: list offending files, suggest `.gitignore` updates, warn if history cleanup is required.

### 7. CI: Tests Run
- Detection:
  ```bash
  grep -rl -E 'npm test|pnpm test|yarn test|vitest|jest|pytest|cargo test|go test|bun test' .github/workflows/ 2>/dev/null
  ```
- Also check fallback CI files: `.circleci/config.yml`, `.travis.yml`, `.gitlab-ci.yml`, `Jenkinsfile`
- Pass: at least one workflow contains a test command
- Fix: generate starter CI workflow from `references/ci-validation.md`.

### 8. CI: Lint Runs
- Detection:
  ```bash
  grep -rl -E 'eslint|biome|prettier --check|clippy|ruff check|golangci|lint' .github/workflows/ 2>/dev/null
  ```
- Pass: at least one workflow contains a lint command
- Fix: add lint step to existing CI workflow or generate a new one.

### 9. GitHub Description Set
- Detection: `gh repo view --json isPrivate,description`
- Pass: non-empty description when the repo is public or explicitly being prepared to go public
- Manual: repo is intentionally private for now, or `gh` is unavailable/auth missing
- Fix: suggest description from package metadata or README first paragraph, then apply with `gh repo edit --description "..."` when the maintainer wants to stage the public repo metadata.

### 10. CHANGELOG.md
- Detection: `test -f CHANGELOG.md && grep -qE '## \[?[0-9]+\.[0-9]+' CHANGELOG.md`
- Pass: file exists and contains at least one version heading
- Fix: scaffold initial CHANGELOG from tags and commit history.

### 11. llms.txt
- Detection: `test -f llms.txt`
- Pass: file exists and follows the expected H1 + link-list format
- Fix: route to llms generation flow.

### 12. llms-full.txt
- Detection: `test -f llms-full.txt`
- Pass: file exists and is non-empty (>1KB is a good heuristic)
- Fix: route to llms generation flow.

## WARN Items (11)

### 13. GitHub Topics/Tags
- Detection: `gh repo view --json isPrivate,repositoryTopics`
- Pass: at least 3 topics set when the repo is public or explicitly being prepared to go public
- Manual: repo is intentionally private for now, or `gh` is unavailable/auth missing
- Fix: suggest topics from package keywords, language, framework, and repo purpose, then apply them when the repo is ready for public discovery.

### 14. AGENTS.md
- Detection: `test -f AGENTS.md`
- Pass: file exists and >200 bytes
- Fix: scaffold from `templates/AGENTS.md`. Treat it as the canonical agent-instructions file.

### 15. Harness-Specific Agent-Instruction Aliases
- Detection:
  ```bash
  find . -maxdepth 2 \( \
    -name 'CLAUDE.md' -o \
    -name '.cursorrules' -o \
    -name '.windsurfrules' -o \
    -name 'codex.md' -o \
    -path './.opencode/config' -o \
    -name '.aider.conf.yml' \
  \) | head -1
  ```
- Pass: at least one alias/mirror exists for the canonical `AGENTS.md`
- Fix: ask which harnesses need aliases, then symlink/copy from `AGENTS.md` when supported.
- Note: this is optional. `AGENTS.md`-only repos are still valid; this item improves discoverability across harnesses.

### 16. SECURITY.md
- Detection: `test -f SECURITY.md || test -f .github/SECURITY.md`
- Pass: file exists
- Fix: scaffold from `templates/SECURITY.md` with real/private reporting channel placeholders.

### 17. CODE_OF_CONDUCT.md
- Detection: `test -f CODE_OF_CONDUCT.md`
- Pass: file exists
- Fix: scaffold Contributor Covenant v2.1 from `templates/CODE_OF_CONDUCT.md`.

### 18. Issue Templates
- Detection: `test -d .github/ISSUE_TEMPLATE && ls .github/ISSUE_TEMPLATE/*.yml 2>/dev/null | wc -l`
- Pass: directory exists with at least 1 YAML form
- Fix: scaffold `bug_report.yml`, `feature_request.yml`, and `config.yml` from `templates/issue-template-bug.md`, `templates/issue-template-feature.md`, and `templates/issue-template-config.yml`.

### 19. PR Template
- Detection: `test -f .github/pull_request_template.md`
- Pass: file exists
- Fix: scaffold from `templates/pr-template.md`.

### 20. CI: Publish Workflow (libraries only)
- Detection: only check when the repo looks like a publishable library.
  ```bash
  grep -rl -E 'npm publish|cargo publish|twine upload|goreleaser|semantic-release|changesets' .github/workflows/ 2>/dev/null
  ```
- Pass: at least one publish workflow found (or repo is not a library)
- Fix: suggest or scaffold a release workflow. See `references/ci-validation.md`.

### 21. docs/ Folder
- Detection: `test -d docs && find docs -name "*.md" -type f | head -1`
- Pass: directory exists with at least one Markdown file
- Fix: `mkdir -p docs` and suggest an initial docs structure.

### 22. Version and Release Metadata in Docs Match Package
- Detection: compare manifest/tag version against `README.md`, `docs/**`, `llms.txt`, `llms-full.txt`, `AGENTS.md`, and known alias files.
- Also compare public install/publish statements against the actual package metadata and release workflow. Check for mismatches such as:
  - README says GitHub Packages while `publishConfig.registry` or publish CI targets npm
  - docs point at an old public docs domain while the deployed homepage/workflow uses a new one
  - package install instructions disagree with the real published package name or registry URLs
- Pass: no stale version references or public release/install metadata mismatches found
- Fix: route to version-sync flow and update stale version strings plus package-name, registry, homepage/docs-domain, and release-url guidance so docs match the real package metadata and CI workflows.

### 23. No TODO/FIXME in Public src/
- Detection:
  ```bash
  grep -rn -E '(TODO|FIXME|HACK|XXX|TEMP)' src/ lib/ --include='*.ts' --include='*.js' --include='*.rs' --include='*.py' --include='*.go' 2>/dev/null | head -20
  ```
- Pass: zero matches (or no public source tree exists)
- Fix: list locations and suggest resolving or moving to issues.

## Scaffold Order

When the fix flow is invoked, scaffold in this order:

```text
1. .gitignore (first — helps prevent accidental secret commits)
2. LICENSE (ask user for type)
3. README.md
4. CONTRIBUTING.md
5. CODE_OF_CONDUCT.md
6. SECURITY.md
7. AGENTS.md (canonical instructions file)
8. Optional harness aliases for AGENTS.md
9. CHANGELOG.md
10. .github/ISSUE_TEMPLATE/ (`bug_report.yml`, `feature_request.yml`, `config.yml`)
11. .github/pull_request_template.md
12. .github/workflows/ci.yml (if no CI exists)
13. llms.txt + llms-full.txt (last — after docs exist)
```

## Scoring Algorithm

```python
blocking_items_scored = blocking items with status not in {MANUAL, N/A}
blocking_total = count(blocking_items_scored)
blocking_pass = count(blocking items with status == PASS)
warn_items_scored = warn items with status not in {MANUAL, N/A}
warn_total = count(warn_items_scored)
warn_pass = count(warn items with status == PASS)

score = (blocking_pass / blocking_total) * 70 + (warn_pass / warn_total) * 30

if blocking_pass == blocking_total:
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    else:
        grade = "C"
else:
    if score >= 60:
        grade = "C"
    elif score >= 40:
        grade = "D"
    else:
        grade = "F"
```