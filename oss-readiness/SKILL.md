---
name: oss-readiness
description: |
  Open-source/public release readiness gate. Audit repos for OSS basics, scaffold missing public-release files,
  generate llms.txt + llms-full.txt, validate CI, and sync version references.
  Triggers: "oss", "/oss", "open source readiness", "release readiness", "public release",
  "go public", "oss audit", "llms.txt", "generate llms", "version bump docs", "scaffold OSS files".
compatibility: Agent Skills spec (agentskills.io). Works with any agent product that supports SKILL.md frontmatter + Markdown. Optional CLI helpers: git, gh, grep, find, jq, node or python.
metadata:
  version: "0.2"
---

# OSS Readiness — Public Release Gate

Audit a repository for open-source release basics. Scaffold missing public docs/templates.
Generate AI-friendly docs (`llms.txt`, `llms-full.txt`). Validate CI. Sync version references.

## Portability Rules

This skill must stay **harness-agnostic** and **maintainer-agnostic**:

- Accept natural-language prompts and slash-command shorthand as equivalent entry points.
- Keep `AGENTS.md` as the canonical agent-instructions file when one is scaffolded.
- Treat harness-specific files such as `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `codex.md`, or `.opencode/config` as optional aliases/mirrors — never the only supported path.
- Use placeholders in generated files. Never hardcode links, social handles, org names, or contact methods from this repository.
- Never invent maintainer contact channels. If the project does not provide one, leave a clear placeholder or omit the optional section.

## Required Capabilities

| Capability | Used For | Required | Fallback |
|---|---|---|---|
| File read/write/edit | Audit and scaffold docs/templates | Yes | — |
| Shell access | git/gh/grep/find-based checks | Recommended | Manual file inspection |
| `git` | Repo metadata, tags, tracked-file checks | Recommended | Filesystem-only audit |
| `gh` | GitHub metadata, PR/issue/security settings | Optional | Report as unchecked/manual |
| `node` or `python` | Manifest/version extraction helpers | Optional | Grep/parse text manually |

The skill still works without shell tooling. Shell commands are accelerators, not requirements.

## Entry Points

Use either natural language or shorthand. Route both to the same workflow.

| Intent | Example prompts | Route |
|---|---|---|
| Full audit | `audit OSS readiness`, `/oss` | `references/checklist.md` |
| Scaffold missing files | `scaffold missing OSS files`, `/oss fix` | `references/checklist.md` |
| Generate LLM docs | `generate llms.txt`, `/oss llms` | `references/llms-generation.md` |
| Sync version refs | `bump stale version refs in docs`, `/oss bump` | `references/version-sync.md` |
| Validate CI | `check OSS CI readiness`, `/oss ci` | `references/ci-validation.md` |

## Template Variables

Scaffolded files should use these placeholders until the target repo values are known:

| Placeholder | Meaning |
|---|---|
| `{REPO_NAME}` | Repository/project name |
| `{ORG}` / `{REPO}` | Git hosting owner + repo slug |
| `{DESCRIPTION}` | One-line project description |
| `{LICENSE_TYPE}` | Chosen OSS license |
| `{PRIMARY_BRANCH}` | Default branch name |
| `{PROJECT_REPO_URL}` | Canonical source repository URL |
| `{PROJECT_HOMEPAGE}` | Public project or docs homepage |
| `{COMMUNITY_SUPPORT_URL}` | Support/discussion channel |
| `{SECURITY_REPORTING_URL}` | Private vulnerability reporting channel |
| `{CODE_OF_CONDUCT_CONTACT}` | Contact path for conduct reports |
| `{MAINTAINER_NAME}` | Maintainer or org display name |
| `{MAINTAINER_URL}` | Maintainer/org profile or homepage |
| `{MAINTAINER_CONTACT_URL}` | Optional generic contact page/social/profile |

If a value is unknown, keep the placeholder or omit the optional block. Never substitute repo-specific defaults from this skill repository.

## Stack Detection

Detect project type to customize audit logic:

```bash
# Package manager / language hints
IS_NPM=$(test -f package.json && echo true || echo false)
IS_CARGO=$(test -f Cargo.toml && echo true || echo false)
IS_PYTHON=$(test -f pyproject.toml -o -f setup.py && echo true || echo false)
IS_GO=$(test -f go.mod && echo true || echo false)

