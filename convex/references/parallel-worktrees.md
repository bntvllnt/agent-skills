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

3) Bootstrap project context (CRITICAL — easy to miss)
   `npx convex deployment select|create` requires CONVEX_DEPLOYMENT to be
   present in the environment to know which Convex team+project to scope
   into. A fresh worktree's .env.local does not exist yet (gitignored), so
   without bootstrap the CLI fails with: "No CONVEX_DEPLOYMENT set, run
   `npx convex dev` to configure".

   Seed only the CONVEX_DEPLOYMENT line from the primary worktree's
   .env.local — do NOT copy secrets, URLs, or other keys. Primary path
   pattern (adjust to your monorepo layout):

     primary=$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')
     primary_env="$primary/packages/backend/.env.local"
     [ -f "$primary_env" ] || { echo "Run \`npx convex dev\` once in $primary first" >&2; exit 1; }
     grep -E '^CONVEX_DEPLOYMENT=' "$primary_env" > packages/backend/.env.local
     chmod 600 packages/backend/.env.local

   If the primary itself has no CONVEX_DEPLOYMENT, error loudly with
   actionable next steps — do not silently auto-provision.

4) (No-op for fresh worktrees) Strip inherited cloud bindings if the
   worktree somehow has stale CONVEX_*/CONVEX_SITE_URL keys from a copied
   env. The bootstrap above writes a clean one-line .env.local, so this
   normally has nothing to do. Apply only when carrying env explicitly.

5) Try select first; fall back to create
   # in the directory that contains convex.json
   npx convex deployment select dev/my-feature-a3b4faf9 \
     || npx convex deployment create dev/my-feature-a3b4faf9 --type dev --select \
          --expiration "in 14 days"

   # --select rewrites .env.local with the worktree's CONVEX_DEPLOYMENT,
   # CONVEX_URL, CONVEX_SITE_URL — the bootstrap line above is replaced.
   # --expiration is the only Convex-supported auto-cleanup mechanism.

6) Generate types
   npx convex dev --once       # one-shot codegen, non-blocking (recommended for agents)
   # or
   npx convex dev              # long-running watcher

7) Verify isolation
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

### Cleanup When a Worktree Retires (CANONICAL ORDER)

**Important truth check.** `npx convex deployment delete` is **not** a real CLI subcommand. Run `npx convex deployment --help` to confirm — only `select` and `create` are exposed. Convex provides no public API to delete a cloud dev deployment either. The dashboard UI is the only way to remove the cloud-side deployment.

What you can automate:

1. Strip CONVEX_* keys from the worktree's `.env.local` (preserve unrelated keys like `BETTER_AUTH_SECRET`, `RESEND_API_KEY`)
2. Delete `.env.local` outright if nothing else remained
3. Print the dashboard URL for the cloud-side delete

Mandatory ordering — `dev:remove` MUST run **before** `git worktree remove`:

```
1) From inside the worktree, clear the local link
   pnpm -F backend dev:remove        # or your equivalent script
   #   -> strips CONVEX_DEPLOYMENT/CONVEX_URL/CONVEX_SITE_URL from .env.local
   #   -> preserves any unrelated keys (BETTER_AUTH_SECRET, RESEND_API_KEY, ...)
   #   -> prints the dashboard URL for the cloud-side delete

2) (Optional) Visit the printed dashboard URL → Settings → Delete deployment
   Required for permanent cleanup. The CLI cannot do this.
   Skip this step if you used --expiration at create time and the deployment
   is allowed to expire on its own.

3) Remove the git worktree
   cd <repo-root-or-primary>
   git worktree remove <path>
```

**Why this order matters.** Once the worktree directory is gone, `dev:remove` can no longer read its `.env.local` to discover the deployment ref, and the dashboard URL has to be reconstructed manually. Always run `dev:remove` first.

**Rules:**

