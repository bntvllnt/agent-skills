# HTTP Actions

HTTP actions docs: https://docs.convex.dev/functions/http-actions

## Pattern

Use `httpRouter()` and `httpAction()` to expose webhook endpoints.

Remember:

- validate signatures
- avoid logging secrets
- call internal mutations for sensitive writes

## Minimal shape

```ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/health",
  method: "GET",
  handler: httpAction(async () => {
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
```
