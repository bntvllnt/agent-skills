# Convex

Convex skill for building and operating Convex backends: functions (queries/mutations/actions), schemas, auth, scheduling, components, testing, and debugging.

## Entry Points

- Home/router: `convex/SKILL.md`
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

## Requirements

- Optional (recommended): Convex MCP server configured for your agent.
- CLI workflows: Node.js + the Convex CLI (typically `npx convex ...`).
