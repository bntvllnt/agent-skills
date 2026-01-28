# Skill Builder

Build correct, consistent Agent Skills.

## Quick Start

- Core doc: `skill-builder/SKILL.md`
- Use when you want to:
  - create/update/delete a skill
  - add routes/workflows to a skill
  - validate skills (tool safety, trigger hygiene, structure)

References:

- `skill-builder/references/checklist.md`
- `skill-builder/references/templates.md`
- `skill-builder/references/validation.md`

## Install

From the repo root:

```bash
npx skills add bntvllnt/agent-skills --skill skill-builder
```

Manual install (download this folder only):

- Copy the `skill-builder/` folder into your agent's skills directory.
- Ensure the folder name is `skill-builder` and includes `SKILL.md`.

## Notes

- Prefer minimal viable skills; often a README section is enough.