- **Refuse to act on the primary's `dev`.** Detect with `git worktree list --porcelain` — the first entry is the primary. Auxiliary worktrees are safe; the primary is not (its `dev` is shared baseline).
- Prefer `--expiration "in 7 days"` (or 14, 30) at create time so forgotten worktrees self-clean on the cloud side. The expiration value is documented in `npx convex deployment create --help`.
- Stale cloud deployments: if `dev:remove` was skipped before `git worktree remove`, the cloud deployment lingers. Open the dashboard at `https://dashboard.convex.dev/t/<team>/<project>` and delete entries matching `dev/*` that no longer correspond to a live worktree.

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

## Common Errors and How to Prevent Them

### Error: "did not find convex.json / settings" or "please log in" inside a fresh worktree

**Symptom.** Right after `git worktree add`, you run `npx convex dev` (or any `npx convex` command) and the CLI:

- Complains it can't find Convex project linkage / "settings" / "convex.json"
- Prompts you to run `npx convex login` even though you're already logged in on this machine
- Drops into an interactive first-run setup flow

**Root cause.** Convex authentication is **global** (`~/.convex/config.json`) and is shared across every worktree on the machine. But `.env.local` — which holds `CONVEX_DEPLOYMENT` and the deployment URLs — is **gitignored** and therefore is **not** carried into a new worktree by `git worktree add`. When `npx convex dev` cannot find `CONVEX_DEPLOYMENT`, it falls back to first-run setup, which involves an OAuth-style flow that *looks* like a re-login prompt.

### Prevention (Mandatory)

Run the ensure-flow as the **first** Convex command in every new worktree, before `npx convex dev` or anything else. Crucially, the flow must **prompt the user before silently creating a new cloud deployment** when the worktree has no `.env*` files yet — auto-creation can leak unwanted dev deployments into the project, and an agent should never assume that's the user's intent.

**Decision tree:**

```
Is there any .env* file in the backend dir?
│
├─ YES, and CONVEX_DEPLOYMENT is set
│    -> Run `npx convex deployment select <ref-from-env>`; you're done.
│
├─ YES, but no CONVEX_DEPLOYMENT
│    -> Bootstrap CONVEX_DEPLOYMENT from primary's .env.local first
│       (write only that line — do NOT copy secrets/URLs).
│       Then run the slug-based ensure-flow:
│         try `deployment select dev/<slug>`,
│         on miss `deployment create dev/<slug> --type dev --select --expiration "in 14 days"`.
│
└─ NO .env* at all (fresh worktree, nothing carried)
     -> STOP. Ask the user how they want to populate it. Don't auto-create.
        Options to offer:
          1. Create a new per-worktree dev deployment (`dev/<slug>`)
             [will bootstrap CONVEX_DEPLOYMENT from primary, then select|create]
          2. Paste an existing Convex deployment URL or ref
             [will bootstrap from primary, then select that ref]
          3. Copy `.env.local` from the primary worktree
             [shares the primary's deployment — loses isolation]
        Only proceed with option 1 (auto-create) after explicit confirmation.

In every branch, "bootstrap from primary" means: read $primary/packages/backend/.env.local,
extract its CONVEX_DEPLOYMENT line, write that single line to the worktree's .env.local
(chmod 600). This gives `npx convex deployment select|create` the team+project context
it needs to scope into. Without bootstrap, those commands fail with "No CONVEX_DEPLOYMENT
set". If the primary itself has no CONVEX_DEPLOYMENT, error loudly with actionable next
steps — point the user at `cd <primary>/packages/backend && npx convex dev` once.
```

Why prompt instead of auto-creating? Three reasons:

- **Cost / sprawl.** Auto-creating per worktree without consent fills the project with stale `dev/*` deployments. Cleanup is manual unless `--expiration` is set, and even then it leaks until expiry.
- **Wrong target.** The user may actually want this worktree to hit shared dev, staging, or a sibling worktree's deployment — not a brand new one.
- **Auth surprise.** If the user is logged into the wrong Convex account, auto-create silently provisions in the wrong project.

