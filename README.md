<div align="center">

# 🎯 Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/skills-4-blue.svg)](./#available-skills)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/bntvllnt/agent-skills/releases)

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

Extract key points, find gaps/risks, identify improvements, and generate actionable plans for ANY topic, file, idea, or decision.

**Modes:**
- **Quick** (30-60s): Fast key points extraction
- **Standard** (2-4min): Multi-perspective analysis with 4-6 experts
- **Deep** (5-8min): Comprehensive analysis with 6-10 experts

**Use cases:**
- Business decisions ("analyze our pricing strategy")
- Code review ("analyze deep src/api/")
- Product ideas ("analyze 'habit tracking app'")
- Personal decisions ("analyze 'should I take this job'")
- Documents ("analyze proposal.md")
- Processes ("analyze 'hiring workflow'")

**Features:**
- ✅ Standalone - no external dependencies
- ✅ First-principles decomposition
- ✅ Failure hypothesis generation
- ✅ Multi-perspective synthesis
- ✅ Actionable roadmaps with dependencies
- ✅ Domain auto-detection (13 domains)
- ✅ Built-in perspectives library

[View skill documentation →](./analyze/SKILL.md)

---

### [Skill Builder](./skill-builder/) - Build Correct Skills

Create/update/delete skills with validated templates, safe defaults, and cross-skill consistency checks.

[View skill documentation →](./skill-builder/SKILL.md)

---

### [Git](./git/) - Git Workflow + Worktrees + PRs

Unified git workflow: branch-first, worktree-first, security-first commits, and PR creation/review flows.

[View skill documentation →](./git/SKILL.md)

---

### [GitHub](./github/) - Releases via gh

Create and verify GitHub Releases using GitHub CLI (`gh`).

[View skill documentation →](./github/SKILL.md)

---

## Installation Options

Install specific skill:

```bash
npx skills add bntvllnt/agent-skills --skill analyze

npx skills add bntvllnt/agent-skills --skill skill-builder

npx skills add bntvllnt/agent-skills --skill git

npx skills add bntvllnt/agent-skills --skill github
```

Global install:
```bash
npx skills add bntvllnt/agent-skills --skill analyze -g

npx skills add bntvllnt/agent-skills --skill skill-builder -g

npx skills add bntvllnt/agent-skills --skill git -g

npx skills add bntvllnt/agent-skills --skill github -g
```

Specific agent:
```bash
npx skills add bntvllnt/agent-skills --skill analyze --agent claude-code

npx skills add bntvllnt/agent-skills --skill skill-builder --agent claude-code

npx skills add bntvllnt/agent-skills --skill git --agent claude-code

npx skills add bntvllnt/agent-skills --skill github --agent claude-code
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

Feel free to:
- Fork and adapt for your needs
- Submit issues for bugs or improvement suggestions
- Share your own variations

---

## License

MIT License - Free to use, modify, and distribute.
