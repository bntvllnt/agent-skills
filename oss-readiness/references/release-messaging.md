# Release Messaging

Cross-platform rubric for evaluating OSS release titles, release-note openings, and launch-announcement framing.

Use this when the user asks things like:

- `is this a good OSS release title?`
- `audit release messaging`
- `improve the release title`
- `rewrite the opening release notes`
- `does this announcement read like a real release?`

## Core Principle

The title and opening lines should make the release legible to an outsider in one glance.

That means:

- name the dominant user-facing change
- say it in plain language
- avoid internal-only framing
- avoid hype the diff does not support

## Preconditions

Before writing a title or lead summary, confirm:

1. **Stable scope**
   - The merged or imminent release diff is known
2. **Dominant change selected**
   - One main external change is identified
3. **Audience selected**
   - Users, contributors, operators, or developers evaluating the project
4. **Truthfulness check**
   - The claim is strong but supported by the release

## Title Rubric

A strong OSS release title is:

- **specific**
- **outcome-first**
- **brief**
- **truthful**
- **aligned with the dominant change**

Good:

- `v1.13.1 — Code review, supercharged`
- `v0.8.0 — Faster local inference`
- `v2.4.0 — Rules discovery everywhere`

Weak:

- `v1.13.1 — Updates`
- `v0.8.0 — Workflow improvements`
- `v2.4.0 — Internal cleanup`

## Opening Summary Rubric

The first 1-3 sentences or first bullets should:

- reinforce the same story as the title
- surface the dominant change immediately
- avoid leading with maintenance work if the release is really about a feature or capability
- be understandable when quoted in chat previews or screenshots

Bad pattern:

```text
v1.13.1 — Code review, supercharged

This release includes several cleanup items, internal refactors, and minor workflow changes...
```

Better pattern:

```text
v1.13.1 — Code review, supercharged

This release hardens review in the workflow skill with line-by-line coverage, rule-by-rule enforcement, and fail-closed review output.
```

## Anti-Patterns

Avoid:

- vague nouns: `updates`, `improvements`, `changes`
- internal-only framing when the release is externally meaningful
- hype words with no evidence
- titles that depend on prior context to make sense
- opening summaries that bury the real release story under housekeeping

## Fast Evaluation Checklist

- Can a new reader tell what changed from the title alone?
- Does the title describe the dominant external outcome?
- Do the opening lines reinforce that same outcome?
- Would the title still work if shown alone on a social card?
- Is the wording strong without overselling?

If any answer is no, rewrite before publishing.
