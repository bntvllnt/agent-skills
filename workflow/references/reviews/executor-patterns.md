# Review Executor Patterns

Optional implementations of the core portable review spec.

This file is intentionally non-normative. It describes ways to execute the review contract, not the contract itself.

## Rule

Any executor is acceptable if it can:
- inspect every changed hunk
- inspect every relevant rule
- emit explicit verdicts
- produce the required review evidence

## Executor Types

### 1. Single-agent executor
One agent performs the full review sequentially.

Use when:
- diff is small
- no parallelism is available
- human/operator cost matters more than redundant review depth

### 2. Multi-reviewer executor
Multiple specialized reviewers split responsibility by perspective or risk.

Use when:
- diff is medium/large
- high-risk hunks exist
- independent second opinions materially reduce risk

Typical roles:
- Correctness reviewer
- Security reviewer
- Reliability reviewer
- Rules auditor

### 3. Human/manual executor
A human follows the review contract using the same ledgers and verdict vocabulary.

Use when:
- automation is unavailable
- changes are highly sensitive
- final arbitration is required

### 4. CI validator / enforcement layer
A CI validator does not need to perform all reasoning itself. It can validate that required review artifacts exist and are complete, or validate artifacts produced by another executor.

Use when:
- enforcing minimum review coverage
- ensuring reproducibility in shared repos
- blocking merges when required evidence is missing

## Runtime-specific examples

Possible adapters include:
- generic subagent orchestration
- external specialist review sessions
- editor-integrated review workflows
- bespoke CI or scripting layers

These are examples only. The core workflow skill should never require one of them by name.

## Recommended OSS posture

For open-source repositories:
- keep the core review contract runtime-neutral
- document adapters as optional examples only when they add real value
- avoid making the review standard depend on one vendor, one model, or one local wrapper
- treat adapter docs as replaceable implementation details

## Selection Guidance

Choose the smallest executor that still satisfies the contract:
- low-risk docs change → single-agent executor may be enough
- high-risk auth/API/infra change → multi-reviewer executor is better
- shared CI enforcement → validate artifacts even if the reasoning was done elsewhere

## Anti-patterns

Avoid these in the core review contract:
- “must call tool X”
- “must use model Y”
- “must spawn subagents”
- “must use runtime Z”

Those statements make the OSS skill less portable and harder to maintain.
