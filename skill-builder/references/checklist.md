# Skill Authoring Checklist

Use this as a pre-flight checklist for any new/updated skill.

## Spec Correctness

- Folder name matches frontmatter `name`.
- `name` is 1-64 chars; lowercase letters/numbers/hyphens; no leading/trailing `-`; no `--`.
- `description` is non-empty, <= 1024 chars, and states both what + when.

## Activation Quality

- Description contains concrete trigger phrases users will say.
- Triggers do not overlap with other skills in the same repo/install.
- Router makes the first decision quickly.

## Context Efficiency

- `SKILL.md` is short (recommendation: < 500 lines).
- Heavy details live in `references/`.
- Reference files are small and focused.

## Safety

- No secrets, credentials, tokens, private URLs.
- No default-destructive commands.
- If you include `allowed-tools`, it is minimal and scoped.

## Usability

- Includes 2-3 examples.
- Includes expected outputs / formatting guidance.
- Includes troubleshooting for common failure modes.
