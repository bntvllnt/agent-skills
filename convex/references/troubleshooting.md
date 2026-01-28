# Troubleshooting & Self-Correction

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

Docs:

- Functions: https://docs.convex.dev/functions
- Error handling: https://docs.convex.dev/functions/error-handling
- Debugging: https://docs.convex.dev/functions/debugging
