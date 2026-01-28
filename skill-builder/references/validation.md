# Validation Flow

## 1) Spec Validation

Preferred (if available):

```bash
skills-ref validate ./<skill-name>
```

If `skills-ref` is not available, this skill still works. Do the manual checks in the next section.

If not available, validate manually against:
- https://agentskills.io/specification

## 2) Trigger Hygiene

Avoid overlap across skills installed together.

Practical checks:

- Search the repo for the new trigger phrases.
- If overlap is unavoidable, rewrite descriptions so each skill has distinct intent keywords.

## 3) Structure + Progressive Disclosure

- Keep `SKILL.md` as router + core rules.
- Split deep workflows into `references/*.md`.

## 4) Safety

- No secrets.
- No default destructive commands.
- Make confirmation boundaries explicit.
