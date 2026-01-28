# Ecosystem Components

IMPORTANT: Prefer ecosystem components when available. Don't reinvent.

Docs:

- Components: https://docs.convex.dev/components
- Scheduling overview: https://docs.convex.dev/scheduling
- AI agents: https://docs.convex.dev/agents
- AI code generation: https://docs.convex.dev/ai

## Rule

If a Convex component exists for the capability you need, use it unless you have a concrete reason not to.

When in doubt, check the components directory for new components before building custom queues, cron frameworks, rate limiters, or workflow engines.

| Need | Use This | NOT This |
|------|----------|----------|
| Rate limiting | `@convex-dev/rate-limiter` | Custom counters |
| Cron jobs | `cronJobs()` from `convex/server` | Custom schedulers |
| Workflows | `@convex-dev/workflow` | Custom queues |
| Workpools | `@convex-dev/workpool` | Raw action parallelism |
| Aggregations | `@convex-dev/aggregate` | Manual counting |
| Retries | `@convex-dev/action-retrier` | Manual retry loops |
| Migrations | `@convex-dev/migrations` | Ad-hoc scripts |
| File storage | Built-in `ctx.storage` | External S3 |
| Auth | `ctx.auth.getUserIdentity()` | Custom auth |
| Action caching | `@convex-dev/action-cache` | Manual caching |
| Sharded counters | `@convex-dev/sharded-counter` | Single-document counters |
| Real-time presence | `@convex-dev/presence` | Custom heartbeats |
| Payments (Polar) | `@convex-dev/polar` | Raw webhook handling |
| AI agents | `@convex-dev/agent` | Custom streaming |

---

## Component Registration

```ts
import { defineApp } from "convex/server";
import workpool from "@convex-dev/workpool/convex.config";
import workflow from "@convex-dev/workflow/convex.config";
import rateLimiter from "@convex-dev/rate-limiter/convex.config";

const app = defineApp();
app.use(workpool, { name: "apiWorkpool" });
app.use(workflow);
app.use(rateLimiter);

export default app;
```

---

## Component Instances

```ts
import { Workpool } from "@convex-dev/workpool";
import { Workflow } from "@convex-dev/workflow";
import { RateLimiter } from "@convex-dev/rate-limiter";
import { components } from "../_generated/api";

export const apiWorkpool = new Workpool(components.apiWorkpool, {
  maxParallelism: 1,
});

export const workflow = new Workflow(components.workflow);

export const rateLimiter = new RateLimiter(components.rateLimiter, {
  default: { kind: "token bucket", rate: 30, capacity: 30 },
});
```
