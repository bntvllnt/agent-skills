# Testing Patterns

Docs:

- Overview: https://docs.convex.dev/testing
- convex-test: https://docs.convex.dev/testing/convex-test
- Run functions from CLI (manual tests): https://docs.convex.dev/cli#run-convex-functions

## Co-located Tests (Preferred)

Keep tests close to the functions they validate:

```text
convex/<scope>/tests/
```

## Naming Convention (Suggested)

Use a clear, scoped naming pattern:

```text
<scope>.<type>.<case>.test.ts
```

Examples:

```text
categories.mutations.create.test.ts
auth.queries.listAvatars.test.ts
wordzic.workflows.lifecycle.test.ts
```

## Strategies

Pick one per repo (or clearly separate them):

1) `convex-test` unit/integration tests in JS (fast, isolated)
2) End-to-end tests against a live dev deployment (slower, higher confidence)

## Live Deployment Tests (Pattern)

If you test against a live dev deployment:

- Keep tests under `convex/<scope>/tests/`.
- Use a shared test harness to call functions (HTTP/WebSocket client) and to seed fixtures.
- Run tests serially if the suite mutates shared tables.
- Add `test_support` helpers when you need to exercise internal functions from tests.

## Rules

- Test auth paths: authenticated and unauthenticated.
- Keep reads bounded (`take`/pagination) to avoid flaky timeouts.
- Prefer index-backed queries and assert shape and ordering.
- Enforce TSDoc on exported functions and avoid non-TSDoc comments.
