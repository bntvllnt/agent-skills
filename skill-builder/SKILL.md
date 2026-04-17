---
name: skill-builder
description: |
  Build correct, consistent Agent Skills for any compatible agent product. Use when creating,
  updating, renaming, deleting, or validating a skill, or when improving skill descriptions,
  structure, safety rules, progressive disclosure, or trigger reliability.
license: MIT
compatibility: "Agent Skills spec (agentskills.io). Works with any agent product that supports SKILL.md frontmatter + Markdown."
metadata:
  version: "1.1"
---

# Skill Builder

Unified, security-first skill builder.

This skill is intentionally opinionated:
- Prefer no new skill if a simpler change works.
- When you do create a skill, make it boring, testable, and hard to misuse.
- Keep one clear router and avoid overlapping descriptions across skills.
- Stay model-agnostic and harness-agnostic unless the target environment explicitly requires otherwise.

## Operation Router

| User intent | Operation | Output |
|---|---|---|
| create/build/make/new skill | CREATE | new skill folder + `SKILL.md` + only the companion files actually needed |
| update/modify/improve skill | UPDATE | minimal diff, keep scope stable |
| delete/remove skill | DELETE | remove skill + update any dependent references |
| add content/route/workflow to skill | ADD | new router row + minimal supporting procedure |
| validate skill | VALIDATE | evidence-backed validation report + fixes |
| rename skill | RENAME | safe rename + reference updates |

## Operation Selection Rules

Use the smallest operation that solves the request:

- **CREATE** — new user-facing capability or clearly distinct intent/description domain.
- **UPDATE** — improve an existing skill without changing its core scope.
- **ADD** — add one new route, example, or sub-workflow inside the current scope.
- **RENAME** — change identity/path/name while preserving mostly the same behavior.
- **DELETE** — remove obsolete capability because it is superseded, merged, or no longer useful.
- **VALIDATE** — inspect correctness without broadening scope.

If uncertain, default to **UPDATE** rather than CREATE.

## What "Correct" Means

This skill treats "correct" as:

- Conforms to the Agent Skills spec where the spec is explicit.
- Uses progressive disclosure: concise `SKILL.md`, deeper docs only when needed.
- Has unambiguous activation: specific description + non-overlapping neighboring skills.
- Is safe: no secrets, no default-destructive commands, explicit confirmation boundaries.
- Produces validation evidence instead of relying on vibes.

## Phase 0: First-Principles Check (Mandatory)

Run this before any CREATE or UPDATE:

1. QUESTION: what problem, for who, measured how?
2. DELETE: can an existing skill, README section, script, or template solve it?
3. SIMPLIFY: what is the smallest change that works?
4. ACCELERATE: only after (2) and (3)
5. AUTOMATE: create a new skill only if it will be reused

If the answer is "no skill", propose:
- a README section
- a small script
- a usage snippet users can copy
- a targeted update to an existing skill

## Phase 1: Detect Target + Name

### Required by the Agent Skills spec

- Skill directory contains `SKILL.md`.
- `SKILL.md` starts with valid YAML frontmatter.
- `name` matches the parent directory name.
- `description` explains what the skill does and when to use it.

### Recommended by this skill

- Keep `SKILL.md` focused on router + core rules.
- Add `references/`, `scripts/`, `assets/`, or `README.md` only when they add real value.
- Keep references one level deep from `SKILL.md`.
- Put nonstandard metadata under `metadata` instead of inventing new top-level fields.

### Naming

- Use kebab-case (`my-skill-name`).
- Avoid generic names (`tools`, `helper`).
- Prefer names that describe a distinct job to be done.

### Description design

The `description` field is the primary discovery surface.

Write it to cover:
- **what** the skill does
- **when** to use it
- likely user wording, domain terms, and near-synonyms

Do not depend on a custom top-level `triggers` field for portability. If you want trigger examples, keep them in the body, `metadata`, or eval fixtures.

## Confirmation Boundary

Safe without confirmation:
- read-only inspection
- drafting content
- local validation
- proposing diffs

Require confirmation before:
- deleting files or folders
- renaming skill folders
- overwriting user-authored content
- changing trigger semantics in ways that may alter discovery behavior
- editing repo indexes or catalogs
- installing dependencies or using networked side effects

## Phase 2: CREATE Flow

### Inputs (minimum)

- Name
- Goal + non-goals
- Description draft that covers what + when
- Optional capability constraints if the target client supports them

### CREATE Steps

