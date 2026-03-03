# E2E Scenario Registry

> **Agent:** Created at ship iteration 1 for specs with ACs. Validated by `done`. Archived with spec. Exempt for trivial/micro tier specs.

AC-to-test traceability with TDD proof tracking. Every Must Have + Error AC maps to an E2E test with RED → GREEN confirmation.

---

## Registry Template

| AC | Description | Test File | TDD Status | Notes |
|----|-------------|-----------|------------|-------|
| AC-1 | {AC description} | {path/to/test.spec.ts} | PENDING | |
| AC-E1 | {Error AC description} | {path/to/test.spec.ts} | RED_CONFIRMED | Fails as expected |
| FH-1 | {Failure hypothesis test} | {path/to/test.spec.ts} | GREEN_CONFIRMED | Defensive test passes |

### TDD Status Values

| Status | Meaning | Transition |
|--------|---------|------------|
| PENDING | Test not yet written | → RED_CONFIRMED (test written + fails) |
| RED_CONFIRMED | Test written, confirmed FAILING against current code | → GREEN_CONFIRMED (impl done + passes) |
| GREEN_CONFIRMED | Implementation done, test PASSING | Terminal |
| SKIP | Explicitly skipped with documented reason | Terminal |

**BLOCKING rule:** GREEN_CONFIRMED requires RED_CONFIRMED first. A test that never failed is not TDD.

### AC Types in Registry

| Prefix | Source | Required |
|--------|--------|----------|
| AC-{N} | Must Have acceptance criteria | BLOCKING |
| AC-E{N} | Error Criteria | BLOCKING |
| AC-S{N} | Should Have | Advisory |
| AC-B{N} | Bug fix ACs (B1-B4) | BLOCKING (for bug fixes) |
| FH-{N} | Failure hypothesis defensive test | BLOCKING (HIGH/MED severity) |
| EC-{N} | Edge case test | Advisory |

## Lifecycle

```
plan → spec has ACs + Error Journeys + Failure Hypotheses
  ↓
ship (iteration 1) → create e2e-scenarios.md from spec
  ↓
ship (per scope item) → write test (RED) → implement → run test (GREEN)
  ↓
ship (exit check) → validate registry: all BLOCKING entries GREEN_CONFIRMED
  ↓
done (Step 1.5) → final validation: 100% Must Have + Error AC coverage
  ↓
done (archive) → move with spec to specs/shipped/
```

### Creation (ship iteration 1)

```
For each Must Have AC      → add registry entry (PENDING)
For each Error AC          → add registry entry (PENDING)
For each HIGH/MED Failure Hypothesis → add registry entry (PENDING)
For each Error Journey     → verify AC-E covers it (no separate entry needed)
For each Edge Case         → add registry entry (PENDING, advisory)
```

### Validation Algorithm

```
validate_registry(registry):
  # 1. Unmapped check
  unmapped = [ac for ac in spec.must_have_acs + spec.error_acs
              if ac not in registry]
  IF unmapped: FAIL "ACs not in registry: {unmapped}"

  # 2. TDD proof check
  no_red = [entry for entry in registry
            if entry.status == GREEN_CONFIRMED
            and not entry.had_red_confirmed]
  IF no_red: FAIL "GREEN without RED proof: {no_red}"

  # 3. Status check (BLOCKING entries only)
  blocking = [entry for entry in registry
              if entry.required == BLOCKING]
  not_green = [e for e in blocking if e.status != GREEN_CONFIRMED]
  IF not_green: FAIL "Not all BLOCKING entries GREEN: {not_green}"

  # 4. Coverage percentage
  total_blocking = len(blocking)
  green_blocking = len([e for e in blocking if e.status == GREEN_CONFIRMED])
  coverage = green_blocking / total_blocking * 100

  IF coverage == 100: PASS
  ELSE: FAIL "{coverage}% coverage — need 100% BLOCKING"
```

## Filled Example

```markdown
# E2E Scenario Registry — User Authentication

| AC | Description | Test File | TDD Status | Notes |
|----|-------------|-----------|------------|-------|
| AC-1 | GIVEN valid credentials WHEN login THEN redirected to dashboard | tests/e2e/auth.spec.ts:12 | GREEN_CONFIRMED | |
| AC-2 | GIVEN new user WHEN signup THEN account created + welcome email | tests/e2e/auth.spec.ts:34 | GREEN_CONFIRMED | |
| AC-E1 | GIVEN invalid password WHEN login THEN error "Invalid credentials" | tests/e2e/auth.spec.ts:56 | GREEN_CONFIRMED | |
| AC-E2 | GIVEN expired session WHEN API call THEN redirect to login | tests/e2e/auth.spec.ts:78 | RED_CONFIRMED | Impl in progress |
| FH-1 | IF concurrent login attempts THEN no session corruption | tests/e2e/auth.spec.ts:90 | GREEN_CONFIRMED | Defensive test |
| EC-1 | Empty email field → validation error shown | tests/e2e/auth.spec.ts:102 | GREEN_CONFIRMED | Advisory |

**Coverage:** 5/5 BLOCKING entries GREEN_CONFIRMED (100%)
**TDD Proof:** All GREEN entries have prior RED_CONFIRMED
```

## Registry Location

Store in spec directory alongside the spec file:

```
specs/
  active/
    2024-01-15-user-auth.md           ← spec
    2024-01-15-user-auth-e2e.md       ← this registry
```

Naming: `{spec-slug}-e2e.md`

## Backward Compatibility

- Existing specs without registry: `done` Step 1.5 → WARN (advisory), not FAIL
- New specs (created after this protocol): registry is BLOCKING
- Bug fix specs: registry contains AC-B1 through AC-B4 entries

## Anti-Patterns (NEVER)

- NEVER mark GREEN_CONFIRMED without prior RED_CONFIRMED (not TDD)
- NEVER skip BLOCKING entries without documented escape hatch
- NEVER create registry without reading the spec's ACs first
- NEVER leave registry entries as PENDING at ship exit
- NEVER delete registry entries — mark SKIP with reason instead
