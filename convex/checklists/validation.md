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

**[advisory]** - Should pass, warn if not:

- [ ] Convex MCP used to check deployments/functions/logs [advisory]
- [ ] Logs verified before/after changes (MCP/CLI/dashboard) [advisory]
- [ ] Tests exist for new behavior [advisory]
