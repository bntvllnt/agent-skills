# Clerk

Official docs:

- https://docs.convex.dev/auth/clerk
- https://clerk.com/docs/guides/development/integrations/databases/convex

Use when the app already uses Clerk or the user wants hosted auth features.

## Workflow

1. Confirm user wants Clerk
2. Ensure user has Clerk account and application
3. Determine framework: React, Next.js, TanStack Start
4. Ask: local-only or production-ready?
5. Gather Clerk keys and Frontend API URL
6. Follow the correct framework section in official docs
7. Complete backend and client wiring
8. Verify Convex reports user as authenticated after login

## Concrete Steps

1. Create Clerk account at `https://dashboard.clerk.com/sign-up` (if needed)
2. Create Clerk app at `https://dashboard.clerk.com/apps/new` (if needed)
3. Copy publishable key from `https://dashboard.clerk.com/last-active?path=api-keys`
4. Open `https://dashboard.clerk.com/apps/setup/convex`
5. Activate Convex integration if not already active
6. Copy Clerk Frontend API URL
7. Install Clerk package for framework
8. Create/update `convex/auth.config.ts` with Clerk issuer domain
9. Set publishable key in frontend env
10. Set issuer domain for Convex JWT validation
11. Replace `ConvexProvider` with `ConvexProviderWithClerk`
12. Wrap app in `ClerkProvider`
13. Use Convex auth helpers (`Authenticated`, `Unauthenticated`, `AuthLoading`)
14. Run Convex dev/deploy flow after backend config changes

## Env Vars

- `CLERK_JWT_ISSUER_DOMAIN` -- Convex backend validation (same URL as `CLERK_FRONTEND_API_URL`)
- `VITE_CLERK_PUBLISHABLE_KEY` (Vite) or `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` (Next.js)
- `CLERK_SECRET_KEY` (Next.js server-side, where needed)

`CLERK_JWT_ISSUER_DOMAIN` and `CLERK_FRONTEND_API_URL` refer to the same value.

## Gotchas

- Prefer `useConvexAuth()` over raw Clerk auth state for Convex-authenticated UI decisions
- After changing `convex/auth.config.ts`, run Convex dev/deploy to sync
- "Clerk login works" is not enough -- verify Convex also sees the session
- If "no auth provider matched the token", confirm Clerk Convex integration was activated
- After activating integration, sign out completely and sign back in before retesting
- Do not assume dev and production Clerk values are the same
- For Next.js, mind server/client boundaries in the provider wrapper

## Validation

- Verify sign-in with Clerk
- If integration just activated, test after full sign-out + fresh sign-in
- Verify `useConvexAuth()` reaches authenticated state
- Verify protected Convex queries succeed
- Verify `ctx.auth.getUserIdentity()` is non-null
- If production requested, verify production Clerk config

## Checklist

- [ ] Confirmed user wants Clerk
- [ ] Asked local-only or production-ready
- [ ] Followed correct framework section in official guide
- [ ] Set Clerk environment variables
- [ ] Configured `convex/auth.config.ts`
- [ ] Verified Convex authenticated state after login
- [ ] If requested, configured production deployment
