# {REPO_NAME}

> {DESCRIPTION}

`AGENTS.md` is the canonical agent-instructions file for this repository.
Optional harness-specific aliases (for example `CLAUDE.md`, `.cursorrules`, `codex.md`, or `.opencode/config`) may mirror this file when needed.

## Project Overview

- **Tech Stack:** {STACK_WITH_VERSIONS}
- **Runtime(s):** {RUNTIMES}
- **Package Manager / Tooling:** {TOOLCHAIN}
- **License:** {LICENSE_TYPE}

## Repository Layout

```text
{REPO_NAME}/
├── src/            # Main source code
├── tests/          # Automated tests
├── docs/           # Human-facing docs
├── .github/        # CI, issue templates, PR template
└── {ENTRY_FILES}   # Main entrypoints / package metadata
```

Adjust the layout example to match the actual repository.

## Common Commands

| Command | Purpose |
|---|---|
| `{INSTALL_COMMAND}` | Install dependencies / bootstrap environment |
| `{LINT_COMMAND}` | Run lint / formatting checks |
| `{BUILD_COMMAND}` | Build / package the project |
| `{TEST_COMMAND}` | Run automated tests |
| `{DEV_COMMAND}` | Start local development workflow |

Remove commands that do not exist for the target repo.

## Code Style

- **Languages:** {LANGUAGE_GUIDELINES}
- **Formatting/Linting:** {LINT_TOOLING}
- **Testing:** {TEST_TOOLING}
- **Validation:** {VALIDATION_APPROACH}
- **Naming:** {NAMING_CONVENTIONS}

Fill this section from the repo's actual conventions. Do not assume TypeScript, Node.js, or any single framework.

## Git Workflow

- Branch from `{PRIMARY_BRANCH}`
- Prefer conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `perf:`
- Open focused PRs with passing CI before merge
- Document any repo-specific merge strategy here

## Boundaries

**Always:**
- Follow existing code patterns
- Update tests when behavior changes
- Update docs when public behavior changes

**Ask first:**
- Adding new dependencies or services
- Changing public APIs or schemas
- Modifying CI/CD or release automation
- Touching security-sensitive configuration

**Never:**
- Commit secrets, credentials, or private keys
- Rewrite shared history without approval
- Disable quality gates without documenting why

## Support / Community

- **Repository:** {PROJECT_REPO_URL}
- **Homepage / Docs:** {PROJECT_HOMEPAGE}
- **Support / Discussion:** {COMMUNITY_SUPPORT_URL}
- **Security Reporting:** {SECURITY_REPORTING_URL}
- **Maintainer / Org:** [{MAINTAINER_NAME}]({MAINTAINER_URL})
- **Optional Contact:** {MAINTAINER_CONTACT_URL}

Remove optional rows that the target project does not use.
