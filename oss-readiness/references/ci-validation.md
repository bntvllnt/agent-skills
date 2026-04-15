# CI Validation

CI pipeline detection, workflow analysis, and starter workflow generation for the CI-check flow (`/oss ci` or equivalent natural-language request).

## CI System Detection

```bash
# GitHub Actions (primary)
GH_WORKFLOWS=$(find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null)

# Fallback CI systems
test -f .circleci/config.yml && CI_SYSTEM="circleci"
test -f .travis.yml && CI_SYSTEM="travis"
test -f Jenkinsfile && CI_SYSTEM="jenkins"
test -f .gitlab-ci.yml && CI_SYSTEM="gitlab"
test -f bitbucket-pipelines.yml && CI_SYSTEM="bitbucket"
```

If no CI detected: report as BLOCKING failure with scaffold option.

## Workflow Analysis (GitHub Actions)

For each workflow file, grep for job types:

| Job Type | Detection Patterns | Severity |
|----------|-------------------|----------|
| Test | `npm test`, `pnpm test`, `yarn test`, `bun test`, `vitest`, `jest`, `pytest`, `cargo test`, `go test` | BLOCKING |
| Lint | `eslint`, `biome`, `prettier --check`, `clippy`, `ruff check`, `golangci-lint`, `lint` | BLOCKING |
| Build | `npm run build`, `pnpm build`, `cargo build`, `go build`, `tsc` | WARN |
| Publish | `npm publish`, `cargo publish`, `twine upload`, `goreleaser` | WARN (libraries) |
| Release automation | `changesets`, `semantic-release`, `release-please`, `auto` | WARN |

## Trigger Validation

| Trigger | Required | Why |
|---------|----------|-----|
| `on: push` or `on: pull_request` | BLOCKING | Tests must run on code changes |
| Runs on `main`/`master` branch | WARN | Should protect default branch |
| `on: release` (for publish) | WARN | Publish on release is best practice |

## Branch Protection Check

```bash
# Check if branch protection exists on default branch
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
gh api "repos/{owner}/{repo}/branches/$DEFAULT_BRANCH/protection" 2>/dev/null
# 200 = protected, 404 = not protected
```

## CI Report Format

```
CI VALIDATION — {repo}
═══════════════════════════════════════

CI System: GitHub Actions
Workflows: {count} found

┌──────────────┬──────────┬────────────────────────────────┐
│ Check        │ Status   │ Details                        │
├──────────────┼──────────┼────────────────────────────────┤
│ Tests        │ PASS     │ ci.yml: vitest run             │
│ Lint         │ PASS     │ ci.yml: biome check            │
│ Build        │ PASS     │ ci.yml: tsc --noEmit           │
│ Publish      │ FAIL     │ No publish workflow found      │
│ Triggers     │ PASS     │ push + pull_request            │
│ Branch prot. │ WARN     │ No branch protection on main   │
└──────────────┴──────────┴────────────────────────────────┘
```

## Starter Workflow Generation

When no CI exists, generate `.github/workflows/ci.yml` based on detected stack:

### Node.js (pnpm example)

```yaml
name: CI

on:
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.head_ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Quality Gates
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Lint
        run: pnpm run lint
      - name: Typecheck
        run: pnpm run check-types     # or: pnpm exec tsc --noEmit
      - name: Build
        run: pnpm run build
      - name: Test
        run: pnpm test
```

### Node.js (npm — fallback)

```yaml
name: CI

on:
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.head_ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Quality Gates
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

### Rust (Cargo)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - run: cargo fmt --check
      - run: cargo clippy -- -D warnings
      - run: cargo test
```

### Python (pip/poetry/uv)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e ".[dev]"    # adjust for your setup
      - run: ruff check .               # or: flake8, pylint
      - run: pytest                      # adjust as needed
```

### Go

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: 'stable'
      - run: go vet ./...
      - run: golangci-lint run          # install golangci-lint first
      - run: go test ./...
```

### Package Manager Detection for Workflow