# Library/package vs app (heuristics)
# npm: package.json has "main" or "exports"
# cargo: Cargo.toml has [lib]
# python: pyproject has build metadata / published package info
# go: cmd/ often implies app; library repos may omit it
```

## Checklist Summary (23 items)

### BLOCKING (12) — must fix before public release

| # | Item | Severity |
|---|---|---|
| 1 | LICENSE file | BLOCKING |
| 2 | README.md exists | BLOCKING |
| 3 | README.md quality (H1, desc, install, usage, license) | BLOCKING |
| 4 | CONTRIBUTING.md | BLOCKING |
| 5 | .gitignore | BLOCKING |
| 6 | No secrets in repo | BLOCKING |
| 7 | CI: tests run | BLOCKING |
| 8 | CI: lint runs | BLOCKING |
| 9 | GitHub description set | BLOCKING |
| 10 | CHANGELOG.md with version entry | BLOCKING |
| 11 | llms.txt exists | BLOCKING |
| 12 | llms-full.txt exists | BLOCKING |

### WARN (11) — recommended

| # | Item | Severity |
|---|---|---|
| 13 | GitHub topics/tags | WARN |
| 14 | AGENTS.md | WARN |
| 15 | Harness-specific agent-instruction aliases | WARN |
| 16 | SECURITY.md | WARN |
| 17 | CODE_OF_CONDUCT.md | WARN |
| 18 | Issue templates | WARN |
| 19 | PR template | WARN |
| 20 | CI: publish workflow (libraries) | WARN |
| 21 | docs/ folder | WARN |
| 22 | Version in docs matches package | WARN |
| 23 | No TODO/FIXME in public src/ | WARN |

Full detection logic + fix actions → [references/checklist.md](references/checklist.md)

## Scoring

```text
SCORE = (blocking_pass / blocking_total) * 70 + (warn_pass / warn_total) * 30

A = score >= 90 AND 0 blocking failures
B = score >= 75 AND 0 blocking failures
C = score >= 60 (some blocking failures)
D = score >= 40
F = score < 40

Any blocking failure caps grade at C maximum.
```

## Audit Output Format

```text
═══════════════════════════════════════════════════════════════
 OSS READINESS — {org}/{repo}
 Version: {version} | Type: {npm|cargo|pip|go|app}
 Grade: {A-F} | Score: {0-100}
═══════════════════════════════════════════════════════════════

 BLOCKING
 ┌────────────────────────────────┬──────────┬───────────────────────┐
 │ Item                           │ Status   │ Note                  │
 ├────────────────────────────────┼──────────┼───────────────────────┤
 │ LICENSE                        │ PASS     │ MIT detected          │
 │ README.md                      │ WARN     │ Missing: usage, API   │
 │ llms.txt                       │ FAIL     │ Not found             │
 └────────────────────────────────┴──────────┴───────────────────────┘

 RECOMMENDED
 ┌────────────────────────────────┬──────────┬───────────────────────┐
 │ AGENTS.md                      │ FAIL     │ Not found             │
 │ Agent aliases                  │ WARN     │ AGENTS.md only        │
 └────────────────────────────────┴──────────┴───────────────────────┘

 BLOCKING failures: 2 — must fix before public release
 Warnings: 1 — recommended

 Run `scaffold missing OSS files` or `/oss fix` to scaffold missing files.
 Run `generate llms.txt` or `/oss llms` to create llms docs.
═══════════════════════════════════════════════════════════════
```

## Scaffold Order

```text
1. Detect stack (npm/cargo/python/go/app)
2. Run full checklist → identify missing items
3. Present: "Missing N BLOCKING + M WARN items. Scaffold all? [all / blocking only / pick]"
4. For each item:
   a. LICENSE → ask user for license type (MIT/Apache-2.0/ISC/GPL-3.0/BSD-3-Clause)
   b. README.md → scaffold from template placeholders
   c. CONTRIBUTING.md → fill template with repo + branch strategy
   d. SECURITY.md → fill template with repo + reporting channel placeholders
   e. CODE_OF_CONDUCT.md → fill Contributor Covenant template + conduct contact placeholder
   f. AGENTS.md → analyze repo, generate canonical instructions file
   g. Optional aliases → ask which harness aliases to create from AGENTS.md
   h. llms.txt + llms-full.txt → route to llms generation flow
   i. Issue templates → create .github/ISSUE_TEMPLATE/
   j. PR template → create .github/pull_request_template.md
   k. GitHub description/topics → update via `gh` when available
   l. CI workflows → generate starter workflow(s) based on stack
5. Report scaffolded files
6. Suggest re-running the audit before commit/push
```

## Error Handling

| Error | Response |
|---|---|
| Not a git repo | "Not a git repository. OSS audit requires a repo." |
| Private repo | Works but warns: "Repo is private. Audit shows readiness for going public." |
| No package manager | Skip version-specific checks, note in output |
| `gh` unavailable/auth missing | Continue filesystem checks; mark GitHub metadata as manual |
| Maintainer contact unknown | Keep placeholder or omit optional contact block |

## References

- [Checklist](references/checklist.md) — full detection + fix logic for all 23 items
- [LLMs Generation](references/llms-generation.md) — `llms.txt` + `llms-full.txt` algorithm
- [Version Sync](references/version-sync.md) — version detection + doc bumping
- [CI Validation](references/ci-validation.md) — CI pipeline rules + starter workflows

## Templates

All scaffold templates live in `templates/`. Keep them generic and placeholder-driven.