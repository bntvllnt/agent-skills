# Troubleshooting & Self-Correction

For deep performance diagnosis, see `references/performance.md`.

## If query performance is slow

1. Check: `.filter()` used instead of `.withIndex()`?
2. Fix: add an index in schema and rewrite query with `.withIndex()`.
3. Validate: run the query and inspect logs.

## If type errors on returns

1. Check: does the document validator include `_id` and `_creationTime`?
2. Fix: use dual validator pattern (data + document).

## If auth check fails

1. Check: `ctx.auth.getUserIdentity()` returns null?
2. Fix: ensure your auth integration is configured; verify identity subject mapping.

## If scheduled function errors

1. Check: scheduler references `api.*` instead of `internal.*`?
2. Fix: schedule `internal.*` functions.

## If action fails with "Operation not permitted"

1. Check: missing runtime directive?
2. Fix: follow the official "runtimes" doc and ensure your action is in the correct runtime.

## If TypeScript fails with TS2589 / FilterApi depth errors

Symptom:

- `TS2589: Type instantiation is excessively deep and possibly infinite`
- usually triggered from `api`, `internal`, `_generated/api`, or `_generated/server`

Root cause chain:

```text
convex/ has N .ts/.js files
  -> codegen includes all N in fullApi
  -> FilterApi<fullApi, "public" | "internal"> recurses across every module
  -> importing api/internal forces deep type resolution
  -> around 350+ modules, TypeScript can exceed its recursion budget
```

Check first:

```bash
grep -c '  "' convex/_generated/api.d.ts
```

Interpretation:

- `> 330`: approaching the danger zone
- `> 350`: likely FilterApi depth failure territory

Preferred fixes, in order:

1. Reduce `convex/` module count. Move utility-only `helpers.ts`, `validators.ts`, `types.ts`, `schemas.ts`, and `constants.ts` into `src/` or merge them into real function files.
2. Stop splitting one logical scope into many tiny files inside `convex/`.
3. Replace deep generated builders with `queryGeneric`, `mutationGeneric`, `actionGeneric`, `internalQueryGeneric`, `internalMutationGeneric`, or `internalActionGeneric` from `convex/server` when the generated `DataModel` chain is the problem.
4. For config-only or bridge files that do not need TypeScript checking, consider `.js` as an intentional escape hatch if the repo accepts it.
5. For thin bridge layers that only proxy `internal.*` calls, use a clearly documented type cut point (`any` / targeted lint disable) if needed to break the recursive chain.

Anti-patterns to flag immediately:

- utility-only files living inside `convex/`
- adding new files under `convex/` that export zero Convex functions
- large `v.union()` literals or deeply nested validators in files that also import `internal` or `api`
- registering another component with `app.use(...)` when the module count is already near the threshold

Docs:

- Functions: https://docs.convex.dev/functions
- Error handling: https://docs.convex.dev/functions/error-handling
- Debugging: https://docs.convex.dev/functions/debugging
