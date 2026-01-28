# Authentication Patterns

Docs:

- Authentication overview: https://docs.convex.dev/auth
- Accessing auth in functions: https://docs.convex.dev/auth/functions-auth

## Core Rules

- User identity comes from `ctx.auth.getUserIdentity()`, not from args.
- If you persist users, map identity subject -> `users` table via an index.

## Wrapper Pattern (Recommended)

If you use wrappers, keep them small and explicit.

Example using `convex-helpers` custom functions:

```ts
import { v } from "convex/values";
import { ConvexError } from "convex/values";
import { customCtx, customQuery, customMutation } from "convex-helpers/server/customFunctions";
import { query, mutation } from "../_generated/server";

export const guestTokenArg = { guestToken: v.optional(v.string()) };

export const authQuery = customQuery(
  query,
  customCtx(async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new ConvexError({ code: "UNAUTHORIZED" });

    const user = await ctx.db
      .query("users")
      .withIndex("by_subject", (q) => q.eq("subject", identity.subject))
      .unique();
    if (!user) throw new ConvexError({ code: "USER_NOT_FOUND" });

    return { user };
  })
);

export const authMutation = customMutation(
  mutation,
  customCtx(async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new ConvexError({ code: "UNAUTHORIZED" });

    const user = await ctx.db
      .query("users")
      .withIndex("by_subject", (q) => q.eq("subject", identity.subject))
      .unique();
    if (!user) throw new ConvexError({ code: "USER_NOT_FOUND" });

    return { user };
  })
);
```

## Notes

- Keep auth checks at the top of public functions.
- If you support guests, treat guest tokens as optional and resolve them via an indexed lookup.
