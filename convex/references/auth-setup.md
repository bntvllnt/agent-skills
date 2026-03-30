# Auth Setup

Docs:

- Authentication overview: https://docs.convex.dev/auth
- Auth in functions: https://docs.convex.dev/auth/functions-auth
- Storing users: https://docs.convex.dev/auth/database-auth

Skip when: auth for a non-Convex backend, pure OAuth/OIDC docs, or auth provider is already fully configured.

## Step 1: Choose the Provider

Do not assume a provider. Before writing setup code:

1. Check the repo for signals:
   - Dependencies: `@convex-dev/auth`, `better-auth`, `@convex-dev/better-auth`
   - Files: `convex/auth.config.ts`, `convex/betterAuth/`, auth middleware, provider wrappers
   - Env vars pointing at a provider (e.g. `BETTER_AUTH_SECRET`)
2. If obvious from repo, continue with that provider
3. If not obvious, ask the user

### Options

| Provider | When to Use | Reference |
|----------|-------------|-----------|
| Convex Auth | Built-in Convex auth: magic links, OTPs, OAuth, passwords | `auth-providers/convex-auth.md` |
| Better Auth | Framework-agnostic auth with plugin ecosystem, runs on Convex infra | `auth-providers/better-auth.md` |
| Custom JWT | Integrating existing auth system not covered above | [Official docs](https://docs.convex.dev/auth) |

## Step 2: Read Provider Reference

After choosing, read exactly one provider reference file. Each contains:

- Concrete setup steps
- Expected files and env vars
- Gotchas specific to that provider
- Validation checklist

## Core Pattern: Protecting Backend Functions

The most common auth task: checking identity in Convex functions.

```ts
// Bad: trusting client-provided userId
export const getMyProfile = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});
```

```ts
// Good: verifying identity server-side
export const getMyProfile = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    return await ctx.db
      .query("users")
      .withIndex("by_tokenIdentifier", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();
  },
});
```

## Shared Auth Behavior (All Providers)

Use official Convex docs as source of truth for:

- `ctx.auth.getUserIdentity()` usage
- Optional app-level user storage (not every app needs a `users` table)
- Authorization patterns (ownership, roles, team access)
- Convex Auth authorization: https://labs.convex.dev/auth/authz

## Workflow

1. Determine provider (ask or infer from repo)
2. Ask: local-only setup or production-ready?
3. Read matching provider reference file
4. Follow official provider docs for current setup details
5. Follow official Convex docs for shared auth behavior
6. Only add app-level user storage if the app actually needs it
7. Add authorization checks where the app needs them
8. Verify login state, protected queries, env vars
9. If blocked on interactive setup, ask the user for that exact step

## Checklist

- [ ] Chosen correct auth provider before writing code
- [ ] Read the relevant provider reference file
- [ ] Asked local-only or production-ready
- [ ] Used official provider docs for wiring
- [ ] Used official Convex docs for shared auth behavior
- [ ] Only added user storage if actually needed
- [ ] Auth checks in protected backend functions
- [ ] Authorization checks where app needs them
- [ ] Client auth provider configured
- [ ] If requested, production setup covered
