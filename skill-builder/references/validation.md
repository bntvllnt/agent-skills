# Validation Flow

Use this flow to produce evidence, not just a checklist.

## 1) Spec Validation

Preferred (if available):

```bash
skills-ref validate ./<skill-name>
```

If `skills-ref` is not available, validate manually against:
- https://agentskills.io/specification
- valid YAML frontmatter parsed by a real parser
- `name` matches the parent directory
- `description` covers what the skill does and when to use it
- only spec-supported top-level fields are used unless the target environment explicitly supports more

YAML pitfalls to check explicitly:
- Quote values containing `:` followed by text.
- Do not rely on permissive parsers.
- Keep extra metadata under `metadata`.

## 2) Trigger Validation

The description is the primary discovery mechanism.

Build a realistic eval set:
- ~8-10 prompts that should trigger
- ~8-10 prompts that should not trigger
- prioritize near-misses over obviously irrelevant prompts
- vary tone, detail level, wording, typos, and indirect phrasing

Practical checks:
- Search neighboring skills for overlapping description language.
- If overlap is unavoidable, rewrite descriptions so each skill has distinct intent keywords.
- Prefer intent phrases over broad single-word cues.

Output evidence:
- which prompts should trigger
- which prompts should not trigger
- any ambiguous cases and how the description was tightened

## 3) Output Validation

Run at least 2-3 realistic tasks.

For each task, record:
- prompt
- expected behavior
- whether the skill improved structure, safety, or consistency
- remaining gaps

If possible, compare:
- without the skill
- with the skill

## 4) Structure + Progressive Disclosure

- Keep `SKILL.md` as router + core rules.
- Split deep workflows into `references/*.md`.
- Keep references one level deep from `SKILL.md`.
- Avoid turning `SKILL.md` into a giant playbook.

## 5) Safety

- No secrets.
- No default destructive commands.
- Make confirmation boundaries explicit.
- Prefer the least-privileged capability that can complete the task.

## Validation Report Template

- Spec validation: pass/fail + evidence
- Trigger validation: pass/fail + prompt set summary
- Output validation: pass/fail + scenario summary
- Risks / follow-ups
