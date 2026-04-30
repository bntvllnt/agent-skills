# Supply Chain

Dependencies — direct, transitive, and the build pipeline that fetches them. Loaded on supply-chain-related queries or as part of full audit.

## Threat Categories

| Category | Description | Example |
|----------|-------------|---------|
| Known CVE | Dep version has documented vuln | event-stream / left-pad-style |
| Typo-squat | Malicious lookalike of popular dep | `lodahs` vs `lodash` |
| Maintainer compromise | Legit dep, account taken | ua-parser-js 2021 |
| Transitive | Direct dep is fine, transitive is not | `lodash@4.17.20` via deep tree |
| Install scripts | postinstall runs malicious code | shell.js / node-ipc |
| Vendor-binary | Repo includes compiled binary, no source | random `tools/scanner.exe` |
| Lockfile drift | lockfile not committed or out of sync | yarn.lock missing |
| Registry confusion | private + public package conflict | dependency confusion (Birsan 2021) |

## Tools (use if installed)

```bash
# JS / TS
npm audit --json
pnpm audit --json
yarn audit --json

# Universal (cross-language CVE)
osv-scanner --json .
osv-scanner --lockfile=package-lock.json

# Python
pip-audit --format json
safety check --json

# Go
govulncheck ./...

# Rust
cargo audit --json

# Snyk
snyk test --json

# OSSF Scorecard (project health)
scorecard --repo=github.com/owner/repo
```

## Manual Audit (when no tooling)

### 1. Lockfile Present?

```
Glob: "package-lock.json|pnpm-lock.yaml|yarn.lock|Cargo.lock|go.sum|poetry.lock|Pipfile.lock"
```

No lockfile = no reproducible install = supply chain vulnerability.

### 2. Lockfile Drift

For Node:

```bash
# Tree should match lockfile
npm ls               # warns on drift
pnpm install --frozen-lockfile  # in CI; fails on drift
```

If CI doesn't use `--frozen-lockfile` (or equivalent), commits can introduce undeclared deps.

### 3. Postinstall / Preinstall Scripts

```
Read: package.json → scripts.{preinstall, postinstall, prepare, prepublish}
```

For each, verify it does what it claims. Common red flags:
- Downloads binaries from arbitrary URLs.
- Runs `curl | sh`.
- Touches files outside the package dir.

For deps:

```bash
npm pack <dep>  # extract and inspect
# or
node -e "console.log(require('./node_modules/<dep>/package.json').scripts)"
```

### 4. Deep Tree Inspection

```bash
# JS
npm ls --all --json > tree.json
npm fund   # who maintains what

# Python
pipdeptree --json > tree.json
```

Look for:
- Unexpectedly deep transitive trees (one direct dep pulling 200 transitives).
- Recently updated transitives with low download counts (typo-squat candidates).
- Deps with single-maintainer / abandoned status.

### 5. Typo-Squat / Lookalike

```
Read: package.json → dependencies, devDependencies
```

For each name:
- Search npm: are there packages with very similar names?
- Compare download counts: legitimate package has orders of magnitude more.
- Check publish date: typo-squats are recent.

### 6. Vendored Binaries

```
Glob: "vendor/**, third-party/**, tools/**, scripts/**.{exe,bin,dll,so,dylib}"
```

Any binary in the repo without source + build step is a black box. Flag it.

### 7. Fetched-at-build

```
Grep in CI / build scripts: "curl|wget|fetch|invoke-webrequest"
```

Anything fetched during build should be:
- HTTPS only.
- Pinned to a hash / signed release (not `latest` / `master`).
- From a known origin (GitHub releases, official CDN).

## Dependency Confusion Check

If your project uses both public (npm.org) and private (artifactory / verdaccio) registries:

```
Read: .npmrc, .yarnrc, package.json (publishConfig)
```

Risk: an attacker publishes a package on the public registry with the **same name** as your private one. If the registry-routing is wrong, the public (malicious) version is installed.

Mitigation:
- Scope private packages: `@yourorg/xyz`.
- Pin scopes to private registry in `.npmrc`: `@yourorg:registry=https://your-registry`.
- Reserve the unscoped name on the public registry as a placeholder.

## Output Template

```markdown
## Supply Chain Audit

### Tooling Run
- npm audit: X CVEs (Y high, Z critical)
- osv-scanner: X CVEs
- (or: NO TOOLING — manual review only)

### Direct Dep Health
| Dep | Version | CVEs | Maintenance | Action |
|-----|---------|------|-------------|--------|
| ... | ... | ... | active / abandoned | upgrade / replace / accept |

### Transitive Risks
| Dep (path) | CVE | Severity | Reachable from your code? |
|------------|-----|----------|---------------------------|
| ... | ... | ... | yes / no / unknown |

### Install-Script Risks
| Dep | Script | Action | Verdict |
|-----|--------|--------|---------|
| ... | postinstall | curl... | reject |

### Lockfile Status
- Committed: yes / no
- CI uses frozen install: yes / no
- Drift: yes / no

### Typo-Squat / Lookalike
| Suspect | Real | Verdict |
|---------|------|---------|

### Vendored Binaries
| Path | Origin | Audited? |
|------|--------|----------|

### Recommended Actions
- [ ] Upgrade [dep] to [version] (fixes CVE-XXXX)
- [ ] Replace [abandoned dep] with [maintained alternative]
- [ ] Add `npm ci` / `pnpm install --frozen-lockfile` to CI
- [ ] Add osv-scanner / npm audit to CI as blocking step
- [ ] Scope private deps under @yourorg
```

## Anti-Patterns (NEVER)

- NEVER `npm install` in production builds — use `npm ci` against committed lockfile.
- NEVER use `latest` tags in package.json or container images.
- NEVER `curl | sh` in install / build scripts.
- NEVER vendor binaries without a source + build trail.
- NEVER ignore CVE alerts on the assumption "we don't use that path" — transitive bugs are reachable in surprising ways.
