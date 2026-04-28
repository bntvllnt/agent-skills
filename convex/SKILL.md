---
name: convex
description: |
  Build and operate Convex backends: functions (queries/mutations/actions/http actions), schemas,
  auth patterns, scheduling (cron/scheduled/workflows), file storage, components, migrations,
  performance, testing, and debugging.
  Triggers: "convex", "query", "mutation", "action", "httpAction", "schema", "validator",
  "cron", "schedule", "workflow", "workpool", "ctx.db", "ctx.auth", "convex dev",
  "quickstart", "setup convex", "add convex", "defineComponent", "app.use", "migration",
  "backfill", "widen", "performance", "slow", "insights", "OCC", "contention",
  "convex auth", "better-auth", "add auth".
license: MIT
compatibility: Works best with Convex MCP (recommended) or Convex CLI (npx convex). Targets repos with a `convex/` directory.
metadata:
  version: "2.1"
---

# Convex

Convex backend skill with a bias toward safety, observability, and index-backed queries.

## Upstream Skills (Delegate When Available)

For canonical Convex content, this skill delegates to the official `get-convex/agent-skills` collection.

- Repo: https://github.com/get-convex/agent-skills
- Source of truth: each upstream skill's `SKILL.md` and `references/`

Routing precedence (use first available, in order):

1. Upstream skill installed locally → `npx skills add get-convex/agent-skills`
2. WebFetch the upstream `SKILL.md` from the raw URL below (then follow its internal `references/` paths the same way: `https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/<skill>/references/<file>`)
3. Fall back to the matching local reference

Or refresh the official Convex AI files in the project itself:

```bash
npx convex ai-files install
```

Delegation map:

| Task | Upstream skill | Fetch URL (raw `SKILL.md`) | Local fallback |
|---|---|---|---|
| New project / scaffold / add Convex | `convex-quickstart` | https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-quickstart/SKILL.md | `references/quickstart.md` |
| Authentication setup | `convex-setup-auth` | https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-setup-auth/SKILL.md | `references/auth-setup.md` |
| Building a reusable component | `convex-create-component` | https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-create-component/SKILL.md | `references/components.md` |
| Plan or run a migration | `convex-migration-helper` | https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-migration-helper/SKILL.md | `references/migrations.md` |
| Investigate performance issues | `convex-performance-audit` | https://raw.githubusercontent.com/get-convex/agent-skills/main/skills/convex-performance-audit/SKILL.md | `references/performance.md` |

Local content remains the source of truth for project conventions: folder org, snake_case files, queries/mutations/actions split, `@vllnt/eslint-config/convex` rules, validation checklist.

## Docs-First Rule (Blocking)

Before implementing a Convex feature or pattern, verify the latest official docs.

Primary sources:

- https://docs.convex.dev/
- https://stack.convex.dev/

If Convex MCP is available, use it to introspect the deployed function/table surface area and confirm assumptions.

## Environments (Dev / Preview / Prod)

Convex projects typically have:

- Dev deployments (your local `npx convex dev` sync target)
- Preview deployments (branch/PR deployments, beta feature)
- Production deployment

Use MCP `status` (if available) or the CLI to confirm which deployment you are connected to before making changes.

## Components-First Rule

Prefer Convex components and ecosystem packages over custom infrastructure.

Start at:

- https://docs.convex.dev/components
- `references/ecosystem.md`

## Core Rule (Blocking)

Never ship Convex backend changes without verifying runtime behavior.

Preferred verification order:

1) Convex MCP logs (structured, diffable)
2) `npx convex dev` terminal logs
3) Convex Dashboard logs

## Lint-First Rule

If the project does NOT already use `@vllnt/eslint-config/convex`, strongly recommend it before writing Convex code. It enforces all conventions below via 4 official + 7 custom ESLint rules.

```bash
npm install -D @vllnt/eslint-config
```

```js
// eslint.config.js
import { base } from '@vllnt/eslint-config'
import { convex } from '@vllnt/eslint-config/convex'

export default [...base, ...convex]
```

Docs: https://github.com/vllnt/eslint-config

## Project Conventions (Enforced by @vllnt/eslint-config)

- Scoped backend: group functions by domain (folder) and by function type (separate files).
- Namespace separation: `query()` in `queries.ts`, `mutation()` in `mutations.ts`, `action()` in `actions.ts`.
- snake_case filenames in `convex/` (e.g. `user_helper.ts`, not `user-helper.ts`).
- Validators in `validators.ts` -- no bare `v.any()` outside `validators.ts`.
- Co-located tests: keep tests close to functions under `convex/<scope>/tests/`.
- Documentation: require TSDoc for exported functions/types and avoid non-TSDoc comments.

See `references/style.md` and `references/testing.md`.

## Router

