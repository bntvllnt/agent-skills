# Schema Patterns

Docs:

- Schema: https://docs.convex.dev/database/schemas
- Indexes: https://docs.convex.dev/database/reading-data/indexes

## Dual Validators (Recommended)

IMPORTANT: Maintain BOTH data validator and document validator. Place validators in `validators.ts` within each scope folder (enforced by `convex-rules/no-bare-v-any`).

```ts
// <scope>/validators.ts
import { defineTable } from "convex/server";
import { v, Infer } from "convex/values";


export const itemValidator = v.object({
  name: v.string(),
  userId: v.id("users"),
  status: v.union(v.literal("pending"), v.literal("active")),
  createdAt: v.number(),
});

export type Item = Infer<typeof itemValidator>;


export const itemDocValidator = v.object({
  _id: v.id("items"),
  _creationTime: v.number(),
  name: v.string(),
  userId: v.id("users"),
  status: v.union(v.literal("pending"), v.literal("active")),
  createdAt: v.number(),
});

export type ItemDoc = Infer<typeof itemDocValidator>;


export const itemsTable = defineTable(itemValidator)
  .index("by_userId", ["userId"])
  .index("by_userId_createdAt", ["userId", "createdAt"])
  .index("by_status", ["status"]);
```

---

## Discriminated Unions for Metadata

```ts
export const vTransactionMetadata = v.union(
  v.object({ type: v.literal("usage"), rawUsageId: v.string(), model: v.optional(v.string()) }),
  v.object({ type: v.literal("payment"), orderId: v.string(), provider: v.string() }),
  v.object({ type: v.literal("refund"), originalId: v.id("transactions"), reason: v.string() }),
  v.object({ type: v.literal("grant"), grantedBy: v.optional(v.id("users")), reason: v.string() })
);
```

---

## Index Naming Convention

```text
by_userId           -> ["userId"]
by_userId_createdAt -> ["userId", "createdAt"]
by_status_priority  -> ["status", "priority"]
by_owner            -> ["ownerType", "ownerId"]
```

---

## Junction Tables (Many-to-Many)

```ts
export const trackGenresTable = defineTable({
  trackId: v.id("tracks"),
  genreId: v.id("genres"),
})
  .index("by_track", ["trackId"])
  .index("by_genre", ["genreId"]);
```

---

## Project Structure (Enforced by @vllnt/eslint-config)

```text
convex/
  lib/
    validators.ts           shared v.any() aliases
  <scope>/
    queries.ts              query(), internalQuery()
    mutations.ts            mutation(), internalMutation()
    internal_mutations.ts   internalMutation() (optional split)
    actions.ts              action(), internalAction()
    validators.ts           v.* validators + types
    schema.ts               table definitions
    workflows.ts
    tests/
  migrations/               relaxed namespace rules
  schema.ts
  convex.config.ts
  auth.config.ts
  crons.ts
  http.ts
  _generated/               excluded from linting
```

snake_case filenames required (e.g. `user_helper.ts`, not `user-helper.ts`). Config files exempt.
