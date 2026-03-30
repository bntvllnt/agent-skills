# Better Auth

Official docs:

- https://www.better-auth.com/docs/introduction
- Convex integration: https://www.better-auth.com/docs/integrations/convex

Use when the user wants framework-agnostic auth with built-in Convex support, or wants features like email/password, social OAuth, 2FA, organizations, and a plugin ecosystem -- all running on Convex infrastructure.

## How It Works

Better Auth runs the entire auth instance on Convex infrastructure via `@convex-dev/better-auth`. No separate auth server needed. API routes proxy requests to the Convex deployment, which handles auth logic, database ops, and OAuth flows through Convex functions.

## Workflow

1. Confirm user wants Better Auth
2. Determine sign-in methods: email/password, social OAuth providers, 2FA
3. Ask: local-only or production-ready?
4. Read the Convex integration guide before writing code
5. Ensure `CONVEX_DEPLOYMENT` is configured (run `npx convex dev` first if not)
6. Install: `npm install better-auth @convex-dev/better-auth`
7. Set env vars via Convex CLI (not `.env.local`)
8. Create auth config, component definition, and register component
9. Create Better Auth instance and generate schema
10. Export adapter functions and mount HTTP routes
11. Create client instance and provider
12. Verify sign-in works
13. If production-ready, configure production deployment too

## Concrete Steps

### 1. Install

```bash
npm install better-auth @convex-dev/better-auth
```

### 2. Set environment variables

```bash
npx convex env set BETTER_AUTH_SECRET=$(openssl rand -base64 32)
npx convex env set SITE_URL http://localhost:3000
```

Auth-specific env vars (BETTER_AUTH_SECRET, OAuth client IDs/secrets) MUST be set via Convex CLI or dashboard, NOT `.env.local`.

`.env.local` only for:

```text
CONVEX_DEPLOYMENT=dev:adjective-animal-123
NEXT_PUBLIC_CONVEX_URL=https://adjective-animal-123.convex.cloud
NEXT_PUBLIC_CONVEX_SITE_URL=https://adjective-animal-123.convex.site
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### 3. Auth config

```ts
// convex/auth.config.ts
import { getAuthConfigProvider } from "@convex-dev/better-auth/auth-config";
import type { AuthConfig } from "convex/server";

export default {
  providers: [getAuthConfigProvider()],
} satisfies AuthConfig;
```

### 4. Component definition

```ts
// convex/betterAuth/convex.config.ts
import { defineComponent } from "convex/server";

const component = defineComponent("betterAuth");

export default component;
```

### 5. Register component

```ts
// convex/convex.config.ts
import { defineApp } from "convex/server";
import betterAuth from "./betterAuth/convex.config";

const app = defineApp();
app.use(betterAuth);

export default app;
```

### 6. Create Better Auth instance

```ts
// convex/betterAuth/auth.ts
import { createClient } from "@convex-dev/better-auth";
import { convex } from "@convex-dev/better-auth/plugins";
import type { GenericCtx } from "@convex-dev/better-auth/utils";
import type { BetterAuthOptions } from "better-auth";
import { betterAuth } from "better-auth";
import { components } from "../_generated/api";
import type { DataModel } from "../_generated/dataModel";
import authConfig from "../auth.config";
import schema from "./schema";

export const authComponent = createClient<DataModel, typeof schema>(
  components.betterAuth,
  {
    local: { schema },
    verbose: false,
  },
);

export const createAuthOptions = (ctx: GenericCtx<DataModel>) => {
  return {
    appName: "My App",
    baseURL: process.env.SITE_URL,
    secret: process.env.BETTER_AUTH_SECRET,
    database: authComponent.adapter(ctx),
    emailAndPassword: {
      enabled: true,
    },
    plugins: [convex({ authConfig })],
  } satisfies BetterAuthOptions;
};

export const options = createAuthOptions({} as GenericCtx<DataModel>);

export const createAuth = (ctx: GenericCtx<DataModel>) => {
  return betterAuth(createAuthOptions(ctx));
};
```

### 7. Generate schema

```bash
npx auth generate --config ./convex/betterAuth/auth.ts --output ./convex/betterAuth/schema.ts
```

### 8. Export adapter functions

```ts
// convex/betterAuth/adapter.ts
import { createApi } from "@convex-dev/better-auth";
import { createAuthOptions } from "./auth";
import schema from "./schema";

export const {
  create, findOne, findMany, updateOne, updateMany, deleteOne, deleteMany,
} = createApi(schema, createAuthOptions);
```

### 9. Mount HTTP routes

```ts
// convex/http.ts
import { httpRouter } from "convex/server";
import { authComponent, createAuth } from "./betterAuth/auth";

