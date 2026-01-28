# CLI Workflows (npx convex)

Official CLI docs: https://docs.convex.dev/cli

Environment docs:

- Preview deployments: https://docs.convex.dev/production/hosting/preview-deployments
- Deploy keys: https://docs.convex.dev/cli/deploy-key-types

## Configure / bootstrap

```bash
npx convex dev
```

This configures a project if `CONVEX_DEPLOYMENT` is not set and creates/updates generated code under `convex/_generated/`.

## Develop

Run dev sync (shows logs by default):

```bash
npx convex dev
```

Notes (from the Convex CLI docs):

- Running `npx convex dev` on a new machine will prompt you to log in or run locally.
- After login, a user token is stored at `~/.convex/config.json` and used for subsequent CLI commands.
- The project-specific deployment selection is commonly stored via `CONVEX_DEPLOYMENT` in `.env.local`.

Tail logs behavior (from docs):

```bash
npx convex dev --tail-logs always
npx convex dev --tail-logs disable
npx convex logs
```

## Run a function

```bash
npx convex run <functionName> '{"arg": "value"}'
```

Useful flags:

```bash
npx convex run <functionName> '{"arg": "value"}' --watch
npx convex run <functionName> '{"arg": "value"}' --push
npx convex run <functionName> '{"arg": "value"}' --prod
```

## Preview deployments

Convex preview deployments allow testing backend changes before production.

Key points from the docs:

- Preview deployments are automatically cleaned up after a time window.
- Initial data setup on a preview deployment is typically done by running a function.
- When re-deploying the same branch, the preview deployment is replaced.

See: https://docs.convex.dev/production/hosting/preview-deployments

## Inspect data

```bash
npx convex data
npx convex data <table>
```

## Env vars

```bash
npx convex env list
npx convex env get <name>
npx convex env set <name> <value>
npx convex env remove <name>
```

## Deploy

```bash
npx convex deploy
```

Deploy target selection follows the Convex CLI rules. In build pipelines, `CONVEX_DEPLOY_KEY` is commonly used.

See: https://docs.convex.dev/cli/deploy-key-types

## Agent mode (background agents)

Convex docs recommend agent mode for remote/background coding agents:

```bash
CONVEX_AGENT_MODE=anonymous npx convex dev --once
```
