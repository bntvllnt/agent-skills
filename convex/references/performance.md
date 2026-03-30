# Performance Audit

Docs: https://docs.convex.dev/understanding/best-practices/

Skip when: initial setup, auth setup, component extraction, pure schema migration, or micro-optimization without a user-visible problem.

## Guardrails

- Prefer simpler code when scale is small, traffic is modest, or signals are weak
- Do not recommend digest tables, document splitting, or migration-heavy rollouts without a measured signal or clearly unbounded path
- A simple scan on a small table is often acceptable in Convex

## Step 1: Gather Signals

Start with the strongest signal available:

1. Deployment Health insights (if available from user/context)
2. CLI: `npx convex insights --details` (use `--prod`, `--preview-name`, or `--deployment-name` as needed)
   - If CLI too old: `npx -y convex@latest insights --details`
3. Convex MCP logs (if available)
4. Code audit (if no runtime signals -- keep guardrails in mind)

## Step 2: Signal Routing

| Signal | Section |
|---|---|
| High bytes/documents read, JS filtering, unnecessary joins | Hot Path Rules |
| OCC conflict errors, write contention, mutation retries | OCC Conflicts |
| High subscription count, slow UI updates, excessive re-renders | Subscription Cost |
| Function timeouts, transaction size errors, large payloads | Function Budgets |
| General "it's slow" with no specific signal | Start with Hot Path Rules |

Multiple problem classes can overlap. Read the most relevant section first.

## Step 3: Scope and Trace

Pick one concrete user flow. Write down:

- Entrypoint functions
- Client callsites (`useQuery`, `usePaginatedQuery`, `useMutation`)
- Tables read and written
- Whether the path is high-read, high-write, or both

For each function, trace every `ctx.db.get()`, `ctx.db.query()`, `ctx.db.patch()`, `ctx.db.replace()`, `ctx.db.insert()`. Note foreign-key lookups, JS-side filtering, and full-document reads.

## Step 4: Fix Sibling Functions Together

When one function has a performance bug, audit sibling functions for the same pattern. Do not leave one path fixed and another on the old pattern.

---

## Hot Path Rules

Core principle: every byte read or written multiplies with concurrency.

`cost x calls_per_second x 86400`

In Convex, every write can fan out into reactive invalidation and downstream sync.

### 1. Push filters to storage

Both JavaScript `.filter()` and Convex query `.filter()` mean you already paid for the read. Only `.withIndex()` and `.withSearchIndex()` reduce documents scanned. [eslint: `convex-rules/no-filter-on-query` bans `.filter()` chained on query expressions]

```ts
// Bad: scans then filters
const tasks = await ctx.db.query("tasks").collect();
return tasks.filter((task) => task.status === "open");
```

```ts
// Also bad: Convex .filter() does not push to storage
return await ctx.db.query("tasks")
  .filter((q) => q.eq(q.field("status"), "open"))
  .collect();
```

```ts
// Good: index does the filtering
return await ctx.db.query("tasks")
  .withIndex("by_status", (q) => q.eq("status", "open"))
  .collect();
```

Index migration rule: `undefined !== false` in Convex. If older documents are missing a field, they will not match a compound index entry that expects `false`. Verify backfill status before trusting indexes on optional fields. See `references/migrations.md` for safe rollout.

Check for redundant indexes: `by_foo` and `by_foo_and_bar` are usually redundant (keep only the compound). Exception: if you need results sorted by `foo` then `_creationTime`, the single-field index is needed.

### 2. Minimize data sources

If a function resolves a foreign key for a tiny display field and a denormalized copy exists, prefer it on the hot path.

Denormalize when:

- Path is hot
- Joined document is much larger than the field needed
- Many readers pay that join cost repeatedly

Fallback rule: denormalized data is an optimization, live data is the correctness path. If the denormalized field is missing, fall back to the live read.

```ts
// Bad: missing denormalized data becomes a placeholder
const ownerName = project.ownerName ?? "Unknown owner";
```

```ts
// Good: fall back to live read
const ownerName =
  project.ownerName ??
  (await ctx.db.get(project.ownerId))?.name ??
  null;
```