### Agent Rule (BLOCKING)

When operating autonomously in a fresh worktree:

1. Check for `.env*` files in the backend dir before any `npx convex` command.
2. If none exist, **ask the user** with the three options above. Quote what would happen for each. Wait for explicit choice.
3. If `.env.local` exists but lacks `CONVEX_DEPLOYMENT`, prefer the slug-based ensure-flow (option 1) but still mention it in chat so the user can override.
4. Never run `deployment create` without user confirmation in fresh-worktree contexts.

### Interactive Bootstrap Script

A minimal wrapper that implements the decision tree, including the bootstrap-from-primary step that gives the Convex CLI project context. Suitable for a worktree post-create hook or `pnpm dev:stack` preflight:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Run from within the worktree, after `git worktree add`.
# - Bootstraps CONVEX_DEPLOYMENT from primary's .env.local so the CLI has project context
# - Selects (or creates) a per-worktree dev/<slug> deployment
# - Prompts the user when no .env exists and primary cannot help
# - Fails closed (exit 2) in non-interactive shells when ambiguous

backend_dir="$(git rev-parse --show-toplevel)/packages/backend"   # adjust to your layout
cd "$backend_dir"

# Locate primary worktree (always the first entry in `git worktree list --porcelain`)
primary="$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')"
primary_env="$primary/packages/backend/.env.local"

env_files=( .env.local .env.development.local .env )
existing=()
for f in "${env_files[@]}"; do
  [[ -f "$f" ]] && existing+=("$f")
done