```bash
# Detect package manager for Node.js projects
if [ -f pnpm-lock.yaml ]; then PM="pnpm"
elif [ -f yarn.lock ]; then PM="yarn"
elif [ -f bun.lockb ]; then PM="bun"
elif [ -f package-lock.json ]; then PM="npm"
else PM="npm"
fi
```

### Publish Workflow (Libraries Only — example pattern)

When IS_LIBRARY=true and no publish workflow exists, suggest a two-track publish:
- **Canary**: auto on push to main (version: `x.y.z-canary.{sha}`, tag: `canary`)
- **Release**: manual workflow_dispatch with version bump choice (patch/minor/major)

Both use npm OIDC provenance (no NPM_TOKEN secret needed — uses `id-token: write`).

```yaml
name: Publish

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "pnpm-lock.yaml"
      - ".github/workflows/publish.yml"
  workflow_dispatch:
    inputs:
      bump:
        description: "Version bump type"
        required: true
        type: choice
        options: [patch, minor, major]

permissions:
  contents: write
  id-token: write

jobs:
  quality:
    name: Quality Gates
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm run lint
      - run: pnpm run build
      - run: pnpm test

  canary:
    name: Publish Canary
    needs: quality
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
          registry-url: https://registry.npmjs.org
      - run: pnpm install --frozen-lockfile
      - run: pnpm run build
      - name: Upgrade npm for OIDC support
        run: npm install -g npm@latest
      - name: Publish canary
        run: |
          sed -i '/_authToken/d' "$NPM_CONFIG_USERCONFIG"
          unset NODE_AUTH_TOKEN
          BASE_VERSION=$(node -p "require('./package.json').version")
          SHORT_SHA=$(echo "$GITHUB_SHA" | cut -c1-7)
          CANARY_VERSION="${BASE_VERSION}-canary.${SHORT_SHA}"
          npm version "$CANARY_VERSION" --no-git-tag-version
          TARBALL=$(pnpm pack --pack-destination /tmp | tail -1)
          npm publish "$TARBALL" --tag canary --provenance --access public

  release:
    name: Publish Release
    needs: quality
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
          registry-url: https://registry.npmjs.org
      - run: pnpm install --frozen-lockfile
      - run: pnpm run build
      - name: Bump version
        id: version
        run: |
          npm version ${{ inputs.bump }} --no-git-tag-version
          VERSION=$(node -p "require('./package.json').version")
          echo "version=$VERSION" >> "$GITHUB_OUTPUT"
      - name: Commit and tag
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add package.json
          git commit -m "chore(release): v${{ steps.version.outputs.version }}"
          git tag -a "v${{ steps.version.outputs.version }}" -m "v${{ steps.version.outputs.version }}"
          git push origin main --follow-tags
      - name: Upgrade npm for OIDC support
        run: npm install -g npm@latest
      - name: Publish to npm
        run: |
          sed -i '/_authToken/d' "$NPM_CONFIG_USERCONFIG"
          unset NODE_AUTH_TOKEN
          TARBALL=$(pnpm pack --pack-destination /tmp | tail -1)
          npm publish "$TARBALL" --tag latest --provenance --access public
      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create "v${{ steps.version.outputs.version }}" \
            --title "v${{ steps.version.outputs.version }}" \
            --generate-notes
```

**Key patterns in this example:**
- Full OIDC/provenance flow — avoids long-lived registry secrets when the registry supports it
- `sed -i '/_authToken/d'` clears package-manager auth before `npm publish`
- `pnpm pack` → `npm publish` avoids package-manager-specific publish auth edge cases
- Canary versions: `{base}-canary.{sha7}`
- Release via `workflow_dispatch` with bump type choice
- `permissions: contents: write` + `id-token: write` cover both git push and package provenance
- `concurrency` with `cancel-in-progress` reduces duplicate CI work

## Non-GitHub CI Systems

For non-GitHub CI (CircleCI, Travis, GitLab CI), only validate existence + test/lint presence. Do not generate config — too many variations. Report:

```
CI System: {system} detected
Test job: {PASS|FAIL} — {details}
Lint job: {PASS|FAIL} — {details}

Note: Starter workflow generation only supports GitHub Actions.
For {system}, manually verify test and lint jobs exist.
```
