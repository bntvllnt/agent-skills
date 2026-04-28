# Migrations

Upstream canonical: prefer the `convex-migration-helper` skill from `get-convex/agent-skills` if installed, or WebFetch it: https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-migration-helper/SKILL.md . This file is the local fallback and supplements upstream with project conventions.

Docs: https://docs.convex.dev/database/schemas

Skip when: greenfield schema with no existing data, adding optional fields, adding new tables, or adding/removing indexes with no correctness concern.

## Key Concepts

Convex will not deploy a schema that does not match data at rest. This drives the workflow:

- Cannot add a required field if existing documents lack it
- Cannot change a field type if existing documents have the old type
- Cannot remove a field if existing documents still have it

## Safe Changes (No Migration Needed)

### Adding optional field

```ts
// Before
users: defineTable({ name: v.string() })

// After -- safe
users: defineTable({ name: v.string(), bio: v.optional(v.string()) })
```

### Adding new table

```ts
posts: defineTable({
  userId: v.id("users"),
  title: v.string(),
}).index("by_user", ["userId"])
```

### Adding index

```ts
users: defineTable({ name: v.string(), email: v.string() })
  .index("by_email", ["email"])
```

## Breaking Changes: Widen-Migrate-Narrow

Every breaking migration follows the same multi-deploy pattern:

**Deploy 1 -- Widen the schema:**

1. Update schema to allow both old and new formats
2. Update code to handle both formats when reading
3. Update code to write new format for new documents
4. Deploy

**Between deploys -- Migrate data:**

5. Run migration to backfill existing documents
6. Verify all documents migrated

**Deploy 2 -- Narrow the schema:**

7. Update schema to require new format only
8. Remove code that handles old format
9. Deploy

## Using @convex-dev/migrations

For any non-trivial migration, use the migrations component. It handles batching, pagination, state tracking, resume from failure, dry runs, and progress monitoring.

### Setup

```bash
npm install @convex-dev/migrations
```

```ts
// convex/convex.config.ts
import { defineApp } from "convex/server";
import migrations from "@convex-dev/migrations/convex.config.js";

const app = defineApp();
app.use(migrations);
export default app;
```

```ts
// convex/migrations.ts
import { Migrations } from "@convex-dev/migrations";
import { components } from "./_generated/api.js";
import { DataModel } from "./_generated/dataModel.js";

export const migrations = new Migrations<DataModel>(components.migrations);
export const run = migrations.runner();
```

### Define a migration

```ts
export const addDefaultRole = migrations.define({
  table: "users",
  migrateOne: async (ctx, user) => {
    if (user.role === undefined) {
      await ctx.db.patch(user._id, { role: "user" });
    }
  },
});
```

Shorthand (return object = auto-patch):

```ts
export const clearField = migrations.define({
  table: "users",
  migrateOne: () => ({ legacyField: undefined }),
});
```

### Run a migration

```bash
npx convex run migrations:run '{"fn": "migrations:addDefaultRole"}'
```

Or programmatically:

```ts
await migrations.runOne(ctx, internal.migrations.addDefaultRole);
```

### Run multiple in order

```ts
export const runAll = migrations.runner([
  internal.migrations.addDefaultRole,
  internal.migrations.clearDeprecatedField,
]);
```

### Dry run

```bash
npx convex run migrations:runIt '{"dryRun": true}'
```

### Check status

```bash
npx convex run --component migrations lib:getStatus --watch
```

### Cancel

```bash
npx convex run --component migrations lib:cancel '{"name": "migrations:addDefaultRole"}'
```

### Configuration

Custom batch size (large documents or heavy write traffic):

```ts
export const migrateHeavy = migrations.define({
  table: "largeDocuments",
  batchSize: 10,
  migrateOne: async (ctx, doc) => { /* ... */ },
});
```

Migrate subset using index:

```ts
export const fixEmpty = migrations.define({
  table: "users",
  customRange: (query) => query.withIndex("by_name", (q) => q.eq("name", "")),
  migrateOne: () => ({ name: "<unknown>" }),
});
```

Parallelize within batch:

```ts
export const clearField = migrations.define({
  table: "myTable",
  parallelize: true,
  migrateOne: () => ({ optionalField: undefined }),
});
```

## Common Patterns

### Adding a required field

