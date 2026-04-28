# Parallel Worktree Development (Isolated Convex Backends)

Docs:

- Convex CLI overview: <https://docs.convex.dev/cli>
- `npx convex deployment --help` (authoritative for `select` / `create` syntax)
- Git worktree skill: see `git/SKILL.md` "Worktrees"

Skip when: single worktree, single agent, no parallel dev.

## Why

`npx convex dev` is a per-process watcher tied to a single deployment. Two worktrees pointing at the same `CONVEX_DEPLOYMENT` will:

- Race over `convex/_generated/` codegen
- Cross-pollinate reactive subscriptions between branches
- Overwrite each other's pushes on hot reload

To run multiple worktrees (or multiple agents) in parallel, give each its own backend.

## TL;DR Decision Guide

| Situation | Pattern |
|---|---|
| Authenticated dev machine, multiple long-lived worktrees, want cloud dashboard + persistent data | **A — Per-worktree cloud dev (`dev/<slug>`)** |
| Cloud agent / CI / sandbox VM that cannot OAuth, ephemeral work | **B — Anonymous local backend** |
| One human, occasional second worktree (hotfix), don't need persistence in the secondary | A in primary, serialize watchers, or B in secondary |

Pattern A is recommended whenever the agent or developer can authenticate. It uses Convex's first-class named-deployment support and gives you cloud features (logs, dashboard, persistence). Pattern B is the fallback for environments without auth.

---

## Pattern A — Per-Worktree Cloud Dev Deployment (Recommended)

Convex supports any number of named dev deployments per project via the `dev/<slug>` ref. Each worktree gets its own. Codegen, schema, data, and `.env.local` URLs are fully isolated. Standard cloud features (dashboard, logs, persistence) all work.

### Authoritative CLI (verified via `npx convex deployment --help`)

```
npx convex deployment select <ref>            # Switch active deployment
npx convex deployment create <ref> --type dev --select [--expiration "in 7 days"]
                                              # Create a named dev deployment.
                                              # --select also writes URLs to .env.local
```

Refs accepted by `select`:

```
dev                              # Your personal default cloud dev deployment
local                            # Local deployment
dev/<name>                       # A named dev deployment in the current project
some-project:dev/<name>          # Cross-project (same team)
some-team:some-project:dev/<name># Fully qualified
```

### Slug Derivation (Production-Tested Pattern)

A worktree's deployment slug should be:

- **Deterministic** — same worktree always resolves to the same slug
- **Collision-resistant across machines** — two devs with the same worktree name get different slugs
- **Sanitized** — Convex slugs are lowercase, `[a-z0-9-]`, max 48 chars

Recipe:

```
slug = sanitize(basename(worktree_path)) + "-" + sha1(hostname + ":" + abspath(worktree_path)).slice(0, 8)
```

Where `sanitize` is:

```
toLowerCase()
replace(/[^a-z0-9]+/g, "-")
strip leading/trailing dashes
collapse multiple dashes
empty -> "dev"
```

The 8-char SHA1 suffix is the collision guard; the readable prefix exists so `npx convex deployment list` is human-scannable. Clamp the prefix so the total stays ≤ 48 chars.

### Step-by-Step: Onboard a Worktree