has_deployment=0
if [[ ${#existing[@]} -gt 0 ]]; then
  if grep -qE '^[[:space:]]*CONVEX_DEPLOYMENT=' "${existing[@]}"; then
    has_deployment=1
  fi
fi

# Per-worktree slug (deterministic, collision-resistant)
worktree_root="$(git rev-parse --show-toplevel)"
worktree_name="$(basename "$worktree_root")"
sanitized="$(printf '%s' "$worktree_name" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g; s/-{2,}/-/g')"
sanitized="${sanitized:-dev}"
sanitized="${sanitized:0:39}"
suffix="$(printf '%s:%s' "$(hostname)" "$(realpath "$worktree_root")" \
  | sha1sum | awk '{ print substr($1, 1, 8) }')"
slug="${sanitized}-${suffix}"
ref="dev/${slug}"

# Skip bootstrap entirely on primary checkout
if [[ "$worktree_root" == "$primary" ]]; then
  echo "Primary checkout — using shared 'dev' deployment. Nothing to do."
  exit 0
fi

# Branch 1: env exists with CONVEX_DEPLOYMENT — just select it (idempotent re-attach)
if [[ ${#existing[@]} -gt 0 && $has_deployment -eq 1 ]]; then
  current_ref="$(grep -E '^[[:space:]]*CONVEX_DEPLOYMENT=' "${existing[@]}" \
    | head -n1 | sed -E 's/^[[:space:]]*CONVEX_DEPLOYMENT=//; s/^"//; s/"$//')"
  echo "Existing deployment ref in env: $current_ref"
  npx convex deployment select "$current_ref"
  exit 0
fi

# Helper: bootstrap CONVEX_DEPLOYMENT-only line from primary's .env.local
bootstrap_from_primary() {
  if [[ ! -f "$primary_env" ]]; then
    cat >&2 <<EOF
Cannot bootstrap Convex project context for this worktree.
  Reason: $primary_env not found.

Fix:
  1. cd $primary
  2. cd packages/backend && npx convex dev   (pick a project once)
  3. Re-run this script.
EOF
    return 1
  fi
  if ! grep -qE '^CONVEX_DEPLOYMENT=' "$primary_env"; then
    cat >&2 <<EOF
Cannot bootstrap Convex project context for this worktree.
  Reason: $primary_env has no CONVEX_DEPLOYMENT line.

Fix: cd $primary/packages/backend && npx convex dev — then retry.
EOF
    return 1
  fi
  grep -E '^CONVEX_DEPLOYMENT=' "$primary_env" > .env.local
  chmod 600 .env.local
  echo "Bootstrapped CONVEX_DEPLOYMENT from $primary_env into $backend_dir/.env.local"
}

# Branch 2: env exists but no CONVEX_DEPLOYMENT — bootstrap then ensure-flow
if [[ ${#existing[@]} -gt 0 && $has_deployment -eq 0 ]]; then
  echo "Env file present but no CONVEX_DEPLOYMENT."
  bootstrap_from_primary || exit 1
  if ! npx convex deployment select "$ref" >/dev/null 2>&1; then
    npx convex deployment create "$ref" --type dev --select --expiration "in 14 days"
  fi
  exit 0
fi

# Branch 3: no env at all — prompt, then bootstrap + select/create
cat <<EOF
No .env* file found in $backend_dir.

Choose how to populate Convex env for this worktree:
  1) Create or attach a per-worktree dev deployment ($ref)
     [bootstraps CONVEX_DEPLOYMENT from primary, then select|create dev/<slug>]
  2) Paste an existing Convex deployment URL or ref
     [requires bootstrap from primary first; will not auto-bootstrap if you cancel]
  3) Copy .env.local from the primary worktree (loses isolation)
  q) Quit and let me decide manually
EOF

if [[ ! -t 0 ]]; then
  echo "Non-interactive shell. Refusing to auto-create. Re-run interactively or pre-populate .env.local." >&2
  exit 2
fi

read -rp "Choice [1/2/3/q]: " choice
case "$choice" in
  1)
    bootstrap_from_primary || exit 1
    if ! npx convex deployment select "$ref" >/dev/null 2>&1; then
      npx convex deployment create "$ref" --type dev --select --expiration "in 14 days"
    fi
    ;;
  2)
    bootstrap_from_primary || exit 1
    read -rp "Paste deployment ref or URL: " ref_or_url
    npx convex deployment select "$ref_or_url"
    ;;
  3)
    if [[ -f "$primary_env" ]]; then
      cp "$primary_env" .env.local
      echo "Copied $primary_env -> $backend_dir/.env.local"
      echo "WARNING: this worktree now shares the primary's deployment. No isolation."
    else
      echo "Primary .env.local not found at $primary_env" >&2
      exit 1
    fi
    ;;
  q|Q)
    echo "Aborted. Nothing changed."
    exit 0
    ;;
  *)
    echo "Invalid choice." >&2
    exit 1
    ;;
esac
```

Save as `scripts/setup-convex-worktree.sh`. Subsequent runs are idempotent: Branch 1 re-selects without recreating.

### Teardown Script (Companion)

`npx convex deployment delete` does not exist. The script can only clear the local env link and surface the dashboard URL for the cloud-side delete. Save as `scripts/teardown-convex-worktree.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

backend_dir="$(git rev-parse --show-toplevel)/packages/backend"   # adjust to your layout
cd "$backend_dir"

worktree_root="$(git rev-parse --show-toplevel)"
primary="$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')"

if [[ "$worktree_root" == "$primary" ]]; then
  echo "Refusing to tear down: this is the primary checkout (shared 'dev' deployment)." >&2
  exit 1
fi

env_file=".env.local"
[[ -f "$env_file" ]] || { echo "No .env.local — nothing to tear down."; exit 0; }

# Capture the ref before stripping so we can print the dashboard URL
ref="$(grep -E '^CONVEX_DEPLOYMENT=' "$env_file" | head -n1 \
  | sed -E 's/^CONVEX_DEPLOYMENT=//; s/^"//; s/"$//' || true)"