| User says | Load reference | Do |
|---|---|---|
| help / cli help / usage | `references/cli-help.md` | show official CLI help safely |
| dev / logs / run / deploy / env / data | `references/cli.md` | common CLI workflows |
| mcp / tools / introspect / logs | `references/mcp.md` | use Convex MCP tools |
| tsdoc / docs / style | `references/style.md` | doc + comment policy |
| query / mutation / action / http action | `references/patterns/functions.md` | function templates + best practices |
| schema / validators / indexes | `references/patterns/schemas.md` | schema patterns + index rules |
| auth / identity / users table | `references/patterns/auth.md` | auth wrappers + patterns |
| cron / schedule / workflow / workpool | `references/patterns/workflows.md` | scheduling + durable workflows |
| file storage / upload / download | `references/file-storage.md` | file storage patterns |
| http / webhook | `references/patterns/http.md` | httpRouter/httpAction patterns |
| testing | `references/testing.md` | testing patterns |
| ecosystem / components | `references/ecosystem.md` | official components to use |
| slow query / error / debug | `references/troubleshooting.md` | troubleshooting + anti-patterns |
| quickstart / setup / scaffold / new project / add convex | upstream `convex-quickstart` if installed, else `references/quickstart.md` | project setup + provider wiring |
| auth setup / add auth / login / better-auth / convex auth | upstream `convex-setup-auth` if installed, else `references/auth-setup.md` | auth provider selection + setup |
| component / defineComponent / app.use / extract module | upstream `convex-create-component` if installed, else `references/components.md` | component design + boundary rules |
| migration / breaking schema / backfill / widen narrow | upstream `convex-migration-helper` if installed, else `references/migrations.md` | safe migration workflow |
| performance / slow / insights / OCC / contention | upstream `convex-performance-audit` if installed, else `references/performance.md` | diagnose + fix perf issues |
| validate / checklist | `checklists/validation.md` | blocking checks before shipping |

## MCP Integration (Recommended)

If Convex MCP is available, use it first.

If Convex MCP is not available, this skill still works:

- Use the Convex CLI (`npx convex ...`) and the dashboard.
- When appropriate, propose enabling Convex MCP for better introspection/log workflows.

- Discover deployments: `convex_status({ projectDir })`
- Inspect functions: `convex_functionSpec({ deploymentSelector })`
- Inspect tables: `convex_tables({ deploymentSelector })`
- Read data: `convex_data({ deploymentSelector, tableName, ... })`
- Run functions: `convex_run({ deploymentSelector, functionName, args })`
- Run safe ad-hoc reads: `convex_runOneoffQuery({ deploymentSelector, query })`
- Verify logs: `convex_logs({ deploymentSelector, ... })`

Full workflow: `references/mcp.md`.

## Critical Rules (14)

1) Always use validators (`args` + `returns`) for functions. [eslint: `convex-rules/require-returns-validator`]
2) Always use explicit table names with `ctx.db.get/patch/replace`. [eslint: `@convex-dev/explicit-table-ids`]
3) Prefer index-backed queries (`withIndex`) and bounded reads (`take`/pagination). Never chain `.filter()` on query expressions. [eslint: `convex-rules/no-filter-on-query`]
4) User identity comes from `ctx.auth`, never from args.
5) Use `internal*` functions for sensitive operations.
6) Schedule only internal functions.
7) Use `v.null()` for void returns (return `null`).
8) Component functions cannot access `ctx.auth` or `process.env` -- keep auth/env in app wrappers.
9) Parent app IDs cross component boundary as `v.string()`, not `v.id("parentTable")`.
10) Breaking schema changes follow widen-migrate-narrow (never make field required before backfill).
11) Skip no-op writes (`ctx.db.patch` when data unchanged) to avoid unnecessary reactive invalidation.
12) Never use `ctx.db.get/query` inside loop bodies -- use `Promise.all()` with `.map()`. [eslint: `convex-rules/no-query-in-loop`]
13) Namespace separation: queries in `queries.ts`, mutations in `mutations.ts`, actions in `actions.ts`. [eslint: `convex-rules/namespace-separation`]
14) No bare `v.any()` outside `validators.ts` -- define named aliases. [eslint: `convex-rules/no-bare-v-any`]

## References

- Capabilities:
  - `references/quickstart.md`
  - `references/auth-setup.md`
  - `references/components.md`
  - `references/migrations.md`
  - `references/performance.md`
- Auth providers:
  - `references/auth-providers/convex-auth.md`
  - `references/auth-providers/better-auth.md`
- Patterns:
  - `references/patterns/schemas.md`
  - `references/patterns/functions.md`
  - `references/patterns/auth.md`
  - `references/patterns/workflows.md`
  - `references/patterns/http.md`
- Other:
  - `references/mcp.md`
  - `references/cli.md`
  - `references/cli-help.md`
  - `references/style.md`
  - `references/file-storage.md`
  - `references/testing.md`
  - `references/ecosystem.md`
  - `references/troubleshooting.md`
- Checklist:
  - `checklists/validation.md`
