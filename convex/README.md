# Convex

Convex skill for building and operating Convex backends: functions, schemas, auth, scheduling, components, migrations, performance, testing, and debugging.

## Entry Points

- Home/router: `convex/SKILL.md`
- Quickstart: `convex/references/quickstart.md`
- Auth setup: `convex/references/auth-setup.md`
- Components: `convex/references/components.md`
- Migrations: `convex/references/migrations.md`
- Performance: `convex/references/performance.md`
- MCP usage (recommended): `convex/references/mcp.md`
- CLI usage/help: `convex/references/cli-help.md`
- Validation checklist: `convex/checklists/validation.md`

## Install

```bash
npx skills add bntvllnt/agent-skills --skill convex
```

Manual install (download this folder only):

- Copy the `convex/` folder into your agent's skills directory.
- Ensure the folder name is `convex` and includes `SKILL.md`.

## Upstream Skills (Recommended Companion)

This skill delegates canonical Convex content to the official `get-convex/agent-skills` collection when those skills are installed. Local references stay as fallback and host project conventions (folder org, eslint config, validation checklist).

```bash
npx skills add get-convex/agent-skills
```

Routing precedence and delegation map: see `SKILL.md` "Upstream Skills".

## Requirements

- Optional (recommended): Convex MCP server configured for your agent.
- Optional (recommended): upstream `get-convex/agent-skills` installed.
- CLI workflows: Node.js + the Convex CLI (typically `npx convex ...`).
