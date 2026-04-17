# Changelog

All notable changes to this project will be documented in this file.

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