```ts
// Deploy 1: allow both states
users: defineTable({
  name: v.string(),
  role: v.optional(v.union(v.literal("user"), v.literal("admin"))),
})

// Migration
export const addDefaultRole = migrations.define({
  table: "users",
  migrateOne: async (ctx, user) => {
    if (user.role === undefined) {
      await ctx.db.patch(user._id, { role: "user" });
    }
  },
});

// Deploy 2: make required
users: defineTable({
  name: v.string(),
  role: v.union(v.literal("user"), v.literal("admin")),
})
```

### Deleting a field

```ts
// Deploy 1: make optional
// isPro: v.boolean()  -->  isPro: v.optional(v.boolean())

// Migration
export const removeIsPro = migrations.define({
  table: "teams",
  migrateOne: async (ctx, team) => {
    if (team.isPro !== undefined) {
      await ctx.db.patch(team._id, { isPro: undefined });
    }
  },
});

// Deploy 2: remove isPro from schema entirely
```

### Changing a field type

Prefer creating a new field:

```ts
// Deploy 1: add new field, keep old optional
// Migration: convert
export const convertToEnum = migrations.define({
  table: "teams",
  migrateOne: async (ctx, team) => {
    if (team.plan === undefined) {
      await ctx.db.patch(team._id, {
        plan: team.isPro ? "pro" : "basic",
        isPro: undefined,
      });
    }
  },
});

// Deploy 2: remove isPro, make plan required
```

### Splitting nested data into a separate table

```ts
export const extractPreferences = migrations.define({
  table: "users",
  migrateOne: async (ctx, user) => {
    if (user.preferences === undefined) return;

    const existing = await ctx.db
      .query("userPreferences")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .first();

    if (!existing) {
      await ctx.db.insert("userPreferences", {
        userId: user._id,
        ...user.preferences,
      });
    }

    await ctx.db.patch(user._id, { preferences: undefined });
  },
});
```

Ensure code already writes to the new table for new users before running the migration.

### Small table shortcut

For small tables (a few thousand documents), skip the component:

```ts
import { internalMutation } from "./_generated/server";

export const backfillSmall = internalMutation({
  handler: async (ctx) => {
    const docs = await ctx.db.query("smallConfig").collect();
    for (const doc of docs) {
      if (doc.newField === undefined) {
        await ctx.db.patch(doc._id, { newField: "default" });
      }
    }
  },
});
```

Only use `.collect()` when certain the table is small.

## Zero-Downtime Strategies

### Dual write (preferred)

Write both formats, read old until migration completes. Safe to rollback at any point.

```ts
// Good: writing both structures during migration
export const createTeam = mutation({
  args: { name: v.string(), isPro: v.boolean() },
  handler: async (ctx, args) => {
    const plan = args.isPro ? "pro" : "basic";
    await ctx.db.insert("teams", {
      name: args.name,
      isPro: args.isPro,
      plan,
    });
  },
});
```

### Dual read

Read both formats, write only new. Avoids duplicate writes but harder to rollback.

```ts
function getTeamPlan(team: Doc<"teams">): "basic" | "pro" {
  if (team.plan !== undefined) return team.plan;
  return team.isPro ? "pro" : "basic";
}
```

## Common Pitfalls

1. **Making field required before migrating data** -- Convex rejects the deploy.
2. **Using `.collect()` on large tables** -- Hits transaction limits. Use the migrations component.
3. **Not writing new format before migrating** -- Documents created during migration window get missed.
4. **Skipping dry run** -- Use `dryRun: true` to validate before production.
5. **Deleting fields prematurely** -- Prefer deprecating with `v.optional` + comment.
6. **Using crons for batches** -- The component handles batching internally.

## Verification

```ts
export const verifyMigration = query({
  handler: async (ctx) => {
    const remaining = await ctx.db
      .query("users")
      .filter((q) => q.eq(q.field("role"), undefined))
      .take(10);

    return {
      complete: remaining.length === 0,
      sampleRemaining: remaining.map((u) => u._id),
    };
  },
});
```

Or use component status:

```bash
npx convex run --component migrations lib:getStatus --watch
```

## Checklist

- [ ] Identified breaking change and planned multi-deploy workflow
- [ ] Schema widened to allow both old and new formats
- [ ] Code handles both formats when reading
- [ ] Code writes new format for new documents
- [ ] Deployed widened schema
- [ ] Migration tested with `dryRun: true`
- [ ] Migration run and status monitored
- [ ] All documents verified migrated
- [ ] Schema narrowed to require new format only
- [ ] Old-format handling code removed
- [ ] Final deploy complete
- [ ] Migration code removed once stable
