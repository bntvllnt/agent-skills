# Contributing to {REPO_NAME}

Thanks for your interest in contributing.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold it. Report unacceptable behavior via {CODE_OF_CONDUCT_CONTACT}.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/{ORG}/{REPO}/issues) first
2. Use the [bug report template](https://github.com/{ORG}/{REPO}/issues/new?template=bug_report.yml)
3. Include: steps to reproduce, expected vs actual behavior, environment details, and relevant logs

### Suggesting Features

1. Check [existing requests](https://github.com/{ORG}/{REPO}/issues?q=label%3Aenhancement)
2. Use the [feature request template](https://github.com/{ORG}/{REPO}/issues/new?template=feature_request.yml)
3. Describe the problem you're solving, not just the proposed solution

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-change`
3. Make your changes
4. Run quality checks:
   ```bash
   {QUALITY_COMMANDS}
   ```
5. Commit using [conventional commits](https://www.conventionalcommits.org/) when they fit the repo workflow
6. Push and open a Pull Request against `{PRIMARY_BRANCH}`

## Development Setup

```bash
git clone {PROJECT_REPO_URL}.git
cd {REPO_NAME}
{SETUP_COMMANDS}
```

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Update tests for behavior changes
- Update docs for public behavior changes
- Ensure CI passes before requesting review
- Note any follow-up work or known limitations

## Style Guide

- Follow existing code patterns in the repository
- See [AGENTS.md](AGENTS.md) for repo-specific agent/developer conventions
- Avoid unrelated refactors in feature PRs

## First-Time Contributors

Look for issues labeled [`good first issue`](https://github.com/{ORG}/{REPO}/labels/good%20first%20issue).

## Community

- **Repository:** {PROJECT_REPO_URL}
- **Homepage / Docs:** {PROJECT_HOMEPAGE}
- **Support / Discussion:** {COMMUNITY_SUPPORT_URL}
- **Security Reporting:** {SECURITY_REPORTING_URL}
- **Maintainer / Org:** [{MAINTAINER_NAME}]({MAINTAINER_URL})
- **Optional Contact:** {MAINTAINER_CONTACT_URL}

Remove optional rows the target project does not use.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project ({LICENSE_TYPE}).