const http = httpRouter();
authComponent.registerRoutes(http, createAuth);

export default http;
```

### 10. Client instance

```ts
// lib/auth-client.ts
import { convexClient } from "@convex-dev/better-auth/client/plugins";
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  plugins: [convexClient()],
});
```

### 11. Server helpers (Next.js)

```ts
// lib/auth-server.ts
import { convexBetterAuthNextJs } from "@convex-dev/better-auth/nextjs";

export const {
  handler,
  preloadAuthQuery,
  isAuthenticated,
  getToken,
  fetchAuthQuery,
  fetchAuthMutation,
  fetchAuthAction,
} = convexBetterAuthNextJs({
  convexUrl: process.env.NEXT_PUBLIC_CONVEX_URL!,
  convexSiteUrl: process.env.NEXT_PUBLIC_CONVEX_SITE_URL!,
});
```

### 12. Route handler

```ts
// app/api/auth/[...all]/route.ts
import { handler } from "@/lib/auth-server";

export const { GET, POST } = handler;
```

### 13. Client provider

```tsx
// components/ConvexClientProvider.tsx
"use client";

import { ConvexBetterAuthProvider } from "@convex-dev/better-auth/react";
import { ConvexReactClient } from "convex/react";
import { authClient } from "@/lib/auth-client";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({
  children,
  initialToken,
}: {
  children: React.ReactNode;
  initialToken?: string | null;
}) {
  return (
    <ConvexBetterAuthProvider
      client={convex}
      authClient={authClient}
      initialToken={initialToken}
    >
      {children}
    </ConvexBetterAuthProvider>
  );
}
```

### 14. Wrap app layout

```tsx
// app/layout.tsx
import { ConvexClientProvider } from "@/components/ConvexClientProvider";
import { getToken } from "@/lib/auth-server";

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const token = await getToken();
  return (
    <html>
      <body>
        <ConvexClientProvider initialToken={token}>
          {children}
        </ConvexClientProvider>
      </body>
    </html>
  );
}
```

## Usage Patterns

### Backend: check identity

```ts
// convex/auth.ts
import { query } from "./_generated/server";

export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.auth.getUserIdentity();
  },
});
```

### Client: sign in

```ts
import { authClient } from "@/lib/auth-client";

await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
});
```

### SSR: preloaded queries

```ts
// Server component
const preloadedUser = await preloadAuthQuery(api.auth.getCurrentUser);

// Client component
import { usePreloadedAuthQuery } from "@convex-dev/better-auth/nextjs/client";
const user = usePreloadedAuthQuery(preloadedUser);
```

### Server: protect routes

```ts
import { isAuthenticated } from "@/lib/auth-server";

const hasToken = await isAuthenticated();
if (!hasToken) return <div>Unauthorized</div>;
```

## Gotchas

- `@convex-dev/better-auth` is maintained by Convex, not the Better Auth team. Check their GitHub for issues.
- Auth env vars (BETTER_AUTH_SECRET, OAuth secrets) MUST be set via `npx convex env set`, NOT `.env.local`. Convex functions read env vars from the deployment, not from local files.
- Run `npx auth generate` after changing auth options to regenerate the schema.
- The component uses `defineComponent` -- it runs as an isolated Convex component with its own tables.
- Better Auth runs entirely on Convex infrastructure. API routes are thin proxies.
- If `npx convex dev` is not running, generated types will be stale. Keep it running during setup.
- For frameworks other than Next.js, adapt the server helpers and route handlers to the framework's conventions.

## Validation

- Verify sign-up, sign-in, sign-out flow works end to end
- Verify `ctx.auth.getUserIdentity()` returns identity in protected backend functions
- Verify Convex hooks (`useQuery`) work with authenticated state
- Verify env vars are set on the Convex deployment (not just locally)
- If SSR, verify preloaded queries work with auth token
- If production requested, verify production deployment env vars and SITE_URL

## Checklist

- [ ] Confirmed user wants Better Auth
- [ ] Asked local-only or production-ready
- [ ] Installed `better-auth` and `@convex-dev/better-auth`
- [ ] Set BETTER_AUTH_SECRET and SITE_URL via `npx convex env set`
- [ ] Created auth config, component, and registered in `convex.config.ts`
- [ ] Created Better Auth instance in `convex/betterAuth/auth.ts`
- [ ] Generated schema with `npx auth generate`
- [ ] Exported adapter functions
- [ ] Mounted HTTP routes in `convex/http.ts`
- [ ] Created client instance and provider
- [ ] Set up route handler and wrapped app layout
- [ ] Verified sign-in and backend identity
- [ ] If requested, configured production deployment
