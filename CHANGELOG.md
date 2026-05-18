# Changelog

All notable changes to this project will be documented in this file.

## [1.13.7] - 2026-04-28

- docs: correct contributing guidance to open pull requests against `main`, matching the repository branch and CI target
- feat(convex): delegate canonical Convex content (quickstart, auth, components, migrations, performance) to upstream `get-convex/agent-skills` with fetchable raw GitHub URLs so agents can WebFetch upstream `SKILL.md` even when not installed locally; local references kept as fallback for project conventions; bump skill metadata 2.0 -> 2.1
- feat(convex): add `references/parallel-worktrees.md` with production-grade pattern for isolated per-worktree Convex dev backends. Primary path is a named cloud dev deployment (`dev/<slug>`) via `npx convex deployment select|create --type dev --select`, with a verified slug-derivation recipe (basename + sha1(host:abspath).slice(0,8)), lock-based ensure flow, cleanup via `deployment delete` or `--expiration` TTL, auth-failure recovery, and per-worktree port allocation. Anonymous mode (`CONVEX_AGENT_MODE=anonymous`) documented as the sandbox/CI fallback for environments that cannot OAuth. Includes a Common Errors section explaining why fresh worktrees see "login required" prompts (gitignored `.env.local` -> first-run setup flow), a decision tree for choosing how to populate env, a BLOCKING rule for agents to prompt the user before auto-creating cloud deployments, and a copy-paste `scripts/setup-convex-worktree.sh` that detects env state, prompts interactively when no `.env*` exists (with create-new / paste-URL / copy-from-primary options), and fails closed in non-interactive contexts.
- feat(convex): add `references/environments.md` documenting multi-deployment per project (staging-as-named-prod, production sharding) — officially supported per Convex docs ("production sharding, or staging setups"). Covers `npx convex deployment create <ref> --type prod`, `--default` semantics for `npx convex deploy`, `--deployment <ref>` for one-off targeting, promotion workflow (dev -> staging -> prod), per-deployment deploy keys, and when to use one project with named prods vs separate projects.
- fix(convex): clarify that not all upstream skills have `references/`, add supply-chain note about `main`-pinned URLs, surface 3-tier precedence in router table header, wrap reference-pointer URLs in angle brackets
- fix(convex): correct parallel-worktrees.md against the authoritative `npx convex deployment --help` — add the missing CONVEX_DEPLOYMENT bootstrap step that gives the Convex CLI project context (without it `deployment select|create` fails with "No CONVEX_DEPLOYMENT set"), remove the non-existent `npx convex deployment delete` claim (the CLI exposes only `select` and `create`; cloud-side delete is dashboard-only), document the strict teardown ordering (`dev:remove` before `git worktree remove` — once the worktree directory is gone the deployment ref becomes unrecoverable), and add a companion `scripts/teardown-convex-worktree.sh` that strips CONVEX_* keys while preserving unrelated env vars and prints the dashboard URL for manual cloud cleanup.

## [1.13.6] - 2026-04-25

- docs(git): clarify env file carry-over for new worktrees so local runtime config is copied intentionally

## [1.13.5] - 2026-04-18

- docs(skill-builder): make authoring guidance more portable across agent products with spec-aligned description, validation, and confirmation rules

## [1.13.4] - 2026-04-17

- fix(oss-readiness): make SKILL.md frontmatter valid YAML so strict indexers can parse the skill

## [1.13.3] - 2026-04-17

- feat(github): add release-title prerequisites and preview-aware release strategy guidance
- feat(oss-readiness): add OSS release messaging rubric for titles and opening summaries

## [1.13.2] - 2026-04-17

- feat(workflow): load rules-discovery across plan, ship, fix, focus, and spec-review

## [1.13.1] - 2026-04-17

- feat(workflow): require line-by-line change coverage and rule-by-rule rules enforcement in review mode
- docs(workflow): define a runtime-neutral portable review spec plus optional executor patterns for OSS-safe review portability

## [1.13.0] - 2026-04-15

- feat(oss-readiness): add harness-agnostic OSS/public release skill with audit, CI, llms, and scaffolding flows
- docs: list OSS Readiness in the README, skills overview, llms.txt, and llms-full.txt

## [1.12.0] - 2026-03-30

- feat(convex): expand skill to v2.0 with quickstart, components, migrations, performance, auth (#16)
- feat(convex): add Better Auth provider with full Convex integration guide
- feat(convex): align skill with @vllnt/eslint-config/convex conventions (14 critical rules)
- feat(convex): add lint-first rule recommending @vllnt/eslint-config/convex
- feat: add publish.yml with canary tags + manual release workflow (#17)
- feat: add CI workflow enforcing CHANGELOG.md update on every PR

## [1.10.1] - 2026-03-24

- feat(workflow,analyze): integrate codebase-intelligence CLI for TypeScript repos (#12)

## [1.10.0] - 2026-03-24

- feat(workflow): extract fix action from ship for dedicated bug fixing (#10)
- feat(workflow): add E2E-first testing with TDD enforcement & anti-regression (#11)
- feat(workflow): add PREVENT step to bug fix anti-cascade protocol (#9)
- docs(readme): standardize skill descriptions to concise one-liners

## [1.9.0] - 2026-03-22

- feat(workflow): add focus action for codebase priority analysis (#8)
- feat(workflow): add auto testing, agent self-improvement, anti-regression (#7)
- feat(workflow): add production-grade auto-selecting code review (#6)
- feat(tmux): add complete tmux management skill (#5)

## [1.8.0] - 2026-03-21

- feat(tmux): add complete tmux management skill (#5)

## [1.7.1] - 2026-03-20

- chore(workflow): tighten activation triggers to avoid cross-skill overlap
- chore(github): add sponsor funding config

## [1.7.0] - 2026-03-20

- feat(workflow): add "what's up" and variant triggers for status action
- feat(github): add CI monitor and PR dashboard
- docs(readme): update git skill description with worktree summary

## [1.6.0] - 2026-03-19

- feat(git): add worktree summary with proactive change analysis

## [1.5.1] - 2026-03-18

- feat(github): add strict release strategy and description format

## [1.5.0] - 2026-03-18

- feat(workflow): add structured adversarial analysis to planning

## [1.4.0] - 2026-03-17

- feat: add workflow skill (#1)
- fix: quote YAML compatibility value to avoid parse error
- fix: add missing frontmatter fields to workflow SKILL.md

## [1.3.1] - 2026-03-16

- fix(github): fix action router and reference loading

## [1.3.0] - 2026-03-16

- feat(github): add GitHub CLI skill

## [1.2.0] - 2026-03-15

- feat(git): add git workflow skill with worktree support

## [1.1.0] - 2026-03-14

- feat(skill-builder): add skill builder for creating/validating skills

## [1.0.0] - 2026-03-13

- feat: initial release with analyze skill
- feat(analyze): universal multi-perspective analyzer (quick/standard/deep modes)