```
1) Create the worktree (use the git skill for env carry-over)
   git worktree add ../my-feature -b feat/my-feature main
   cd ../my-feature

2) Compute the slug
   - basename: my-feature
   - sha1("hostname:/abs/path/to/my-feature").slice(0,8): e.g. a3b4faf9
   - slug: my-feature-a3b4faf9
   - ref:  dev/my-feature-a3b4faf9

3) Strip inherited cloud bindings from the carried .env.local before doing anything else
   - Remove any of: CONVEX_DEPLOYMENT, CONVEX_URL, NEXT_PUBLIC_CONVEX_URL,
     EXPO_PUBLIC_CONVEX_URL, CONVEX_SITE_URL, NEXT_PUBLIC_CONVEX_SITE_URL,
     CONVEX_DEPLOY_KEY
   - This prevents the worktree from silently reusing the parent's backend

4) Try select first; fall back to create
   # in the convex/ directory (or wherever you run npx convex)
   npx convex deployment select dev/my-feature-a3b4faf9 \
     || npx convex deployment create dev/my-feature-a3b4faf9 --type dev --select \
          --expiration "in 14 days"

   # --select writes CONVEX_URL/NEXT_PUBLIC_CONVEX_URL/CONVEX_SITE_URL into .env.local
   # --expiration auto-cleans up forgotten worktree deployments

5) Generate types
   npx convex dev --once       # one-shot codegen, non-blocking (recommended for agents)
   # or
   npx convex dev              # long-running watcher

6) Verify isolation
   - convex/_generated/ exists in this worktree
   - .env.local CONVEX_URL ends with the new deployment slug
   - Cloud dashboard shows the new dev deployment
   - Two worktrees can run dev simultaneously without a codegen race
```

### Concurrency: Locking ensure-runs

If multiple processes (e.g. parallel agents on the same worktree) call the onboarding flow at once, they will race on `deployment select/create`. Wrap the ensure flow in a per-worktree advisory lock:

```
lock = path.join(backendDir, ".convex-dev-ensure.lock")

acquire(lock) {            # write our PID to lock; if file exists, retry
  for up to 30s:
    try create(lock, "wx") with our PID
    on EEXIST:
      if (mtime > 60s old) or (process for stored PID is dead):
        remove and retry
      else:
        sleep 100ms and retry
}
release(lock) { remove }
```

This keeps the slow path (`select` -> create on miss -> `--select` rewrite of `.env.local`) safely serialized within one worktree without blocking other worktrees.

### Cleanup When a Worktree Retires

```
npx convex deployment delete dev/<slug> --yes
```

Rules:

- **Refuse to delete the primary's `dev`.** Detect with `git worktree list --porcelain`; only the first line is the primary. Anything else is auxiliary and safe to clean up.
- Prefer `--expiration "in 7 days"` (or 14, 30) at create time so forgotten worktrees self-clean. Cleanup-on-retire becomes optional rather than mandatory.

### Auth Failure Recovery

If `select` or `create` returns text matching `not logged in`, `npx convex login`, `unauthorized`, `not authenticated`, or `auth token`, surface a precise error:

```
Convex CLI is not authenticated. Run `npx convex login` from <backendDir>, then retry.
```

Never silently swallow auth failures — they look identical to "deployment doesn't exist" if you aren't checking.

### Reference Contract

A correct ensure-flow returns:

```
{
  isAuxiliaryWorktree: boolean
  worktreeName: string
  deploymentRef: "dev" | "dev/<slug>"
  deploymentSlug: string | undefined
  cloudUrl: string         # CONVEX_URL after --select
  siteUrl: string          # CONVEX_SITE_URL after --select
  created: boolean         # true if we just created vs reused
}
```

