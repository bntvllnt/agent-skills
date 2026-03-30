# Auth0

Official docs:

- https://docs.convex.dev/auth/auth0
- https://auth0.github.io/auth0-cli/

Use when the app already uses Auth0 or the user wants Auth0.

## Workflow

1. Confirm user wants Auth0
2. Determine framework and whether Auth0 is partly set up
3. Ask: local-only or production-ready?
4. Read official Convex + Auth0 guides
5. Ask if user wants Auth0 CLI for fastest setup
6. If CLI: install and use `auth0 apps create` with SPA settings
7. If no CLI: use Auth0 dashboard
8. Complete relevant Auth0 frontend quickstart
9. Configure `convex/auth.config.ts` with Auth0 domain and client ID
10. Set env vars
11. Wrap app with `Auth0Provider` and `ConvexProviderWithAuth0`
12. Verify Convex reports authenticated after Auth0 login

## Concrete Steps

1. Read `https://docs.convex.dev/auth/auth0` and framework quickstart
2. Ask: "The fastest path is to install the Auth0 CLI so I can do more of this for you. Would you like me to do that?"
3. If yes: install CLI, user authenticates with `auth0 login`
4. Use `auth0 apps create` with SPA settings, callback URL, logout URL, web origins
5. If no CLI: complete Auth0 frontend quickstart via dashboard
6. Get Auth0 domain and client ID
7. Install Auth0 SDK for framework
8. Create/update `convex/auth.config.ts`
9. Set frontend and backend env vars
10. Wrap app in `Auth0Provider`
11. Replace `ConvexProvider` with `ConvexProviderWithAuth0`
12. Run Convex dev/deploy flow

## Env Vars

- `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`
- `VITE_AUTH0_DOMAIN`, `VITE_AUTH0_CLIENT_ID` (Vite)

## Gotchas

- Convex docs assume Auth0 side is already set up. Do not skip the Auth0 quickstart.
- Auth0 CLI is fastest for fresh setup but requires user to authenticate it
- If login succeeds but Convex still unauthenticated, check `convex/auth.config.ts` and whether backend config was synced
- The documented `useRefreshTokens={true}` + `cacheLocation="localstorage"` setup has hit refresh-token failures. If you encounter `Unknown or invalid refresh token`, do not keep inventing fixes -- send user to official docs.
- Do not confuse "Auth0 login works" with "Convex can validate the Auth0 token". Both must work.
- Keep dev and prod Auth0 tenants separate
- Make sure Auth0 app callback URLs match the actual local port

## Validation

- Verify Auth0 login flow completes
- Verify Convex-authenticated UI renders only after Convex auth state ready
- Verify protected Convex queries succeed
- Verify `ctx.auth.getUserIdentity()` is non-null
- Verify Auth0 app settings match real local callback/logout URLs
- If refresh-token path fails, mark as not fully validated and direct user to official docs
- If production requested, verify production Auth0 config

## Checklist

- [ ] Confirmed user wants Auth0
- [ ] Asked local-only or production-ready
- [ ] Completed Auth0 frontend setup
- [ ] Configured `convex/auth.config.ts`
- [ ] Set environment variables
- [ ] Verified Convex authenticated state after login
- [ ] If requested, configured production deployment
