# WorkOS AuthKit

Official docs:

- https://docs.convex.dev/auth/authkit/
- https://docs.convex.dev/auth/authkit/add-to-app
- https://docs.convex.dev/auth/authkit/auto-provision

Use when the app already uses WorkOS or the user wants AuthKit.

## Workflow

1. Confirm user wants WorkOS AuthKit
2. Determine: Convex-managed WorkOS team or existing WorkOS team
3. Ask: local-only or production-ready?
4. Read official Convex + WorkOS AuthKit guide
5. Create/update `convex.json` with `authKit` section for framework and local port
6. Follow the correct setup branch
7. Configure WorkOS env vars
8. Configure `convex/auth.config.ts` for WorkOS JWTs
9. Wire client provider and callback flow
10. Verify authenticated requests reach Convex

## Concrete Steps

1. Choose Convex-managed or existing WorkOS team
2. Create/update `convex.json` with `authKit` section
3. Ensure `redirectUris`, `appHomepageUrl`, `corsOrigins` match actual local port
4. Managed team: run `npx convex dev` and follow interactive onboarding
5. Existing team: get `WORKOS_CLIENT_ID` and `WORKOS_API_KEY` from WorkOS dashboard, set with `npx convex env set`
6. Create/update `convex/auth.config.ts`
7. Run Convex dev/deploy flow
8. Wire WorkOS client provider
9. Configure callback and redirect handling
10. Verify sign-in and return to app

## Env Vars

- `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_COOKIE_PASSWORD`
- `VITE_WORKOS_CLIENT_ID`, `VITE_WORKOS_REDIRECT_URI` (Vite)
- `NEXT_PUBLIC_WORKOS_REDIRECT_URI` (Next.js)

For managed teams, `convex dev` can write local env vars to `.env.local`.

## Gotchas

- The docs split setup between managed and existing teams -- ask which path
- `convex.json` is NOT optional for the managed AuthKit flow
- If frontend starts on a different port than `convex.json`, the callback URL will be wrong. Update `convex.json`, update redirect env var, run `npx convex dev` again.
- Vite can fall off port `5173` if other apps are running. Do not assume default port.
- A successful WorkOS sign-in should redirect back and reach Convex-authenticated state. Do not stop at "the hosted page loaded."
- Keep dev and prod WorkOS config separate
- Only add `storeUser` / `users` table if app needs app-level user rows

## Validation

- Verify complete login flow (sign in, redirect back, authenticated state)
- Verify callback URL matches real frontend port
- Verify Convex receives authenticated requests
- Verify `convex.json` matches framework and setup path
- Verify `convex/auth.config.ts` matches setup path
- If production requested, verify production WorkOS config

## Checklist

- [ ] Confirmed user wants WorkOS AuthKit
- [ ] Asked local-only or production-ready
- [ ] Chose Convex-managed or existing team
- [ ] Created/updated `convex.json`
- [ ] Configured WorkOS env vars
- [ ] Configured `convex/auth.config.ts`
- [ ] Verified authenticated requests after login
- [ ] If requested, configured production deployment
