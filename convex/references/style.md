# Style (TSDoc + No Inline Comments)

Goals:

- Make Convex backend code self-documenting.
- Keep documentation in TSDoc, not scattered inline comments.

## Rules

- Every exported Convex function must have TSDoc.
- Every exported non-trivial type (shared across files) should have TSDoc.
- Avoid non-TSDoc comments (`//` and `/* ... */`) in backend code.
  - Exception: directive comments required by tooling (e.g. runtime directives) and ESLint disables.

## TSDoc Template

```ts
/**
 * One-line summary of what this function does.
 *
 * Preconditions:
 * - Authentication required (or not)
 * - Any invariants
 *
 * @param ctx - Convex context
 * @param args - Validated input
 * @returns Validated output
 */
```

## File organization (recommended)

Within a scope folder:

```text
convex/<scope>/
  queries.ts
  mutations.ts
  actions.ts
  workflows.ts
  crons.ts
  schemas.ts
  helpers.ts
  tests/
```
