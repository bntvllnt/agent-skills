# {REPO_NAME}

> {DESCRIPTION}

This is the canonical agent-instructions file for this repository. `AGENTS.md` is a byte-identical
mirror of this file for tools that read `AGENTS.md` — edit **this** file, then regenerate the mirror
with `cp CLAUDE.md AGENTS.md`.

## Project Overview

- **Tech stack:** {STACK_WITH_VERSIONS}
- **Package manager / tooling:** {TOOLCHAIN}
- **Primary branch:** {PRIMARY_BRANCH}
- **License:** {LICENSE_TYPE}

## Common Commands

| Command | Purpose |
|---|---|
| `{INSTALL_COMMAND}` | Install dependencies / bootstrap |
| `{LINT_COMMAND}` | Lint / format checks |
| `{BUILD_COMMAND}` | Build / package |
| `{TEST_COMMAND}` | Run tests |
| `{DEV_COMMAND}` | Start local development |

Remove rows that do not apply.

## Rules

Modular rules live in `.claude/rules/`. Each is loaded on demand.

- @.claude/rules/git-workflow.md
- @.claude/rules/code-style.md
- @.claude/rules/security.md

When you add a rule file, add a matching `@.claude/rules/<name>.md` line above and re-run
`cp CLAUDE.md AGENTS.md`.

## Boundaries

**Always:** follow existing patterns; update tests when behavior changes; update docs on public
behavior change.

**Ask first:** new dependencies/services; public API or schema changes; CI/CD or release changes;
security-sensitive config.

**Never:** commit secrets; rewrite shared history without approval; disable quality gates without
documenting why.
