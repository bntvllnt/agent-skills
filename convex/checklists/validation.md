# Validation Checklist

## Before Submitting

**[blocking]** - Must pass to continue:

- [ ] All `db.get/patch/replace` use explicit table name [blocking]
- [ ] Dual validators: data + document (with `_id`, `_creationTime`) [blocking]
- [ ] Prefer index-backed queries (`withIndex`) over `filter` [blocking]
- [ ] Bounded reads with `.take(n)` or pagination [blocking]
- [ ] `returns` validators on all functions [blocking]
- [ ] User identity from `ctx.auth`, never args [blocking]
- [ ] Internal functions for sensitive operations [blocking]
- [ ] Schedulers reference `internal.*`, not `api.*` [blocking]
- [ ] Runtime verified via logs (MCP preferred, else `npx convex dev` or dashboard) [blocking]
- [ ] Quickstart: `convex/_generated/` exists after setup [blocking]
- [ ] Components: component imports from own `_generated/server`, not app's [blocking]
- [ ] Components: auth/env stay in app wrappers, not component functions [blocking]
- [ ] Migrations: schema widened before data migration runs [blocking]
- [ ] Migrations: migration tested with `dryRun: true` before production [blocking]
- [ ] Performance: no JS `.filter()` or Convex `.filter()` on hot paths without index [blocking]
- [ ] No `ctx.db.get/query` inside loop bodies -- use `Promise.all` + `.map()` [blocking]
- [ ] Namespace separation: queries in `queries.ts`, mutations in `mutations.ts`, actions in `actions.ts` [blocking]
- [ ] No bare `v.any()` outside `validators.ts` [blocking]
- [ ] snake_case filenames in `convex/` (except config files) [blocking]
- [ ] No utility-only `helpers.ts` / `validators.ts` / `types.ts` / `schemas.ts` / `constants.ts` added under `convex/` when they could live in `src/` [blocking]

**[advisory]** - Should pass, warn if not:

- [ ] Convex MCP used to check deployments/functions/logs [advisory]
- [ ] Logs verified before/after changes (MCP/CLI/dashboard) [advisory]
- [ ] Tests exist for new behavior [advisory]
- [ ] Quickstart: provider wired at app root, not inside component [advisory]
- [ ] Components: parent IDs cross boundary as `v.string()` [advisory]
- [ ] Migrations: dual-write during migration window [advisory]
- [ ] Performance: `npx convex insights --details` checked for signal [advisory]
- [ ] Module count from `convex/_generated/api.d.ts` checked when adding files/components; warn above ~330, block above ~350 [advisory]
