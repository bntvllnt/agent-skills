# Components

Upstream canonical: prefer the `convex-create-component` skill from `get-convex/agent-skills` if installed, or WebFetch it: https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-create-component/SKILL.md . This file is the local fallback and supplements upstream with project conventions.

Docs: https://docs.convex.dev/components/authoring

Skip when: one-off business logic, thin utilities without tables, app-level orchestration, or a plain TypeScript library would suffice.

## When to Use

- Extracting reusable backend logic with isolated tables
- Building a third-party integration that owns its own tables and workflows
- Packaging Convex functionality for reuse across apps

## Choose the Shape

| Goal | Shape | Approach |
|------|-------|----------|
| Component for this app only | Local | Put under `convex/components/<name>/` |
| Publish or share across apps | Packaged | Use `npx create-convex@latest --component` |
| Explicitly needs both | Hybrid | Advanced -- confirm user really needs it |
| Not sure | Default to local | Simplest path |

## Default Approach (Local)

```text
convex/
  convex.config.ts          # app: defineApp() + app.use(...)
  components/
    <name>/
      convex.config.ts      # component: defineComponent("<name>")
      schema.ts             # component's own tables
      <feature>.ts          # component functions
```

## Component Skeleton

```ts
// convex/components/notifications/convex.config.ts
import { defineComponent } from "convex/server";

export default defineComponent("notifications");
```

```ts
// convex/components/notifications/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  notifications: defineTable({
    userId: v.string(),
    message: v.string(),
    read: v.boolean(),
  }).index("by_user", ["userId"]),
});
```

```ts
// convex/components/notifications/lib.ts
import { v } from "convex/values";
import { mutation, query } from "./_generated/server.js";

export const send = mutation({
  args: { userId: v.string(), message: v.string() },
  returns: v.id("notifications"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("notifications", {
      userId: args.userId,
      message: args.message,
      read: false,
    });
  },
});

export const listUnread = query({
  args: { userId: v.string() },
  returns: v.array(
    v.object({
      _id: v.id("notifications"),
      _creationTime: v.number(),
      userId: v.string(),
      message: v.string(),
      read: v.boolean(),
    })
  ),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("notifications")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .filter((q) => q.eq(q.field("read"), false))
      .collect();
  },
});
```

```ts
// convex/convex.config.ts
import { defineApp } from "convex/server";
import notifications from "./components/notifications/convex.config.js";

const app = defineApp();
app.use(notifications);

export default app;
```

```ts
// convex/notifications.ts (app-side wrapper)
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { components } from "./_generated/api";
import { getAuthUserId } from "@convex-dev/auth/server";

export const sendNotification = mutation({
  args: { message: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Not authenticated");

    await ctx.runMutation(components.notifications.lib.send, {
      userId,
      message: args.message,
    });
    return null;
  },
});

export const myUnread = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Not authenticated");

    return await ctx.runQuery(components.notifications.lib.listUnread, {
      userId,
    });
  },
});
```

Reference path: a function in `convex/components/notifications/lib.ts` is called as `components.notifications.lib.send` from the app.

## Critical Rules

- Keep authentication in the app -- `ctx.auth` is not available inside components.
- Keep environment access in the app -- component functions cannot read `process.env`.
- Pass parent app IDs across the boundary as `v.string()`, not `v.id("parentTable")`.
- Import from the component's own `./_generated/server`, not the app's generated files.
- Do not expose component functions directly to clients. Create app wrappers.
- If the component defines HTTP handlers, mount routes in the app's `convex/http.ts`.
- If the component needs pagination, use `paginator` from `convex-helpers` (built-in `.paginate()` does not work across the boundary).
- Add `args` and `returns` validators to all public component functions.

## Patterns

### Authentication and environment access

```ts
// Bad: component code cannot rely on app auth or env
const identity = await ctx.auth.getUserIdentity();
const apiKey = process.env.OPENAI_API_KEY;
```

```ts
// Good: app resolves auth and env, passes explicit values
const userId = await getAuthUserId(ctx);
if (!userId) throw new Error("Not authenticated");

await ctx.runAction(components.translator.translate, {
  userId,
  apiKey: process.env.OPENAI_API_KEY,
  text: args.text,
});
```

### Client-facing API

```ts
// Bad: assuming component function is directly callable
export const send = components.notifications.send;
```

```ts
// Good: re-export through an app mutation
export const sendNotification = mutation({
  args: { message: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Not authenticated");

    await ctx.runMutation(components.notifications.lib.send, {
      userId,
      message: args.message,
    });
    return null;
  },
});
```

### IDs across the boundary

```ts
// Bad: parent app table IDs are not valid component validators
args: { userId: v.id("users") }
```

```ts
// Good: treat parent-owned IDs as strings at the boundary
args: { userId: v.string() }
```

## Advanced Patterns

### Function handles for callbacks

When the app needs to pass a callback to the component (common for scheduled work):

```ts
// App side
import { createFunctionHandle } from "convex/server";

export const startJob = mutation({
  handler: async (ctx) => {
    const handle = await createFunctionHandle(internal.myModule.processItem);
    await ctx.runMutation(components.workpool.enqueue, {
      callback: handle,
    });
  },
});
```

```ts
// Component side
import type { FunctionHandle } from "convex/server";

export const enqueue = mutation({
  args: { callback: v.string() },
  handler: async (ctx, args) => {
    const handle = args.callback as FunctionHandle<"mutation">;
    await ctx.scheduler.runAfter(0, handle, {});
  },
});
```

### Deriving validators from schema

```ts
import schema from "./schema.js";

const notificationDoc = schema.tables.notifications.validator.extend({
  _id: v.id("notifications"),
  _creationTime: v.number(),
});
```

### Static configuration with a globals table

```ts
export default defineSchema({
  globals: defineTable({
    maxRetries: v.number(),
    webhookUrl: v.optional(v.string()),
  }),
});
```

### Class-based client wrappers (published components)

```ts
import type { GenericMutationCtx, GenericDataModel } from "convex/server";
import type { ComponentApi } from "../component/_generated/component.js";

type MutationCtx = Pick<GenericMutationCtx<GenericDataModel>, "runMutation">;

export class Notifications {
  constructor(
    private component: ComponentApi,
    private options?: { defaultChannel?: string },
  ) {}

  async send(ctx: MutationCtx, args: { userId: string; message: string }) {
    return await ctx.runMutation(this.component.lib.send, {
      ...args,
      channel: this.options?.defaultChannel ?? "default",
    });
  }
}
```

## Packaged Components

When publishing to npm:

1. `npx create-convex@latest --component` to scaffold
2. Build order: `npx convex codegen --component-dir ./path` -> package build -> `npx convex dev --typecheck-components` in example app
3. Exports: package root (client helpers/types), `./convex.config.js`, `./_generated/component.js`, `./test` (test helpers)
4. Test with `convex-test` for component logic, example app for app-side wrappers

## Validation

Try in order:

1. `npx convex codegen --component-dir convex/components/<name>`
2. `npx convex codegen`
3. `npx convex dev`

Fresh repos may fail until `CONVEX_DEPLOYMENT` is configured. If blocked on login/deployment setup, ask the user for that step.

## Checklist

- [ ] Confirmed a component is the right abstraction
- [ ] Planned tables, public API, boundaries, and app wrappers
- [ ] Component lives under `convex/components/<name>/`
- [ ] Component imports from its own `./_generated/server`
- [ ] Auth, env access, and HTTP routes stay in the app
- [ ] Parent app IDs cross the boundary as `v.string()`
- [ ] Public functions have `args` and `returns` validators
- [ ] Ran `npx convex dev` and fixed codegen or type issues
