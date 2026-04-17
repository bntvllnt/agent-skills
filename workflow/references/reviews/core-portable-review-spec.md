# Core Portable Review Spec

Tool-agnostic review contract for `workflow`'s `review` action.

Use this file to keep the review standard portable across agent runtimes, CI systems, and human/manual execution.

## Purpose

Separate **review policy** from **review executor**.

- **Core portable review spec** = what must happen
- **Executor / adapter** = how a specific runtime performs it

The core spec is the OSS asset. Executors are optional implementations.

## Non-Goals

This spec does **not** require:
- a specific model
- a specific coding agent
- a specific CLI or orchestration tool
- a specific terminal/session manager
- a specific local shell wrapper or harness

If a runtime can produce the required evidence, it can implement this spec.

## Required Inputs

Every review must operate on:
- base ref or previous review point
- head ref or current working state
- changed files
- changed hunks / exact line ranges
- discovered project rules
- optionally loaded user rules
- per-file category and risk classification

## Required Phases

1. Discover the diff
2. Build a line-range ledger for all changed hunks
3. Discover and normalize relevant rules
4. Assign reviewer responsibility by perspective and risk
5. Review each changed hunk
6. Review each relevant rule one by one
7. Merge findings and resolve conflicts per policy
8. Emit human-readable summary + machine-readable artifacts

## Coverage Contract

A review is only complete when both are true:

1. **Line coverage** — every changed hunk / line range has an explicit verdict
2. **Rule coverage** — every relevant rule has an explicit verdict

No clean verdict without both.

## Verdict Vocabulary

Use fixed states only:
- `PASS`
- `WARN`
- `FAIL`
- `NOT_APPLICABLE`

Optional merged state for final arbitration:
- `REQUIRES_HUMAN_REVIEW`

## Blocking Conditions

The review must block when any of the following is true:
- a changed hunk has no verdict
- a relevant rule has no verdict
- a mandatory project rule source could not be loaded
- any finding is `FAIL`
- high-risk conflicts remain unresolved
- required output artifacts are missing or invalid

## Rule Source Policy

Rule sources are split into:
- **Project-level** — stable, repo-owned, reproducible; can block
- **User-level** — environment-specific overlays; must be reported explicitly when loaded

Default OSS-safe posture:
- CI / shared review mode: project-level rules only
- local enhanced review mode: project + user rules, with source disclosure

Never claim a user-level rule was checked unless that source was actually loaded.

## Reviewer Assignment Model

The spec requires assignment by hunk, not vague global review.

Minimum contract:
- every changed hunk has at least one assigned review perspective
- high-risk hunks may require an additional perspective or second opinion
- the executor may use one reviewer, many reviewers, humans, or agents
- the assignment and reviewer identity must be recorded in the artifact

## Executor Contract

An executor is any system that can consume the review inputs and emit the required evidence.

Examples:
- single-agent local review
- multiple parallel subagents
- human reviewer with a checklist
- CI validator
- external coding-agent orchestration

Executors may differ, but they must all emit the same review evidence.

## Required Artifacts

At minimum, the review output must contain:

### Human-readable summary
- change overview
- coverage summary
- rule coverage ledger
- per-file findings
- final verdict

### Machine-readable artifact
The executor must emit a structured artifact equivalent to:

```json
{
  "review_id": "string",
  "base_ref": "string",
  "head_ref": "string",
  "rule_sources_loaded": {
    "project": [],
    "user": [],
    "unavailable": []
  },
  "changed_hunks": [
    {
      "file": "string",
      "range": "string",
      "category": "string",
      "risk": "LOW|MEDIUM|HIGH",
      "assigned_perspectives": [],
      "reviewed_by": [],
      "verdict": "PASS|WARN|FAIL|NOT_APPLICABLE"
    }
  ],
  "rule_checks": [
    {
      "rule_id": "string",
      "source": "string",
      "applies_to": [],
      "verdict": "PASS|WARN|FAIL|NOT_APPLICABLE"
    }
  ],
  "findings": [],
  "final_verdict": "CLEAN|WARNINGS_ONLY|HAS_BLOCKERS|REQUIRES_HUMAN_REVIEW"
}
```

The exact file name is executor-specific. The schema contract is not.

## Merge / Conflict Policy

If multiple reviewers or systems contribute findings:
- any `FAIL` blocks
- conflicting `PASS` / `WARN` results should be surfaced
- unresolved high-risk conflicts become `REQUIRES_HUMAN_REVIEW`
- missing assigned reviewer output is a process failure

## Portability Rule

The `workflow` skill must describe the review contract in a way that remains valid even when:
- no subagents exist
- no external model CLIs exist
- no CI exists
- only a human operator is available

Runtime-specific orchestration belongs in optional executor guidance, not in the core review contract.