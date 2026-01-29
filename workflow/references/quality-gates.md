# Quality Gates

> **Agent:** Load this file when `ship` runs quality gates. Also referenced by `done` for full validation.

Two-pass validation. No task complete until full pass green.

## Quick Pass (After Each Edit Batch)

Scope: changed files only. Run after each logical unit of edits.

```
Changed files → LINT → TYPECHECK → pass? → continue coding
                 ↓ fail   ↓ fail
                FIX       FIX (max 3 attempts → escalate)
```

## Full Pass (Before Task Complete — BLOCKING)

Scope: full project. All 4 gates must pass.

```
LINT (changed) → TYPECHECK (full) → BUILD (full) → TEST (related)
```

Gate order rationale: cheapest/fastest first. Each catches a superset of earlier failures.

| Gate | Scope | Why |
|------|-------|-----|
| Lint | Changed files | Fast — catches style/syntax |
| Typecheck | Full project | Catches broken consumers of changed exports |
| Build | Full project | Dependency graph requires full compilation |
| Test | Related tests | Match changed files to their test files |

## Stack Auto-Detection

Detect tooling from project files. Never hardcode commands.

### Package Manager

| Lockfile | Manager |
|----------|---------|
| pnpm-lock.yaml | pnpm |
| yarn.lock | yarn |
| bun.lockb | bun |
| package-lock.json | npm |

### Lint Tool

| Config | Tool |
|--------|------|
| biome.json / biome.jsonc | biome check |
| .eslintrc* / eslint.config.* | eslint |
| deno.json | deno lint |
| ruff.toml / pyproject.toml (ruff) | ruff check |
| .golangci.yml | golangci-lint run |
| .rubocop.yml | rubocop |
| phpcs.xml / .php-cs-fixer.php | phpcs / php-cs-fixer |
| .swiftlint.yml | swiftlint |
| detekt.yml / .editorconfig (ktlint) | detekt / ktlint |

### Build Tool

| Config | Tool |
|--------|------|
| package.json (scripts.build) | {pkg-manager} run build |
| build.gradle / build.gradle.kts | gradle build |
| pom.xml | mvn compile |
| *.csproj / *.sln | dotnet build |
| Makefile | make |
| Cargo.toml | cargo build |
| Package.swift | swift build |
| mix.exs | mix compile |
| Gemfile + Rakefile | bundle exec rake build |
| composer.json | composer build (if script exists) |

### Test Runner

| Config | Runner |
|--------|--------|
| vitest.config.* | vitest run |
| jest.config.* | jest |
| pytest.ini / pyproject.toml (pytest) | pytest |
| *_test.go | go test ./... |
| Cargo.toml | cargo test |
| build.gradle / build.gradle.kts | gradle test |
| pom.xml | mvn test |
| *.csproj (with test projects) | dotnet test |
| Package.swift | swift test |
| mix.exs | mix test |
| Gemfile | bundle exec rspec / bundle exec rake test |
| composer.json | composer test / phpunit |

### Typecheck

| Stack | Command |
|-------|---------|
| TypeScript | tsc --noEmit |
| Python (typed) | mypy / pyright |
| Java / Kotlin | (covered by build — compiler checks types) |
| C# | (covered by dotnet build) |
| Go | (covered by go build / go vet) |

## Fix Loop Protocol

Per gate, on failure:
1. Read error output
2. Fix the issue
3. Re-run same gate
4. Max 3 attempts → escalate to user with error output

## Gate Levels

All gates support three levels (edit this file to change):

| Level | Behavior |
|-------|----------|
| BLOCKING | Must pass. Failure stops progress. |
| ADVISORY | Warn on failure. Continue allowed. |
| SKIP | Don't run this gate at all. |

Default: all built-in gates are BLOCKING. Override in config:

```markdown
### Quality Gates (Full Pass)

| Gate | Level | Command Override |
|------|-------|-----------------|
| Lint (changed files) | BLOCKING | |
| Typecheck (full project) | SKIP | No TypeScript |
| Build (full project) | BLOCKING | |
| Test (related tests) | ADVISORY | Tests are flaky, fixing next sprint |
```

## Escape Hatch

Skip a gate via:
1. **Config:** Set gate level to SKIP in quality-gates.md
2. **Flag:** `--skip-tests`, `--skip-review`
3. **Auto-detect:** No tooling found for gate (no eslint config = skip lint)
4. **User explicit:** User says "skip build" during session

Always document skip reason in output.
