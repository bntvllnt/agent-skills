# OSS Readiness

Open-source/public release readiness skill: audit repos for OSS basics, scaffold missing release docs/templates, generate `llms.txt` + `llms-full.txt`, validate CI, and sync version references.

## Install

```bash
npx skills add bntvllnt/agent-skills --skill oss-readiness
```

Global:

```bash
npx skills add bntvllnt/agent-skills --skill oss-readiness -g
```

## Quick Start

Use natural language or slash-command shorthand:

- `audit OSS readiness`
- `scaffold missing OSS files`
- `generate llms.txt`
- `bump stale version refs in docs`
- `check OSS CI readiness`
- `/oss`
- `/oss fix`
- `/oss llms`
- `/oss bump`
- `/oss ci`

## What It Covers

- Release docs: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`
- AI docs: `llms.txt`, `llms-full.txt`
- Repo hygiene: `.gitignore`, changelog, issue/PR templates, topics, description
- CI checks: test/lint coverage, optional publish workflow for libraries
- Agent instructions: canonical `AGENTS.md` plus optional harness-specific aliases

## Portability

This skill is designed to work across agent harnesses:

- `AGENTS.md` is the canonical instructions file when scaffolded
- `CLAUDE.md`, `.cursorrules`, `codex.md`, `.opencode/config`, etc. are optional aliases
- Generated templates use placeholders instead of maintainer-specific links or handles
- Shell tooling (`git`, `gh`, `node`, `python`) is optional — helpful, not required

## Reading Order

- Home/router: `oss-readiness/SKILL.md`
- Audit + scaffold logic: `oss-readiness/references/checklist.md`
- LLM docs generation: `oss-readiness/references/llms-generation.md`
- Version sync: `oss-readiness/references/version-sync.md`
- CI validation: `oss-readiness/references/ci-validation.md`
- Scaffold templates: `oss-readiness/templates/`

## Requirements

- Any agent that supports `SKILL.md` frontmatter + Markdown routing
- Optional CLI helpers: `git`, `gh`, `grep`, `find`, `jq`, `node`, or `python`
- Optional validator: `skills-ref validate ./oss-readiness`
