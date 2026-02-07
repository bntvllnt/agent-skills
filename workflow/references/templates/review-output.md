# Review Output Template

Edit this file to customize what the agent returns after `review`. Decision logic: [actions/review.md](../actions/review.md).

---

## Change Overview (ALWAYS FIRST)

Before findings, show the change map from Step 1 of review.md:

```markdown
## Change Overview

| File | Category | Risk | Language |
|------|----------|------|----------|
| src/api/auth.ts | auth/security | HIGH | TypeScript |
| src/lib/utils.ts | internal logic | LOW | TypeScript |

**Mode:** {MODE} — {reason}
**Language:** {language} | **Framework:** {framework}
```

Rules:
- Always show the change map table before any findings
- State selected mode and reason on its own line
- State detected language and framework

---

## Per-File Findings

For each file with findings, list issues with location:

```
{file_path}:{line} — {FAIL|WARN} [{perspective}] {one-line description}
  Fix: {concrete action to take}
```

Rules:
- One line per issue — description + fix on next line
- Always include file path and line number
- Always include a concrete fix (not just "consider improving")
- FAIL = must fix. WARN = should fix. BLOCKS_PRODUCTION = violates production bar (Production mode only).
- Skip PASS items — only show what needs action
- Group by file, not by perspective

---

## Review Summary

After all per-file findings:

```markdown
## Review: {N} files checked

**FAIL ({N})** — must fix before shipping:
1. `{file}:{line}` — [{perspective}] {description}
2. `{file}:{line}` — [{perspective}] {description}

**WARN ({N})** — should fix:
1. `{file}:{line}` — [{perspective}] {description} (severity)
2. `{file}:{line}` — [{perspective}] {description} (severity)

**Verdict:** {CLEAN / HAS_BLOCKERS / WARNINGS_ONLY}
```

---

## Output Rules

- **Actionable only** — every finding has a Fix line. No vague "could be improved".
- **File:line always** — user must be able to jump to the exact location.
- **No noise** — skip PASS items entirely. Only show what needs action.
- **Flat list** — no nested sections per perspective. One flat list sorted by severity (FAIL first, then WARN).
- **Concrete fixes** — "Add `await` before `db.save()`" not "Consider handling async properly".
- **Short** — one line per issue. Description ≤ 80 chars. Fix ≤ 80 chars.
- **Verdict at the end** — CLEAN (0 FAIL, 0 WARN), WARNINGS_ONLY (0 FAIL, N WARN), HAS_BLOCKERS (N FAIL).

---

## Production Mode Output

When Production mode is active, additional format rules apply:

### BLOCKS_PRODUCTION Severity

Above FAIL. Format:

```
{file}:{line} — BLOCKS_PRODUCTION [{perspective}] {description}
  Fix: {concrete action}
  Standard: {Company} — {rule violated}
```

The `Standard:` line cites which company bar and specific rule was violated (e.g., `Standard: Google — No bare console.log, use structured logging`).

### Production Verdict

Replace standard verdict with production-specific:

```markdown
**Production Verdict:** {PRODUCTION_READY / NOT_PRODUCTION_READY / WARNINGS_ONLY}
```

- `PRODUCTION_READY` — 0 BLOCKS_PRODUCTION, 0 FAIL, 0 WARN
- `NOT_PRODUCTION_READY` — any BLOCKS_PRODUCTION or FAIL exists
- `WARNINGS_ONLY` — 0 BLOCKS_PRODUCTION, 0 FAIL, N WARN

### Severity Order

```
BLOCKS_PRODUCTION > FAIL > WARN
```

Sort all findings by this order. BLOCKS_PRODUCTION items listed first.

---

## Example

```
## Review: 3 files checked

src/middleware/auth.ts:42 — FAIL [Security] JWT secret read from env without fallback
  Fix: Add validation: `if (!secret) throw new Error("JWT_SECRET required")`

src/routes/users.ts:18 — FAIL [Correctness] Missing await on async db.save()
  Fix: Add `await` before `db.save(user)`

src/routes/users.ts:31 — WARN [Performance] N+1 query in user list (medium)
  Fix: Replace loop with `db.users.findMany({ where: { id: { in: ids } } })`

src/utils/format.ts:7 — WARN [DX] Function name `fn` is not descriptive (low)
  Fix: Rename to `formatUserDisplayName`

**FAIL (2)** — must fix before shipping:
1. `src/middleware/auth.ts:42` — [Security] JWT secret without fallback
2. `src/routes/users.ts:18` — [Correctness] Missing await on db.save()

**WARN (2)** — should fix:
1. `src/routes/users.ts:31` — [Performance] N+1 query (medium)
2. `src/utils/format.ts:7` — [DX] Non-descriptive function name (low)

**Verdict:** HAS_BLOCKERS
```