Wire this to whatever launcher your stack uses (e.g. `pnpm dev:stack`, a Makefile, or the agent's worktree-bootstrap step). Run it before spawning the dev watcher, frontend dev server, or any process that reads `CONVEX_URL`.

### Per-Worktree Port Allocation (Optional but Recommended)

When the worktree also runs a frontend or mobile dev server, allocate a deterministic port range per worktree to avoid `EADDRINUSE`:

```
worktreeIndex = position in `git worktree list --porcelain`   # 0 = primary
stackPort     = 41000 + worktreeIndex * 10
{ web: stackPort, mobile-web: stackPort+1, convex-local: stackPort+2, metro: stackPort+3 }
```

`stackPort` is just a base offset; pick whatever band makes sense for your machine.

---

## Pattern B — Anonymous Local Backend (Sandbox / CI / Headless)

`CONVEX_AGENT_MODE=anonymous` runs a fully local, no-auth Convex backend on the current machine. Use it when:

- The agent cannot OAuth (cloud sandbox, headless CI runner, ephemeral container)
- You want zero cloud footprint for throwaway work
- You explicitly want unshared, non-persistent state

### Step-by-Step

```
1) Create the worktree
   git worktree add ../sandbox-feature -b feat/sandbox main
   cd ../sandbox-feature

2) Strip inherited cloud bindings (same as Pattern A step 3)

3) Opt into anonymous mode
   echo 'CONVEX_AGENT_MODE=anonymous' >> .env.local

4) Generate types and start
   npx convex dev --once     # or: npx convex dev (watcher)

5) Verify
   - Local backend URL printed (loopback / 127.0.0.1)
   - convex/_generated/ exists
   - No CONVEX_DEPLOYMENT pointing at *.convex.cloud
```

### What anonymous mode gives / doesn't give

| Gives | Doesn't give |
|---|---|
| No OAuth, fully local | Persistent cloud-stored data |
| Independent of any other worktree | Cloud dashboard / log UI |
| Schema, functions, codegen all work | Preview deployments |
| Safe for cloud agents and CI | Shared QA — no one else can connect |

Treat anonymous-mode data as **ephemeral**. It evaporates when the local backend stops.

---

## Anti-Patterns

- **Sharing `CONVEX_DEPLOYMENT` across worktrees** — codegen race, stale `_generated/`, cross-branch reactive invalidation
- **Two `npx convex dev` watchers against the same cloud deployment** — last writer wins on push; subscriptions thrash
- **Carrying `.env.local` into a new worktree without stripping `CONVEX_*`** — the worktree silently reuses the parent's backend until the next ensure-run
- **Using only the worktree basename as the slug** — two worktrees with the same name on different machines collide
- **Deleting the primary's `dev` deployment as part of cleanup** — destroys the shared baseline; always check `isAuxiliaryWorktree` first
- **Treating anonymous-mode data as durable** — it's not; do not rely on it for review, demos, or QA
- **Running ensure flows in parallel without a lock** — `select` then `create` is not atomic; concurrent runs duplicate-create or race on `.env.local` writes
- **Hardcoding `CONVEX_URL` in committed env files** — it must be derived per worktree; commit only the schema and function code

## Validation Checklist

- [ ] Worktree has its own `.env.local`
- [ ] Inherited `CONVEX_*` cloud bindings stripped before ensure-run
- [ ] Slug is deterministic and includes a host+path hash suffix
- [ ] Pattern A: `npx convex deployment select dev/<slug>` succeeds, OR `create --type dev --select` ran once
- [ ] Pattern B: `CONVEX_AGENT_MODE=anonymous` set
- [ ] `--select` populated `.env.local` (Pattern A) — `CONVEX_URL` ends with the slug
- [ ] `npx convex dev --once` (or `dev`) completes without OAuth prompt for the chosen pattern
- [ ] `convex/_generated/` regenerated for this worktree
- [ ] Auth-failure errors are surfaced with a clear "run `npx convex login`" message
- [ ] Ensure-flow is serialized per worktree via a lock file
- [ ] Cleanup path exists: either `deployment delete dev/<slug>` on retire, or `--expiration` set at create time
- [ ] Two worktrees run their dev backends simultaneously with no codegen conflict and no state crossover
- [ ] Primary's `dev` deployment is never targeted by cleanup

## Reference Implementation

A production-tested implementation of Pattern A (with locking, slug derivation, auth-failure recovery, and a 100% covered test suite) is reasonable as a 200-300 line Node script. Stages:

```
1. Detect worktree state          (git worktree list --porcelain)
2. Compute slug                   (basename + sha1(host:abspath).slice(0,8))
3. Resolve deploymentRef          (primary -> "dev"; auxiliary -> "dev/<slug>")
4. Acquire backend-dir lock       (PID file with mtime staleness check)
5. Try `deployment select <ref>`
6. On failure -> `deployment create <ref> --type dev --select --expiration ...`
7. Detect auth failures and rethrow with actionable message
8. Reload .env.local; return { ref, slug, cloudUrl, siteUrl, created }
9. Release lock
```

Cleanup script symmetrically uses `deployment delete <ref> --yes`, refusing to act when `isAuxiliaryWorktree` is false.