1. Discover existing conventions in the target repo.
2. Draft a micro-spec: goal, non-goals, router, safety boundary.
3. Create `/<skill-name>/SKILL.md` with:
   - frontmatter (`name`, `description`, optional spec-supported fields)
   - router table
   - safety and confirmation rules
   - short workflows or links to `references/`
4. Add companion files only if justified:
   - `README.md` for human-facing install/overview
   - `references/` for deep workflows
   - `scripts/` for executable helpers
   - `assets/` for templates/resources
5. Validate using the evidence rules below.
6. If the repo maintains an index, update it.

### Output Contract (CREATE)

Always return:
- files created/edited
- description added or changed
- whether optional fields like `compatibility`, `metadata`, or `allowed-tools` were used
- one minimal smoke-test prompt
- validation report: pass/fail + evidence + remaining risks

## Phase 3: UPDATE Flow

1. Read the current skill.
2. Identify the actual user goal.
3. Apply the smallest diff that solves it.
4. Re-run validation.
5. Keep scope and description stable unless a broader change is explicitly requested.

### Output Contract (UPDATE)

Return:
- files changed
- behavior changed
- description change: yes/no
- validation report
- risks or follow-ups

## Phase 4: DELETE Flow

1. Confirm the target skill folder.
2. Identify dependents: indexes, references, sibling skills.
3. Remove the skill and update references.
4. Provide rollback instructions.

### Output Contract (DELETE)

Return:
- removed paths
- references updated
- rollback note
- validation/report of any remaining broken links

## Phase 5: ADD Content to a Skill

Rules for skill growth:
- Never duplicate description intent across multiple skills in the same install.
- Route by intent first, then load deeper sections.
- Keep `SKILL.md` readable: short tables, stable templates, deep detail in `references/`.

Add steps:
1. Add one new router row or one tightly scoped section.
2. Add the minimal new procedure.
3. If it grows, split into `references/<topic>.md`.
4. Add or update examples.
5. Re-check neighboring skills for overlap.

## Phase 6: RENAME Flow

1. Confirm old and new names.
2. Rename the folder and update frontmatter `name`.
3. Update internal and repo-level references.
4. Validate links, name/path parity, and discovery wording.

### Output Contract (RENAME)

Return:
- old name → new name
- moved paths
- references updated
- validation report

## Validation

### Validation Requirements

A skill is not validated until you produce evidence for all three layers:

1. **Spec validation** — structure and YAML correctness
2. **Trigger validation** — the description should trigger when it should, and not trigger on near-misses
3. **Output validation** — the skill improves or constrains the resulting work on realistic tasks

### Skill Validation Checklist

- Frontmatter includes valid `name` and `description`.
- Frontmatter is valid YAML, not just visually plausible Markdown metadata.
- `name` matches the parent directory.
- Description clearly states what + when.
- Any extra frontmatter stays within spec-supported fields unless the target environment explicitly supports more.
- Router is present.
- Confirmation boundary is explicit.
- No secrets; no private paths unless the target repo is intentionally private.
- No unscoped destructive instructions.
- Progressive disclosure is respected.
- Trigger hygiene has been checked against neighboring skills.

### Spec Validation (Recommended)

If available:

```bash
skills-ref validate ./<skill-name>
```

If not available, validate manually using the rules in `references/validation.md`.

### Capability Safety

- Prefer the least-privileged capability that can complete the task.
- Inspect/search before executing commands.
- If command execution is needed, scope it tightly.
- Never recommend `rm -rf`, `git reset --hard`, or `push --force` as defaults.

## Templates

### Skill Frontmatter

```yaml
---
name: my-skill
description: Use this skill when you need to do X, Y, or Z. It handles A and B and is relevant when the user asks for C.
compatibility: Optional. Mention required runtimes, system tools, or environment assumptions.
metadata:
  version: "0.1"
allowed-tools: Optional experimental field. Only include it when the target client supports it and the skill benefits from a constrained tool list.
---
```

### Minimum Viable Portable Skill

1. Frontmatter
2. One-paragraph purpose/activation guidance
3. Router table
4. Safety + confirmation rules
5. Short workflows
6. Optional `references/` only when needed

## References

- `references/checklist.md` (authoring checklist)
- `references/templates.md` (copy/paste templates)
- `references/validation.md` (spec, trigger, and output validation)

## What This Skill Is For (Practical Examples)

- "Create a skill that scaffolds new skills" → CREATE.
- "Make this skill more portable across agent products" → UPDATE.
- "Rename this skill without breaking references" → RENAME.
- "Check whether this skill will trigger reliably" → VALIDATE.
- "Make skills consistent across repos" → UPDATE or ADD, depending on scope.
