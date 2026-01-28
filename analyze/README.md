# Analyze Skill

Universal multi-perspective analyzer for any topic, file, idea, or decision.

## Quick Start

```bash
analyze "your topic"           # Standard mode (4-6 perspectives)
analyze quick "your topic"     # Fast mode (key points only)
analyze deep "your topic"      # Comprehensive (6-10 perspectives)
```

## What It Does

1. **Auto-detects domain** (business, product, software, personal, etc.)
2. **Selects expert perspectives** based on domain and mode
3. **Runs parallel analysis** with multiple expert agents
4. **Synthesizes findings** into actionable insights
5. **Generates roadmaps** with dependencies and priorities

## Features

- ✅ **Standalone** - No external dependencies
- ✅ **First-principles decomposition** - Challenges assumptions
- ✅ **Failure hypothesis generation** - Proactive risk identification
- ✅ **Multi-perspective synthesis** - Cross-cutting insights
- ✅ **Actionable roadmaps** - With dependencies and timelines
- ✅ **Domain auto-detection** - 13+ domains supported
- ✅ **Built-in perspectives** - 50+ expert roles included

## Modes

| Mode | Duration | Agents | Best For |
|------|----------|--------|----------|
| **Quick** | 30-60s | 0-1 | Fast key points, initial assessment |
| **Standard** | 2-4min | 4-6 | Balanced analysis, most use cases |
| **Deep** | 5-8min | 6-10 | Comprehensive, critical decisions |

## Supported Domains

- **Business** - Strategy, market analysis, revenue
- **Product** - Features, user needs, roadmap
- **Software** - Code, architecture, tech debt
- **Process** - Workflows, operations, SOP
- **Personal** - Career, life decisions
- **Financial** - Budget, investment, ROI
- **Marketing** - Campaigns, sales, brand
- **Legal** - Contracts, policy, terms
- **Creative** - Design, brand, visual
- **Research** - Study, hypothesis, data
- **Document** - Articles, proposals, reports
- **Event** - Launches, conferences
- **Education** - Curriculum, teaching
- **General** - Fallback for any topic

## Examples

### Business Decision
```bash
analyze quick "our pricing strategy"
```

**Output includes:**
- Verified facts with evidence
- Key points ranked by importance
- Assumptions to challenge
- What you haven't considered
- Quick actions with impact
- Critical risks

### Code Analysis
```bash
analyze deep src/api/
```

**Output includes:**
- Security vulnerabilities
- Performance bottlenecks
- Architecture issues
- Test coverage gaps
- Scalability concerns
- Maintainability assessment
- Actionable roadmap

### Personal Decision
```bash
analyze "should I take this job offer"
```

**Perspectives include:**
- Future You (1 year)
- Future You (5 years)
- Skeptic (risks/downsides)
- Supporter (opportunities)
- Financial Advisor
- Life Coach (values alignment)

## Output Format

### Quick Mode
- The Essence
- Verified Facts
- Key Points (Top 5-10)
- Assumptions to Challenge
- What You Haven't Considered
- The Real Question
- Quick Actions
- Critical Risk

### Standard Mode
Everything in Quick, plus:
- Executive Summary
- Failure Hypotheses
- Multi-perspective synthesis
- Gap Analysis
- Improvement Opportunities
- Action Plan with dependencies
- Cross-cutting Concerns

### Deep Mode
Everything in Standard, plus:
- Extended roadmap (immediate/short/medium/long-term)
- Dependency map
- Risk mitigation strategies
- More detailed hypotheses
- 12 questions per agent (vs 7)

## Installation

```bash
npx skills add bntvllnt/agent-skills --skill analyze
```

The CLI will prompt you to choose installation location and target agent.

**Quick options:**
```bash
# Global install
npx skills add bntvllnt/agent-skills --skill analyze -g

# Specific agent
npx skills add bntvllnt/agent-skills --skill analyze --agent claude-code

# Skip all prompts
npx skills add bntvllnt/agent-skills --skill analyze -g --agent claude-code -y
```

## Full Documentation

See [SKILL.md](./SKILL.md) for:
- Complete execution flow
- Thinking framework (UltraThink)
- First-principles methodology
- Perspectives library (50+ roles)
- Self-correction guide
- Failure patterns
- Integration notes

## License

MIT - Free to use, modify, distribute

## Author

**bntvllnt** ([github](https://github.com/bntvllnt) | [web](https://bntvllnt.com))
