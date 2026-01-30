# Spec Review Action

> **Agent:** Load this file when `spec-review` triggers. Also load the active spec from `specs/active/`.

Deep adversarial analysis of an active spec. Standalone — no dependency on analyze skill.

**Triggers:** "review spec", "analyze spec", "challenge spec", "spec-review"

---

## Steps

### Step 1: Load Spec + Context

1. Find active spec in `specs/active/`
2. Read the full spec
3. Read codebase files listed in the spec's `## Codebase Impact` section
4. If no active spec → error: "No active spec found. Run `plan {idea}` first."

### Step 2: Select Perspectives (Dynamic)

Read the spec's context, scope, codebase impact, and risks. Autonomously select 3-6 expert perspectives most relevant to THIS spec's domain.

**Selection process:**

1. Identify the spec's domains from its content (code, SEO, marketing, data, infra, UX, legal, business, ops, content, security, performance, accessibility, etc.)
2. Select 3-6 perspectives that would catch the most blind spots for THESE domains
3. Always include 1 **Skeptic** (domain-agnostic adversarial thinker)
4. Present selected perspectives to user before launching

**Examples:**

| Spec Domain | Selected Perspectives |
|-------------|----------------------|
| SEO migration | SEO Specialist, Content Strategist, Web Performance Engineer, Skeptic |
| Auth system | Security Engineer, API Consumer, UX Designer, Skeptic |
| Pricing page | Conversion Optimizer, Frontend Engineer, A/B Testing Analyst, Skeptic |
| Database migration | Data Engineer, Reliability Engineer, DBA, Skeptic |
| CLI tool | Developer Advocate, Systems Engineer, Skeptic |

Min 3, max 6 perspectives.

### Step 3: Launch Parallel Analysis

**Launch ALL perspectives as parallel sub-agents** (single message, multiple Task tool calls).

Each sub-agent receives this prompt:

```
You are a {Role}. Review this spec adversarially.

SPEC:
{full spec content}

CONTEXT:
{codebase files from Codebase Impact, or domain context if not code-focused}

Answer these 4 questions:

1. ASSUMPTIONS: What's assumed that could be wrong?
   | Assumption | Evidence For | Evidence Against | Verdict |
   |------------|-------------|-----------------|---------|
   (min 2 per perspective)

2. BLIND SPOTS: What hasn't been considered?
   - 2-3 items with [category] + why it matters

3. FAILURE HYPOTHESES:
   | IF | THEN | BECAUSE | Severity |
   (1-3 per perspective)

4. THE REAL QUESTION: Is this solving the right problem from your perspective?

Every finding must end with action: → update spec / → explore / → question / → no action
```

### Step 4: Synthesize

1. Collect all perspective outputs
2. Deduplicate findings (merge similar assumptions/blind spots)
3. Rank by severity (HIGH → MED → LOW)
4. Aggregate into structured report

### Step 5: Output Report

Follow [plan-output.md](../templates/plan-output.md) (unified template for both `plan` and `spec-review`).

### Step 6: Merge (Optional)

If user says "merge" or "apply":
- Update the spec's `## Analysis` section with synthesized findings
- Add new risks to `## Risks` table
- Add new ACs if findings warrant them
- Note in spec's `## Notes`: "Spec review applied: {date}"

---

## Task Tracking

```
[ ] Load active spec + codebase context
[ ] Select and present perspectives
[ ] Launch parallel perspective agents
[ ] Synthesize findings into report
[ ] Present report (optionally merge into spec)
```

---

## Rules

- **Standalone**: No dependency on analyze skill or any external tool
- **Action-driven**: Every finding must force a decision (update/explore/question/no action)
- **Codebase-grounded**: Cross-reference against actual code, not just spec text
- **Parallel execution**: All perspectives run simultaneously (single message, multiple Task calls)
- **No passive observations**: "This could be a problem" is not allowed. "IF X THEN Y → update spec" is.
