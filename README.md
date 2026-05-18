<div align="center">

# 🎯 Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/skills-8-blue.svg)](./#available-skills)
[![Release](https://img.shields.io/github/v/release/bntvllnt/agent-skills?display_name=tag&sort=semver)](https://github.com/bntvllnt/agent-skills/releases/latest)

**Compatible with:** Claude Code • OpenCode • Windsurf • Cursor • More via [skills.sh](https://skills.sh)

[GitHub](https://github.com/bntvllnt) • [Twitter](https://twitter.com/bntvllnt) • [Web](https://bntvllnt.com)

</div>

---

## Installation

```bash
npx skills add bntvllnt/agent-skills
```

---

## Available Skills

### [Analyze](./analyze/) - Universal Multi-Perspective Analyzer

Multi-perspective analysis for any topic, file, idea, or decision. Three modes: quick, standard, deep.

[View skill documentation →](./analyze/SKILL.md)

---

### [Skill Builder](./skill-builder/) - Build Correct Skills

Create/update/delete skills with validated templates, safe defaults, and cross-skill consistency checks.

[View skill documentation →](./skill-builder/SKILL.md)

---

### [OSS Readiness](./oss-readiness/) - Public Release Gate

Audit repos for OSS release readiness, scaffold missing public docs/templates, generate `llms.txt`/`llms-full.txt`, validate CI, and sync version references.

[View skill documentation →](./oss-readiness/SKILL.md)

---

### [Git](./git/) - Git Workflow + Worktrees + PRs

Unified git workflow: branch-first commits, worktree management, and PR creation/review flows.

[View skill documentation →](./git/SKILL.md)

---

### [GitHub](./github/) - GitHub CLI (gh)

GitHub operations via `gh` CLI: repos, issues, PRs, Actions, releases, and CI monitoring.

[View skill documentation →](./github/SKILL.md)

---

### [Convex](./convex/) - Convex Backend + MCP

Build and operate Convex backends with best practices, validation, and Convex MCP workflows.

[View skill documentation →](./convex/SKILL.md)

---

### [Workflow](./workflow/) - High-Velocity Solo Development

Idea to production same-day. Spec-first, quality-gated development: plan, spike, ship, fix, review, done, drop.

[View skill documentation →](./workflow/SKILL.md)

---

### [tmux](./tmux/) - Terminal Multiplexer Management

Complete tmux management: sessions, windows, panes, layouts, and scripting/automation.

[View skill documentation →](./tmux/SKILL.md)

---

## Installation Options

Install specific skill:

```bash
npx skills add bntvllnt/agent-skills --skill analyze

npx skills add bntvllnt/agent-skills --skill skill-builder

npx skills add bntvllnt/agent-skills --skill oss-readiness

npx skills add bntvllnt/agent-skills --skill git

npx skills add bntvllnt/agent-skills --skill github

npx skills add bntvllnt/agent-skills --skill convex

npx skills add bntvllnt/agent-skills --skill workflow

npx skills add bntvllnt/agent-skills --skill tmux
```

Global install:
```bash
npx skills add bntvllnt/agent-skills --skill analyze -g

npx skills add bntvllnt/agent-skills --skill skill-builder -g

npx skills add bntvllnt/agent-skills --skill oss-readiness -g

npx skills add bntvllnt/agent-skills --skill git -g

npx skills add bntvllnt/agent-skills --skill github -g

npx skills add bntvllnt/agent-skills --skill convex -g

npx skills add bntvllnt/agent-skills --skill workflow -g

npx skills add bntvllnt/agent-skills --skill tmux -g
```

Specific agent:
```bash
npx skills add bntvllnt/agent-skills --skill analyze --agent claude-code

npx skills add bntvllnt/agent-skills --skill skill-builder --agent claude-code

npx skills add bntvllnt/agent-skills --skill oss-readiness --agent claude-code

npx skills add bntvllnt/agent-skills --skill git --agent claude-code

npx skills add bntvllnt/agent-skills --skill github --agent claude-code

npx skills add bntvllnt/agent-skills --skill convex --agent claude-code

npx skills add bntvllnt/agent-skills --skill workflow --agent claude-code

npx skills add bntvllnt/agent-skills --skill tmux --agent claude-code
```

---

## Usage Examples

Quick analysis:
```bash
analyze quick "our pricing strategy"
```

Standard analysis (default):
```bash
analyze "SaaS product for developers"
```

Deep analysis:
```bash
analyze deep "migration to microservices"
```

Analyze files:
```bash
analyze src/auth.ts
```

```bash
analyze package.json
```

Personal decisions:
```bash
analyze "should I accept this job offer"
```

---

## Contributing

This is a public collection of skills developed by [@bntvllnt](https://github.com/bntvllnt). 

Before opening a PR, run the repository validator:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
```

If you changed skill content or root documentation, refresh generated manifests first:

```bash
python scripts/validate_repo.py --write
```

The validator checks `SKILL.md` YAML frontmatter, required skill metadata, skill folder/name consistency, local Markdown links, and exact generated `llms.txt` / `llms-full.txt` manifest sync.

Feel free to:
- Fork and adapt for your needs
- Submit issues for bugs or improvement suggestions
- Share your own variations

---

## Community

- [Website](https://bntvllnt.com) — about the maintainer and projects
- [Discord](https://bntvllnt.com/discord) — questions, discussion, support
- [GitHub](https://bntvllnt.com/github) — issues, PRs, code
- [X / Twitter](https://bntvllnt.com/x) — updates, DMs for security
- [LinkedIn](https://bntvllnt.com/linkedin) — professional inquiries
- [Book a meeting](https://bntvllnt.com/book) — consultation, collaboration, or anything

---

## License

MIT License - Free to use, modify, and distribute.
