# Templates

## Minimal Skill

```markdown
---
name: my-skill
description: What it does and when to use it. Include trigger phrases.
compatibility: Optional. Mention required system tools or network access.
metadata:
  version: "0.1"
---

# My Skill

## Router

| User says | Do |
|---|---|
| <intent> | <procedure> |

## Safety

- Define what is read-only vs state-changing.
- Require confirmation for destructive operations.

## Workflow

1. Step
2. Step

## Examples

- "<example prompt>"
```

## Skill With References

```markdown
## Router

| User says | Load reference | Do |
|---|---|---|
| <intent> | `references/<topic>.md` | <action> |
```

## Skill With Scripts

Document script entrypoints and args.

```markdown
## Usage

```bash
scripts/<script>.sh <args>
```
```
