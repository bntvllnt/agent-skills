# Convex Environments (Dev / Preview / Staging / Prod) in One Project

Sources:

- <https://docs.convex.dev/production/hosting/preview-deployments> ("production sharding, or staging setups")
- <https://docs.convex.dev/production>
- `npx convex deployment --help` and `npx convex deployment create --help` (authoritative for CLI flags)

This skill verifies CLI behavior against `convex@1.36.1`. Re-verify with `npx convex deployment --help` when on a newer version.

## What Convex Officially Supports

> "By default, projects have a single shared prod deployment and each developer working on the project has their own dev deployment. However, you can create additional deployments for advanced use cases like preview environments, isolated developer instances, production sharding, or staging setups."
>
> — https://docs.convex.dev/production/hosting/preview-deployments

So per project you can host:

| Type | Default count | Multiple supported |
|---|---|---|
| `dev` | One per developer (`dev`) | Yes — any number of `dev/<slug>` (use case: per-worktree, see `references/parallel-worktrees.md`) |
| `preview` | Auto-created per branch | Yes — any number of `preview/<branch>` |
| `prod` | One default (`production`) | Yes — any number of named prod deployments (use case: staging, sharding, regions) |

Older Convex setups used a separate project for staging/production. That pattern still works, but **named prod deployments inside one project** is now first-class and reduces project sprawl, IAM duplication, and team-membership churn.

## Deployment Refs

| Ref form | Meaning |
|---|---|
| `dev` | Your personal default cloud dev deployment |
| `dev/<name>` | A named dev deployment in the current project |
| `local` | Your local deployment for the current project |
| `preview/<name>` | A named preview deployment |
| `<name>` (no prefix, type prod) | A named prod deployment (e.g. `staging`, `production`) |
| `some-project:<ref>` | Cross-project (same team) |
| `some-team:some-project:<ref>` | Fully qualified |

## Authoritative CLI

```
npx convex deployment select <ref>
npx convex deployment create <ref> --type <dev|prod|preview> [--select] [--default] [--region <r>] [--expiration <when>]
```

Verified flag behavior (per `--help`):

- `--select` — sets the new deployment as active and writes URLs to `.env.local` (`CONVEX_URL`, `CONVEX_SITE_URL`, plus framework-specific public mirrors)
- `--default` — marks the new prod deployment as the default that `npx convex deploy` (without `--deployment`) will target. **Critical** when you have multiple prod deployments and want to control which one `npx convex deploy` ships to
- `--expiration` — TTL for ephemeral deployments (e.g. `"in 7 days"`, `"none"`, ISO 8601, UNIX seconds/ms). Useful for preview-like staging
- `--region` — pin to a specific region

## When to Use Multi-Prod-Per-Project vs Separate Projects

Use **multi-prod in one project** when:

- Staging and production share the same team, IAM, billing, and codebase
- You want the same `convex/` source pushed through staging then production
- You want the dashboard, logs, and metrics for staging and prod side by side
- You're sharding production by region or tenant inside one logical service

Use **a separate project for production** when:

- Production must be isolated from non-prod team membership (e.g. you don't want non-admins able to switch between prod and staging by selecting a deployment ref)
- Billing/compliance requires fully separate Convex projects
- You want a strict trust boundary that the project itself enforces, not just role policies

For most teams, multi-prod in one project is now the simpler default.

## Step-by-Step: Add a Staging Deployment to an Existing Project

```
1) Authenticate (once)
   npx convex login

2) Make sure you're on the project you want
   npx convex deployment select production       # or your existing default prod

3) Create the staging deployment
   npx convex deployment create staging --type prod
   # Don't pass --select unless you want your laptop's active deployment to switch
   # Don't pass --default — `production` should remain the default for `npx convex deploy`

4) Confirm in the dashboard that "staging" appears alongside "production"

5) Decide how staging gets deployed
   Option A — manual:
     CONVEX_DEPLOYMENT=<team>:<project>:staging npx convex deploy
   Option B — CI pipeline with a deploy key (recommended):
     # In dashboard: create a deploy key scoped to the staging deployment
     # In CI:
     CONVEX_DEPLOY_KEY=<staging-key> npx convex deploy
   Option C — local agent inspection:
     npx convex deployment select staging
     # subsequent npx convex commands run against staging until you select another
```

## Step-by-Step: Targeting a Specific Deployment for One-off Commands

Per `npx convex deployment select --help`:

> "You can also run individual commands on another deployment by using the `--deployment` flag on that command."

Examples:

```
# Run a query against staging without switching active deployment
npx convex run myFunction --deployment staging

# Tail prod logs while keeping dev selected for hot reload
npx convex logs --deployment production

# Set an env var on staging
npx convex env set FOO bar --deployment staging
```

`--prod` is a shortcut that targets the default prod (whatever was created with `--default` or your project's original `production`). It does not target a non-default named prod — use `--deployment <ref>` for those.

## Step-by-Step: Production Sharding (Multiple Active Prods)

Use case: regional shards, tenant isolation, blue/green prod.

```
1) Create each shard
   npx convex deployment create prod-eu  --type prod --region eu
   npx convex deployment create prod-us  --type prod --region us
   npx convex deployment create prod-apac --type prod

2) Pick one as the default for `npx convex deploy`
   npx convex deployment create prod-eu --type prod --region eu --default
   # (or set --default at create time on whichever is your primary)

3) Deploy to each shard via deploy keys in CI
   # one CI job per shard, each with its own CONVEX_DEPLOY_KEY scoped to that shard

4) Application reads its own CONVEX_URL from .env.local / runtime config —
   serve EU traffic from prod-eu's URL, US from prod-us, etc.
```

## Promotion Workflow (Dev -> Staging -> Prod)

```
1) Develop against dev (or per-worktree dev/<slug>)
2) Push to PR -> CI creates a preview/<branch> automatically (if preview keys configured)
3) Merge to main -> CI deploys to staging
   CONVEX_DEPLOY_KEY=<staging-key> npx convex deploy
   # Run smoke tests against the staging URL
4) Tag/release -> CI deploys to default prod
   CONVEX_DEPLOY_KEY=<production-key> npx convex deploy
```

Each stage uses the same `convex/` source. Schema, functions, and codegen go through unchanged; data is per-deployment.

## Environment Variables and Naming

Convex doesn't impose a `CONVEX_ENV` value — that's an app convention. A common app-level pattern:

| Deployment | App-level `CONVEX_ENV` |
|---|---|
| `dev` / `dev/<slug>` | `dev` |
| `preview/<branch>` | `preview` |
| `staging` (named prod) | `staging` |
| `production` (default prod) | `production` |
| `prod-eu`, `prod-us` (shards) | `production` (or `production-<region>`) |

Wire `CONVEX_ENV` from your CI pipeline / runtime config; gate cron jobs, autonomous workflows, and dangerous side effects on it (e.g. only run autonomous imports when `CONVEX_ENV === "production"`).

## Anti-Patterns

- **Marking staging as `--default`** — accidentally makes `npx convex deploy` ship to staging when devs run it locally. Reserve `--default` for the actual production deployment
- **Sharing one deploy key across prod deployments** — defeats the point of the split; create a key per deployment
- **Letting `--select` switch a CI runner's active deployment** — CI should use `CONVEX_DEPLOY_KEY` and `--deployment`, not modify `.env.local`
- **Treating `staging` as ephemeral** — without `--expiration`, named prod deployments are permanent. Set TTL only if you genuinely want auto-cleanup
- **Mixing per-worktree dev refs (`dev/<slug>`) with named prod refs in the same `.env.local`** — `--select` overwrites cleanly, but manual edits often leave stale URLs. Prefer `npx convex deployment select` over hand-editing
- **Running migrations / data backfills against the wrong prod** — always pass `--deployment <ref>` explicitly for write operations against named prods, even if your active deployment is correct

## Validation Checklist

- [ ] `npx convex deployment list` (if available) or the dashboard shows the expected deployments
- [ ] Default prod is the actual production (verify with `npx convex deployment select production` succeeding without ambiguity)
- [ ] `npx convex deploy` without flags ships to the intended default prod (dry-run first: `npx convex deploy --dry-run`)
- [ ] Each named prod has its own deploy key in CI (one key per deployment)
- [ ] `CONVEX_DEPLOY_KEY=<staging-key> npx convex deploy --dry-run` reports the right target
- [ ] App-level `CONVEX_ENV` is set per deployment and gates dangerous workflows
- [ ] Local devs select dev / per-worktree dev refs, never staging or prod, for `npx convex dev`
- [ ] Cleanup plan exists for ephemeral named prods (either explicit `deployment delete` or `--expiration`)

## See Also

- Per-worktree dev deployments: `references/parallel-worktrees.md`
- Migrations across stages: `references/migrations.md`
- Performance per-deployment: `references/performance.md`
