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

## File Organization (Enforced by @vllnt/eslint-config)

Namespace separation: each function type MUST live in its designated file. This is enforced by `convex-rules/standard-filenames` and `convex-rules/namespace-separation`.

```text
convex/<scope>/
  queries.ts              query(), internalQuery()
  mutations.ts            mutation(), internalMutation()
  internal_mutations.ts   internalMutation() (optional split)
  actions.ts              action(), internalAction()
  validators.ts           v.* validators + types
  schema.ts               table definitions
  workflows.ts
  crons.ts
  tests/
```

### Naming Rules

- **snake_case filenames** in `convex/` (enforced by `convex-rules/snake-case-filenames`). Example: `user_helper.ts`, not `user-helper.ts`.
- Config files exempt: `auth.ts`, `auth.config.ts`, `convex.config.ts`.
- Migration files exempt from namespace separation.

### Namespace Rules

- `query()` / `internalQuery()` ONLY in `queries.ts`
- `mutation()` / `internalMutation()` ONLY in `mutations.ts` or `internal_mutations.ts`
- `action()` / `internalAction()` ONLY in `actions.ts`

### Validator Rules

- No bare `v.any()` outside `validators.ts` (enforced by `convex-rules/no-bare-v-any`). Define named aliases instead:

```ts
// validators.ts
export const IdInput = v.any();

// queries.ts -- use the alias
import { IdInput } from "./validators";
export const myQuery = query({
  args: { id: IdInput },
  handler: async (ctx, args) => { /* ... */ },
});
```
