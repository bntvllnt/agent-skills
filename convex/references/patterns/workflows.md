# Scheduling, Workflows, Workpools

Scheduling docs: https://docs.convex.dev/scheduling

## Rule

Schedule internal functions, not public `api.*` references.

## Options

- Built-in scheduled functions + crons for simple jobs.
- Components (workpool/workflow) for higher-level durability/retry/priority.

Component docs:

- https://docs.convex.dev/components

## Workpool (rate limiting / serialization)

This is useful when calling rate-limited external APIs from actions.

```ts
import { defineApp } from "convex/server";
import workpool from "@convex-dev/workpool/convex.config";

const app = defineApp();
app.use(workpool, { name: "externalApi" });

export default app;
```

## Workflow (durable multi-step)

Workflows are useful for long-running, multi-step jobs with retries/delays.

See also: `references/ecosystem.md`.

## Keep it up to date

Convex components evolve. Before choosing an approach, re-check:

- https://docs.convex.dev/components
- https://stack.convex.dev/