# Strip CONVEX_* keys; preserve unrelated ones
tmp="$(mktemp)"
grep -vE '^(CONVEX_DEPLOYMENT|CONVEX_URL|CONVEX_SITE_URL|NEXT_PUBLIC_CONVEX_URL|EXPO_PUBLIC_CONVEX_URL|NEXT_PUBLIC_CONVEX_SITE_URL)=' "$env_file" > "$tmp" || true

if [[ -s "$tmp" ]]; then
  mv "$tmp" "$env_file"
  echo "Stripped CONVEX_* keys from $env_file (other keys preserved)."
else
  rm -f "$tmp" "$env_file"
  echo "Removed $env_file (no other keys remained)."
fi

if [[ -n "$ref" ]]; then
  cat <<EOF

Cloud deployment is NOT deleted. The Convex CLI exposes no delete command;
do this manually in the dashboard:

  https://dashboard.convex.dev/

Find the deployment matching: $ref
Settings -> Delete deployment.

If the deployment was created with --expiration, you can also let it expire
on its own.
EOF
fi
```

**Mandatory ordering:** run `teardown-convex-worktree.sh` BEFORE `git worktree remove`. Once the worktree directory is gone, `.env.local` is unreadable and you have to reconstruct the deployment ref manually.

**Non-interactive contexts** (CI, headless agents): the bootstrap script fails closed (exit 2) when stdin is not a TTY and no env exists. The agent should detect that exit code and surface the choice to its operator rather than retrying.

### Error: "auth token expired" or genuine re-login required

**Cause.** `~/.convex/config.json` access token is missing or revoked, so it actually does need a fresh login.

**Fix.** From any worktree on the machine: `npx convex login`. This updates the global config and benefits every worktree at once.

**How to tell apart from the previous error.** In the previous case, `~/.convex/config.json` exists with a valid token; the issue is local to the worktree. In this case, the global config file is missing or its token rejected. The CLI's wording is similar in both, but only the global-config issue actually requires re-login — the worktree-local issue is fixed by running the ensure-flow.

### Error: codegen race / "convex/_generated/ is out of date"

**Cause.** Two `npx convex dev` processes targeting the same deployment from different worktrees are pushing conflicting code.

**Fix.** Confirm each worktree resolves to its own `dev/<slug>` ref (run the ensure-flow), and that `.env.local` `CONVEX_URL` differs between worktrees. If two worktrees show the same URL, the slug derivation is non-deterministic or the suffix hash collided — re-derive using the recipe above.

### Error: `npx convex deploy` shipped to staging instead of production (multi-prod setups)

See `references/environments.md` for the full multi-environment guide. Short answer: only one prod deployment can be `--default`; ensure that the production one (not staging) was created with `--default`, and that CI uses an explicit `CONVEX_DEPLOY_KEY` scoped to the right deployment.

## Anti-Patterns

- **Sharing `CONVEX_DEPLOYMENT` across worktrees** — codegen race, stale `_generated/`, cross-branch reactive invalidation
- **Two `npx convex dev` watchers against the same cloud deployment** — last writer wins on push; subscriptions thrash
- **Skipping the bootstrap step** — `npx convex deployment select|create` fails with "No CONVEX_DEPLOYMENT set" without project context. Always seed `CONVEX_DEPLOYMENT` from primary first
- **Copying primary's `.env.local` wholesale** — drags secrets and stale URLs into the worktree. Bootstrap copies *only* the `CONVEX_DEPLOYMENT` line; `--select` then writes the rest
- **Using only the worktree basename as the slug** — two worktrees with the same name on different machines collide
- **Calling `npx convex deployment delete`** — that subcommand does not exist. Cloud-side delete is dashboard-only. Use `--expiration` at create time or accept manual cleanup
- **Skipping `dev:remove` before `git worktree remove`** — once the worktree directory is gone, `.env.local` is unreadable and the deployment ref is lost; the dashboard URL has to be reconstructed manually
- **Touching the primary's `dev` deployment as part of cleanup** — destroys the shared baseline; cleanup scripts must refuse when `worktree_root == primary`
- **Treating anonymous-mode data as durable** — it's not; do not rely on it for review, demos, or QA
- **Running ensure flows in parallel without a lock** — `select` then `create` is not atomic; concurrent runs duplicate-create or race on `.env.local` writes
- **Hardcoding `CONVEX_URL` in committed env files** — it must be derived per worktree; commit only the schema and function code

## Validation Checklist

### Onboarding (after `git worktree add`)

- [ ] Slug is deterministic and includes a host+path hash suffix
- [ ] Bootstrap step ran: worktree's `.env.local` contains exactly the primary's `CONVEX_DEPLOYMENT` line (and only that, before `--select`)
- [ ] Pattern A: `npx convex deployment select dev/<slug>` succeeded, OR `create --type dev --select [--expiration ...]` ran once
- [ ] Pattern B: `CONVEX_AGENT_MODE=anonymous` set instead (sandbox / no-auth context)
- [ ] After `--select`: `.env.local` has `CONVEX_DEPLOYMENT`, `CONVEX_URL`, `CONVEX_SITE_URL` matching the slug; secrets are NOT polluted
- [ ] `npx convex dev --once` (or `dev`) completes without OAuth prompt for the chosen pattern
- [ ] `convex/_generated/` regenerated for this worktree
- [ ] Auth-failure errors are surfaced with a clear "run `npx convex login`" message
- [ ] Ensure-flow is serialized per worktree via a lock file when called concurrently
- [ ] Two worktrees run their dev backends simultaneously with no codegen conflict and no state crossover

### Teardown (before `git worktree remove`)

- [ ] Teardown script ran first; `git worktree remove` came second
- [ ] Worktree's `.env.local` had `CONVEX_*` keys stripped (or file deleted if it had no other keys)
- [ ] Unrelated keys (`BETTER_AUTH_SECRET`, `RESEND_API_KEY`, etc.) preserved
- [ ] Dashboard URL printed for cloud-side delete (or `--expiration` was set at create time and self-cleanup is acceptable)
- [ ] Primary's `dev` deployment was NOT touched (script refuses on primary)
- [ ] Cloud-side delete completed via dashboard for permanent cleanup, OR deployment is left to expire

## Reference Implementation

A production-tested implementation of Pattern A (with bootstrap, locking, slug derivation, auth-failure recovery, and full test coverage) is reasonable as a 300-400 line Node script. Stages:

```
1. Detect worktree state          (git worktree list --porcelain)
2. Skip everything if primary     (worktree_root == primary)
3. Compute slug                   (basename + sha1(host:abspath).slice(0,8))
4. Resolve deploymentRef          ("dev/<slug>" for auxiliary)
5. Acquire backend-dir lock       (PID file with mtime staleness check)
6. Bootstrap project context      (write only CONVEX_DEPLOYMENT line from primary's .env.local)
7. Try `deployment select <ref>`
8. On failure -> `deployment create <ref> --type dev --select [--expiration ...]`
9. Detect auth failures and rethrow with actionable message
10. Reload .env.local; return { ref, slug, cloudUrl, siteUrl, created }
11. Release lock
```

Teardown script (separate entrypoint):

```
1. Refuse if primary checkout
2. Read CONVEX_DEPLOYMENT from .env.local before stripping (so we can print the dashboard URL)
3. Strip CONVEX_DEPLOYMENT/CONVEX_URL/CONVEX_SITE_URL/NEXT_PUBLIC_CONVEX_*/EXPO_PUBLIC_CONVEX_*
4. Preserve unrelated keys; delete the file if nothing else remained
5. Print dashboard URL for manual cloud-side delete
```

Both scripts gate on `isAuxiliaryWorktree` (the first `git worktree list --porcelain` entry is the primary; everything else is auxiliary). The teardown script does NOT call any `deployment delete` CLI command — that command does not exist.
