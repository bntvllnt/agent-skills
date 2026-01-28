# Convex MCP (Model Context Protocol)

This skill strongly prefers Convex MCP for:

- accurate deployment introspection (functions/tables)
- structured logs
- safe, sandboxed one-off read queries
- environment variable management

Official docs: https://docs.convex.dev/ai/convex-mcp-server

## MCP is optional

If MCP is not configured or not allowed in your environment, use:

- `npx convex dev` terminal logs
- `npx convex logs`
- `npx convex run ...` for manual verification
- Convex Dashboard

When you can, enable MCP to make introspection and log verification faster.

## Setup (for your agent)

Convex docs recommend running the MCP server via:

```bash
npx -y convex@latest mcp start
```

## Configuration options (from Convex docs)

Run MCP server for a single project directory:

```bash
npx -y convex@latest mcp start --project-dir /path/to/project
```

Deployment selection examples:

- prod (requires explicit enablement): `--prod` with `--dangerously-enable-production-deployments`
- preview: `--preview-name <name>`
- specific deployment: `--deployment-name <name>`
- env-file override: `--env-file <path>` (uses `.env.local` / `.env` format)

Disable tools (reduce blast radius):

```bash
npx -y convex@latest mcp start --disable-tools data,run,envSet
```

## Production safety

By default, the MCP server cannot access production deployments. To enable prod access you must explicitly opt in:

```bash
npx -y convex@latest mcp start --dangerously-enable-production-deployments
```

Treat this as dangerous: it can read/modify production data.

## Deployment selection

From the Convex MCP docs:

- Default: development deployment
- Preview: `--preview-name <name>`
- Specific deployment: `--deployment-name <name>`
- Production: `--prod` requires `--dangerously-enable-production-deployments`

Always confirm the target deployment before running tools that mutate data (`run`, `envSet`, etc).

## Tooling model

The MCP server typically returns an opaque `deploymentSelector` from `status`. Pass that selector unchanged into subsequent calls.

## Recommended MCP workflow

1) Get deployments (first call)

```js
convex_status({ projectDir: "/path/to/repo" })
```

Pick the dev deployment selector by default.

2) Inspect API surface

```js
convex_functionSpec({ deploymentSelector })
```

3) Inspect schema/tables

```js
convex_tables({ deploymentSelector })
```

4) Verify logs before/after changes

```js
convex_logs({ deploymentSelector })
```

5) Run a function with args (confirm first)

```js
convex_run({
  deploymentSelector,
  functionName: "path/to/module.ts:exportName",
  args: JSON.stringify({})
})
```

6) Run a sandboxed one-off read query (safe)

```js
convex_runOneoffQuery({
  deploymentSelector,
  query: `import { query } from "convex:/_system/repl/wrappers.js";

export default query({
  handler: async (ctx) => {
    return await ctx.db.query("users").take(5);
  },
});`
})
```

## Available MCP tools (common)

The official Convex MCP docs list tools in these categories:

- Deployment: `status`
- Tables/data: `tables`, `data`, `runOneoffQuery`
- Functions: `functionSpec`, `run`, `logs`
- Env vars: `envList`, `envGet`, `envSet`, `envRemove`

## Compatibility note

Different agents expose the Convex MCP tools under different names.

Use the conceptual tool names from the Convex docs (status/tables/functionSpec/run/logs/etc), then map them to whatever your agent provides.

## Docs and components verification

Use MCP introspection to reduce guesswork:

- `functionSpec` to confirm what is deployed (names, args, visibility)
- `tables` to confirm table names and declared/inferred schema

Then verify the latest docs and components list:

- https://docs.convex.dev/
- https://docs.convex.dev/components

In this environment, those map to tools named:

- `convex_status`
- `convex_tables`
- `convex_data`
- `convex_runOneoffQuery`
- `convex_functionSpec`
- `convex_run`
- `convex_logs`
- `convex_envList` / `convex_envGet` / `convex_envSet` / `convex_envRemove`
