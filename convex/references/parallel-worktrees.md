# Parallel Worktree Development (Isolated Convex Backends)

Docs:

- Convex CLI overview: <https://docs.convex.dev/cli>
- Quickstart (Node / agent context): <https://docs.convex.dev/quickstart/nodejs>
- Git worktree (project skill): see `git/SKILL.md` "Worktrees"

Skip when: single worktree, single agent, no parallel dev.

## Why

`npx convex dev` is a per-machine, per-deployment watcher. Two worktrees pointing at the same `CONVEX_DEPLOYMENT` will fight over codegen and live sync, and reactive subscriptions will cross-pollinate state between branches.

To run multiple worktrees (or multiple agents) in parallel, each worktree needs its own backend.

## Honest Limits

Convex's official docs document **one** first-class isolation primitive: `CONVEX_AGENT_MODE=anonymous`, which spins up a local anonymous backend with no auth and no cloud dependency. Multi-cloud-deployment-per-developer is not first-class today; the cloud workarounds below are workarounds, not blessed paths.

If you need durable shared state across worktrees, prefer a single primary worktree with cloud dev + ephemeral anonymous backends in the others.

## Pattern A — Anonymous Local Backend per Worktree (Recommended for Agents)

Each worktree opts into anonymous mode. Convex creates an isolated local backend per worktree process. No auth prompt. No conflict. Data is ephemeral (lives only while the local backend runs and persists in the worktree's local Convex state directory).

### Step-by-Step

```
1) Create the worktree (use the git skill — handles env carry-over)
   git worktree add ../my-feature-worktree -b feat/my-feature main
   cd ../my-feature-worktree

2) Strip any inherited cloud bindings from the carried .env.local so the
   worktree cannot accidentally reuse the parent's cloud deployment.
   Remove these keys if present (any framework variant your app uses):
     CONVEX_DEPLOYMENT
     CONVEX_URL
     VITE_CONVEX_URL
     NEXT_PUBLIC_CONVEX_URL
     EXPO_PUBLIC_CONVEX_URL
     CONVEX_DEPLOY_KEY

3) Opt the worktree into anonymous mode by adding to .env.local:
     CONVEX_AGENT_MODE=anonymous

4) Generate types and start the local deployment.
   For agents (non-blocking, one-shot codegen):
     npx convex dev --once
   For long-running iterative work (run in a separate terminal or background):
     npx convex dev

5) Verify the worktree is isolated:
   - convex/_generated/ exists in this worktree
   - .env.local contains CONVEX_AGENT_MODE=anonymous
   - No CONVEX_DEPLOYMENT or *_CONVEX_URL pointing at a cloud URL
   - The CLI printed a local backend URL (loopback / 127.0.0.1)
   - Another worktree's `npx convex dev` does not interfere
```

### What anonymous mode gives you

- Local Convex backend, no OAuth flow
- Independent of any other worktree's deployment
- Safe for cloud agents, CI, sandbox VMs
- Schema, functions, and codegen all work normally

### What anonymous mode does NOT give you

- Persistent cloud-stored data (data lives only in the local backend's state)
- Cloud dashboard / logs UI
- Preview deployments
- Shared QA — anyone else can't connect to your local anonymous backend

## Pattern B — Cloud-Backed Parallel Work (Humans, Optional)

If you need cloud features (dashboard, persistent data, preview deploys) across worktrees, choose one of the following. None of these is first-class; pick the one whose tradeoff fits.

### B.1 Single dev deployment, serialized

Only run `npx convex dev` in one worktree at a time. Switch by stopping the watcher in worktree A before starting it in worktree B. Simplest; no extra setup; loses parallelism.

### B.2 One Convex project per long-lived worktree

Create a separate Convex project for each long-lived worktree:

```
cd ../my-feature-worktree
npx convex dev --configure new
# follow prompts to create a new project
```

Each worktree's `.env.local` then points at its own dev deployment. Data is fully isolated in the cloud. Cost: more projects in your dashboard; manual cleanup when worktrees retire.

### B.3 Hybrid

Cloud dev deployment in your primary worktree (where most work and review happens). `CONVEX_AGENT_MODE=anonymous` in every secondary or agent worktree. Common in practice.

## Decision Guide

| Situation | Pattern |
|---|---|
| Cloud or sandbox agent, ephemeral work | A (anonymous) |
| Multiple agents in parallel on different features | A per worktree |
| One human, occasional second worktree (hotfix) | B.1 (serialize) or A in the secondary |
| Long-lived parallel branches needing persistent cloud data | B.2 (one project per worktree) |
| Mixed: primary humans + parallel agents | B.3 (hybrid) |

## Anti-Patterns

- Sharing `CONVEX_DEPLOYMENT` across worktrees -- causes codegen race, stale `_generated/`, and cross-branch reactive invalidation
- Running two `npx convex dev` watchers against the same cloud deployment
- Carrying `.env.local` to a new worktree without stripping the parent's `CONVEX_*` bindings (the worktree silently inherits the parent's cloud state)
- Treating anonymous-mode data as durable -- it is not; do not rely on it for shared review, demos, or QA
- Using a personal cloud dev deployment from a CI/cloud agent runner -- pollutes your local state with noisy data

## Validation Checklist

- [ ] Worktree has its own `.env.local`
- [ ] Inherited `CONVEX_*` cloud bindings stripped (or replaced with the worktree's own values for B.2)
- [ ] `CONVEX_AGENT_MODE=anonymous` set (Pattern A) OR worktree linked to its own dedicated cloud project (Pattern B.2)
- [ ] `npx convex dev --once` (or `dev`) completes without an OAuth prompt
- [ ] `convex/_generated/` regenerated for this worktree
- [ ] Two worktrees can run `npx convex dev` simultaneously without errors or codegen conflict
- [ ] Stopping one worktree's backend does not affect the other
- [ ] No state crossover (data created in worktree A is not visible in worktree B)
