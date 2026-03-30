# Convex Auth

Official docs:

- https://docs.convex.dev/auth/convex-auth
- Setup guide: https://labs.convex.dev/auth/setup

Use when the user wants auth handled directly in Convex.

## Workflow

1. Confirm user wants Convex Auth
2. Determine sign-in methods: magic links/OTPs, OAuth, passwords
3. Ask: local-only or production-ready?
4. Read the setup guide before writing code
5. Ensure `CONVEX_DEPLOYMENT` is configured (run `npx convex dev` first if not)
6. Install: `npm install @convex-dev/auth @auth/core@0.37.0`
7. Run: `npx @convex-dev/auth`
8. Confirm created: `convex/auth.config.ts`, `convex/auth.ts`, `convex/http.ts`
9. Add `authTables` to `convex/schema.ts`
10. Replace `ConvexProvider` with `ConvexAuthProvider`
11. Configure auth methods in `convex/auth.ts`
12. Run `npx convex dev --once` to push schema
13. Verify sign-in works
14. If production-ready, configure production deployment too

## Gotchas

- Do not assume a sign-in method. Ask first.
- `npx @convex-dev/auth` is required -- it initializes key material. Do not skip.
- `npx @convex-dev/auth` fails without `CONVEX_DEPLOYMENT`. Run `npx convex dev` first.
- `npx convex dev` may require interactive setup. Ask the user for that step.
- `npx @convex-dev/auth` does not finish the integration alone. Still need `authTables`, `ConvexAuthProvider`, and at least one auth method.
- A successful build with `providers: []` does NOT mean auth is configured.
- Convex Auth manages user records internally. Do NOT add a parallel `users` table + `storeUser` unless the app needs app-level user records.
- If app is greenfield, prefer the official starter flow over hand-wiring.
- Do not stop at local dev if user expects production-ready auth.

## Validation

- Verify sign-in, sign-out, and sign-back-in flow
- Verify `ctx.auth.getUserIdentity()` returns identity in backend functions
- Verify `convex/auth.ts` no longer has empty `providers: []`
- Run `npx convex dev --once` after changes and confirm push succeeds
- If production requested, verify production deployment too

## Checklist

- [ ] Confirmed user wants Convex Auth
- [ ] Asked local-only or production-ready
- [ ] Ensured Convex deployment configured
- [ ] Installed `@convex-dev/auth` and `@auth/core@0.37.0`
- [ ] Ran `npx @convex-dev/auth`
- [ ] Confirmed generated files exist
- [ ] Added `authTables` to schema
- [ ] Replaced `ConvexProvider` with `ConvexAuthProvider`
- [ ] Configured at least one auth method
- [ ] Ran `npx convex dev --once`
- [ ] Verified sign-in and backend identity
- [ ] If requested, configured production deployment