### 3. Minimize row size (digest tables)

When list queries only need a few fields but documents are large, consider a companion digest table with just the fields needed for listing.

### 4. Skip no-op writes

Every `ctx.db.patch()` triggers reactive invalidation even if data is unchanged.

```ts
// Bad: always writes, even when unchanged
await ctx.db.patch(doc._id, { status: newStatus });
```

```ts
// Good: skip when unchanged
if (doc.status !== newStatus) {
  await ctx.db.patch(doc._id, { status: newStatus });
}
```

### 5. Match consistency to read patterns

- **High-read / low-write**: denormalize aggressively, digest tables, pre-computed aggregates
- **High-read / high-write**: isolate frequently-updated fields into separate documents to minimize invalidation blast radius

---

## OCC Conflicts

Convex uses Optimistic Concurrency Control. When two transactions read and write overlapping data, one is retried. Under load, this becomes contention.

### Symptoms

- OCC conflict errors in logs
- Mutation retries visible in dashboard/insights
- Timeouts under concurrent writes

### Common causes and fixes

**Hot document** (single counter, global config updated frequently):

```ts
// Bad: single counter document updated by every request
await ctx.db.patch(counterId, { count: current.count + 1 });
```

Fix: use `@convex-dev/sharded-counter` to spread writes across shards.

**Wide read set** (query reads many documents, mutation touches one):

Fix: narrow query scope with tighter indexes, smaller read window (`.take(n)`), or move reads to a digest/summary table.

**Competing writers on same row**:

Fix: design mutations to touch fewer shared rows. Use per-user or per-session documents instead of shared ones where possible.

### When to escalate

If the fix requires document splitting, summary tables, or migration-heavy changes, present options to the user before editing. See `references/migrations.md` for safe rollout patterns.

---

## Subscription Cost

Every reactive query (useQuery) is a live subscription. More subscriptions = more work on every relevant write.

### Symptoms

- Slow UI updates
- Excessive re-renders
- Dashboard shows high subscription count

### Fixes

**Too many subscriptions per page**:

Fix: consolidate related queries. One query returning a structured object is cheaper than five returning fragments.

**Queries returning too much data**:

Fix: return only what the UI needs. Use `.take(n)`, pagination, or project fewer fields (digest table pattern).

**Point-in-time reads instead of subscriptions**:

If the data does not need live updates (e.g., user settings loaded once), use a one-shot fetch instead of a subscription where the framework supports it.

**Subscription invalidation amplification**:

If a write to table A invalidates 100 subscriptions, the write fan-out is expensive. Fix: narrow subscription read sets (tighter indexes, smaller tables, digest tables).

---

## Function Budgets

Convex has execution and transaction limits. Hitting these means the function is doing too much work.

### Symptoms

- Function timeout errors
- Transaction size exceeded
- "Too many documents read" errors
- Large payload errors

### Fixes

**Too many documents read in one transaction**:

Fix: add indexes to reduce scan width. Use `.take(n)` or pagination. If you must process many documents, use an action with batched reads via scheduled mutations.

**Large documents**:

Fix: split large blobs into separate documents or use file storage. Keep frequently-read documents lean.

**Large return payloads**:

Fix: return only the fields the client needs. Consider a digest table for list endpoints.

**Long-running computation**:

Fix: move heavy computation to an action (runs outside the transaction). Use `"use node"` for CPU-intensive work.

---

## Verification

After applying fixes:

1. Results are the same -- no dropped records
2. Eliminated reads/writes are no longer in the path
3. Fallback behavior works when denormalized/indexed fields are missing
4. New writes avoid unnecessary invalidation when data unchanged
5. Every relevant sibling reader/writer was inspected

## Checklist

- [ ] Gathered signals from insights, dashboard, or code audit
- [ ] Identified the problem class
- [ ] Scoped one concrete user flow
- [ ] Traced every read and write in the path
- [ ] Identified sibling functions touching same tables
- [ ] Applied fixes following recommended order
- [ ] Fixed sibling functions consistently
- [ ] Verified behavior and no regressions
