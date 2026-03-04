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

Scope: full project. All 6 gates must pass.

```
LINT (changed) → TYPECHECK (full) → BUILD (full) → TEST (related) → E2E (registry) → COVERAGE (advisory)
```

Gate order rationale: cheapest/fastest first. Each catches a superset of earlier failures.

| Gate | Scope | Level | Why |
|------|-------|-------|-----|
| Lint | Changed files | BLOCKING | Fast — catches style/syntax |
| Typecheck | Full project | BLOCKING | Catches broken consumers of changed exports |
| Build | Full project | BLOCKING | Dependency graph requires full compilation |
| Test | Related tests | BLOCKING | Match changed files to their test files |
| E2E | Registry ACs | BLOCKING | Validates AC coverage via e2e-scenarios registry |
| TDD Proof | Registry status | BLOCKING | Every GREEN_CONFIRMED had prior RED_CONFIRMED |
| Coverage | Full project | ADVISORY | Warn on >5% drop or below configured threshold |

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

### E2E Framework

| Config | Framework | Run Command |
|--------|-----------|-------------|
| playwright.config.* | Playwright | npx playwright test |
| cypress.config.* / cypress/ dir | Cypress | npx cypress run |
| maestro/ dir / .maestro/ | Maestro | maestro test |
| detox.config.* | Detox | detox test |

### E2E Gate Algorithm

```
e2e_gate(registry_path):
  IF not exists(registry_path):
    IF tier in [trivial, micro]: SKIP "No registry for trivial/micro"
    ELSE: FAIL "E2E registry missing — create at ship iteration 1"

  registry = load(registry_path)

  # TDD proof: no GREEN without prior RED
  for entry in registry:
    IF entry.status == GREEN_CONFIRMED AND NOT entry.had_red:
      FAIL "TDD violation: {entry.ac} GREEN without RED"

  # All BLOCKING entries must be GREEN_CONFIRMED
  blocking = [e for e in registry if e.required == BLOCKING]
  not_green = [e for e in blocking if e.status != GREEN_CONFIRMED]
  IF not_green: FAIL "BLOCKING entries not GREEN: {not_green}"

  PASS
```

### Coverage Gate Algorithm

```
coverage_gate(threshold=null):
  IF no coverage tool detected: SKIP "No coverage tool"

  Run coverage report
  current = parse_coverage_percent()

  IF threshold AND current < threshold:
    WARN "Coverage {current}% below threshold {threshold}%"

  IF baseline exists:
    delta = current - baseline
    IF delta < -5:
      WARN "Coverage dropped {delta}% from baseline"

  PASS (advisory — never blocks)
```

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
| E2E (registry ACs) | BLOCKING | |
| TDD Proof (registry status) | BLOCKING | |
| Coverage (full project) | ADVISORY | Threshold: 70% |
```

## Escape Hatch

Skip a gate via:
1. **Config:** Set gate level to SKIP in quality-gates.md
2. **Flag:** `--skip-tests`, `--skip-review`, `--skip-e2e`
3. **Auto-detect:** No tooling found for gate (no eslint config = skip lint)
4. **User explicit:** User says "skip build" or "skip e2e" during session
5. **E2E skip:** No E2E framework detected AND user declines setup → E2E gate downgrades to ADVISORY
6. **Coverage skip:** No coverage tool configured → Coverage gate auto-SKIP

Always document skip reason in output.
