# Quickstart

Upstream canonical: if the `convex-quickstart` skill from `get-convex/agent-skills` is installed, prefer it. This file is the local fallback and supplements upstream with project conventions.

Docs: https://docs.convex.dev/quickstart

Skip when: project already has `convex/` directory and `CONVEX_DEPLOYMENT` configured.

## Path 1: New Project (Recommended)

Use the official scaffolding tool:

```bash
npm create convex@latest my-app -- -t <template>
cd my-app
npm install
```

### Templates

| Template | Stack |
|----------|-------|
| `react-vite-shadcn` | React + Vite + Tailwind + shadcn/ui |
| `nextjs-shadcn` | Next.js App Router + Tailwind + shadcn/ui |
| `react-vite-clerk-shadcn` | React + Vite + Clerk auth + shadcn/ui |
| `nextjs-clerk` | Next.js + Clerk auth |
| `nextjs-convexauth-shadcn` | Next.js + Convex Auth + shadcn/ui |
| `nextjs-lucia-shadcn` | Next.js + Lucia auth + shadcn/ui |
| `bare` | Convex backend only, no frontend |

Default: `react-vite-shadcn` for simple apps, `nextjs-shadcn` for SSR/API routes.

Custom GitHub template:

```bash
npm create convex@latest my-app -- -t owner/repo
npm create convex@latest my-app -- -t owner/repo#branch
```

To scaffold in the current (empty) directory:

```bash
npm create convex@latest . -- -t react-vite-shadcn
npm install
```

### Start the Dev Loop

`npx convex dev` is a long-running watcher that requires browser-based OAuth on first run. Ask the user to run it themselves. Once running it will:

- Create a Convex project and dev deployment
- Write the deployment URL to `.env.local`
- Create `convex/` with generated types
- Watch for changes and sync continuously

Exception: cloud/headless agents should use Agent Mode (see below).

Start frontend in a separate terminal:

```bash
npm run dev
```

### What You Get

```text
my-app/
  convex/           # Backend functions and schema
    _generated/     # Auto-generated types (check into git)
    schema.ts       # Database schema
  src/              # Frontend (or app/ for Next.js)
  package.json
  .env.local        # Deployment URL env var
```

## Path 2: Add Convex to Existing App

### Install

```bash
npm install convex
```

Ask the user to run `npx convex dev` to initialize.

### Wire Up the Provider

Create `ConvexReactClient` at module scope, not inside a component.

#### React (Vite)

```tsx
// src/main.tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import App from "./App";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL as string);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConvexProvider client={convex}>
      <App />
    </ConvexProvider>
  </StrictMode>,
);
```

#### Next.js (App Router)

```tsx
// app/ConvexClientProvider.tsx
"use client";

import { ConvexProvider, ConvexReactClient } from "convex/react";
import { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

```tsx
// app/layout.tsx
import { ConvexClientProvider } from "./ConvexClientProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ConvexClientProvider>{children}</ConvexClientProvider>
      </body>
    </html>
  );
}
```

#### Other Frameworks

- [Vue](https://docs.convex.dev/quickstart/vue)
- [Svelte](https://docs.convex.dev/quickstart/svelte)
- [React Native](https://docs.convex.dev/quickstart/react-native)
- [TanStack Start](https://docs.convex.dev/quickstart/tanstack-start)
- [Remix](https://docs.convex.dev/quickstart/remix)
- [Node.js (no frontend)](https://docs.convex.dev/quickstart/nodejs)

### Environment Variables

| Framework | Variable |
|-----------|----------|
| Vite | `VITE_CONVEX_URL` |
| Next.js | `NEXT_PUBLIC_CONVEX_URL` |
| Remix | `CONVEX_URL` |
| React Native | `EXPO_PUBLIC_CONVEX_URL` |

`npx convex dev` writes the correct variable to `.env.local` automatically.

## Agent Mode (Cloud and Headless Agents)

Set `CONVEX_AGENT_MODE=anonymous` for environments that cannot open a browser for login:

```bash
CONVEX_AGENT_MODE=anonymous npx convex dev
```

Add to `.env.local` or set inline. Runs a local anonymous deployment without authentication.

## Verify Setup

1. User confirms `npx convex dev` running without errors
2. `convex/_generated/` exists with `api.ts` and `server.ts`
3. `.env.local` contains deployment URL

## First Function (Smoke Test)

`convex/schema.ts`:

```ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    text: v.string(),
    completed: v.boolean(),
  }),
});
```

`convex/tasks.ts`:

```ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

export const create = mutation({
  args: { text: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("tasks", { text: args.text, completed: false });
  },
});
```

Usage in React:

```tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function Tasks() {
  const tasks = useQuery(api.tasks.list);
  const create = useMutation(api.tasks.create);

  return (
    <div>
      <button onClick={() => create({ text: "New task" })}>Add</button>
      {tasks?.map((t) => <div key={t._id}>{t.text}</div>)}
    </div>
  );
}
```

## Dev vs Production

- `npx convex dev` for development (personal dev deployment, syncs on save)
- `npx convex deploy` for production (separate deployment, do not use during dev)

## Next Steps

- Add auth: `references/auth-setup.md`
- Design schema: `references/patterns/schemas.md`
- Build components: `references/components.md`
- Plan migrations: `references/migrations.md`
