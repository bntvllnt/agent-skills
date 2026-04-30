# First Principles

First-principles thinking and 5-step engineering algorithm (popularized by Elon Musk). Break problems down to fundamentals and rebuild solutions from scratch.

## What This Does

Two composable frameworks:

- **First-Principles Thinking** — decompose a stated cost / constraint / belief into its physical or economic atoms, compute the irreducible floor, and reconstruct from there. Counters reasoning-by-analogy.
- **5-Step Algorithm** — *make requirements less dumb → delete the part → simplify → accelerate → automate*, run in order. Counters premature optimization and automating broken processes.

## When To Use

| Situation | Framework |
|-----------|-----------|
| "Industry says X costs Y" | First Principles |
| "Everyone does it like this" | First Principles |
| Designing or fixing a process / system | 5-Step Algorithm |
| Hard problem with both: cost belief + process | 1, then 2 |

## Entry Points

| Say | Action |
|-----|--------|
| "first principles on [X]" | Run 4-step decomposition on X |
| "what does the physics say about [X]" | Compute physical-cost floor for X |
| "5-step algorithm on [process]" | Run musk algorithm in order |
| "delete the part: [process]" | Apply step 2 specifically |
| "is this reasoning by analogy?" | Detect + replace analogy |

## Files

- `SKILL.md` — frontmatter, router, both frameworks, quick examples, anti-patterns
- `references/first-principles.md` — full decomposition workflow + analogy detector
- `references/algorithm.md` — 5-step algorithm with per-step checklists
- `references/case-studies.md` — worked examples (battery, SpaceX, Tesla, software)

## Requirements

- None. Agent-agnostic. No tools.

## License

MIT
