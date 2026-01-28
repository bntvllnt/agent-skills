# Function Templates

Docs:

- Functions overview: https://docs.convex.dev/functions
- Queries: https://docs.convex.dev/functions/query-functions
- Mutations: https://docs.convex.dev/functions/mutation-functions
- Actions: https://docs.convex.dev/functions/actions
- HTTP actions: https://docs.convex.dev/functions/http-actions
- Internal functions: https://docs.convex.dev/functions/internal-functions
- Validation: https://docs.convex.dev/functions/validation
- Runtimes: https://docs.convex.dev/functions/runtimes

## Query with Returns Validator

```ts
import { query } from "../_generated/server";
import { v } from "convex/values";
import { itemDocValidator } from "./schemas";

export const get = query({
  args: { id: v.id("items") },
  returns: v.union(itemDocValidator, v.null()),
  handler: async (ctx, args) => {
    return await ctx.db.get("items", args.id);
  },
});

export const list = query({
  args: { userId: v.id("users"), limit: v.optional(v.number()) },
  returns: v.array(itemDocValidator),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("items")
      .withIndex("by_userId", (q) => q.eq("userId", args.userId))
      .take(args.limit ?? 50);
  },
});
```

---

## Mutation with Soft Delete

```ts
import { mutation } from "../_generated/server";
import { v } from "convex/values";
import { itemDocValidator } from "./schemas";

export const create = mutation({
  args: { name: v.string() },
  returns: v.id("items"),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    return await ctx.db.insert("items", {
      name: args.name,
      userId: identity.subject,
      status: "pending",
      createdAt: Date.now(),
    });
  },
});


export const archive = mutation({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const item = await ctx.db.get("items", args.id);
    if (!item || item.userId !== identity.subject) {
      throw new Error("Not found");
    }

    await ctx.db.patch("items", args.id, {
      deletedAt: Date.now(),
    });
    return null;
  },
});


export const listActive = query({
  args: { userId: v.id("users") },
  returns: v.array(itemDocValidator),
  handler: async (ctx, args) => {
    const items = await ctx.db
      .query("items")
      .withIndex("by_userId", (q) => q.eq("userId", args.userId))
      .take(100);

    return items.filter((item) => item.deletedAt === undefined);
  },
});
```

---

## Action with Node.js

```ts
"use node";

import { internalAction } from "../_generated/server";
import { v } from "convex/values";
import { internal } from "../_generated/api";

export const processExternal = internalAction({
  args: { itemId: v.id("items") },
  returns: v.object({ success: v.boolean() }),
  handler: async (ctx, args) => {
    const result = await fetch("https://api.example.com/process", {
      method: "POST",
      body: JSON.stringify({ id: args.itemId }),
    });

    if (!result.ok) {
      throw new Error(`API error: ${result.status}`);
    }

    await ctx.runMutation(internal.items.mutations.updateStatus, {
      itemId: args.itemId,
      status: "processed",
    });

    return { success: true };
  },
});
```

---

## Void Returns Pattern

```ts
export const updateItem = mutation({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch("items", args.id, { updatedAt: Date.now() });
    return null;
  },
});
```

ESLint conflict: if using `unicorn/no-null`, add file-level disable:

```ts
/* eslint-disable unicorn/no-null -- Convex v.null() requires explicit null */
```

## Notes

- Prefer `.withIndex()` over `.filter()`.
- Keep reads bounded with `.take(n)` or pagination.
