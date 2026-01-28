# Agent Skills

Public collection of AI agent skills by [@bntvllnt](https://github.com/bntvllnt)

**Compatible with:** Claude Code • OpenCode • Windsurf • Cursor • More via [skills.sh](https://skills.sh)

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

## Installation

Install specific skills from this collection:

```bash
# Install the analyze skill
npx skills add bntvllnt/agent-skills --skill analyze

# Or install all skills
npx skills add bntvllnt/agent-skills --all
```

The CLI will prompt you to choose installation location and target agent.

**Quick options:**
```bash
# Global install
npx skills add bntvllnt/agent-skills --skill analyze -g

# Specific agent
npx skills add bntvllnt/agent-skills --skill analyze --agent claude-code

# Install all without prompts
npx skills add bntvllnt/agent-skills --all -g --agent claude-code
```

---

## Usage Examples

```bash
# Quick analysis
analyze quick "our pricing strategy"

# Standard analysis (default)
analyze "SaaS product for developers"

# Deep analysis
analyze deep "migration to microservices"

# Analyze files
analyze src/auth.ts
analyze package.json

# Personal decisions
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

---

## Author

**bntvllnt** ([github](https://github.com/bntvllnt) | [web](https://bntvllnt.com))
