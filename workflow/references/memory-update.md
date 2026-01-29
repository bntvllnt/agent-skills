# Memory Update Protocol

> **Agent:** Load this file during `done` Step 4. Read the user's agent config (global + project rules) before proposing.

After retro, propose updating the agent's persistent memory with learnings from this session.

---

## Step 1: Read Existing Rules (MANDATORY)

**Before proposing anything, understand what already exists.**

Read both levels using the Agent Config Targets table below. Build a mental model:
- What thinking patterns are already defined?
- What coding standards exist?
- What quality gates are configured?
- What project-specific conventions are enforced?
- What security/testing rules exist?

**Why:** Proposals that duplicate existing rules waste time. Proposals that contradict existing rules cause confusion. Understanding the hierarchy ensures updates slot in correctly.

## Step 2: Extract Learnings

From the retro and session history, identify learnings in 5 categories:

| Category | What to extract | Example |
|----------|----------------|---------|
| **Thinking patterns** | Reasoning approaches that worked/failed | "Tree-of-thought for multi-approach decisions in auth" |
| **Coding rules** | Code standards discovered during implementation | "Always validate JWT expiry before checking claims" |
| **Project rules** | Codebase conventions the agent should follow | "This project uses barrel exports — add to index.ts" |
| **Quality checks** | New checklist items from bugs or review findings | "Auth features need rate limiting check" |
| **Process rules** | Workflow improvements from the session | "Run integration tests before unit tests in this project" |

For each learning, check:

| Check | If Yes |
|-------|--------|
| Already exists in user/project rules? | SKIP (don't duplicate) |
| Contradicts an existing rule? | FLAG as conflict |
| Universal or project-specific? | Determines target level |
| Actionable in 1-2 lines? | If not, refine |

## Step 3: Classify & Target

| Learning Type | Target Level | Where to Add |
|---------------|-------------|--------------|
| Thinking pattern (universal) | User-level | Rules file: reasoning/mental-models |
| Thinking pattern (project) | Project-level | Project rules file |
| Coding rule (universal) | User-level | Rules file: coding standards |
| Coding rule (language-specific) | User-level | Rules file: coding-{language} |
| Coding rule (project-specific) | Project-level | Project rules or CLAUDE.md |
| Project convention | Project-level | Project rules file |
| Quality check | Project-level | Quality checklist or rules file |
| Process rule (universal) | User-level | Rules file: workflow/process |
| Process rule (project) | Project-level | Project rules file |

## Step 4: Propose

Present to user for approval:

    ### Proposed Memory Updates

    Based on this session, I suggest updating your agent config:

    **Thinking Patterns:**
    - [user-level] {pattern}: {when to apply} → Add to {file}
    - [project-level] {pattern}: {when to apply} → Add to {file}

    **Coding Rules:**
    - [project-level] {rule}: {rationale} → Add to {file}

    **Quality Checks:**
    - [project-level] {check}: {what it catches} → Add to {file}

    **Process Rules:**
    - [user-level] {rule}: {why it helps} → Add to {file}

    **Conflicts with existing rules:**
    - {existing rule} vs {proposed rule}: {recommendation}

    Update? [apply all / select / skip]

## Agent Config Targets

| Agent | User-level | Project-level |
|-------|-----------|--------------|
| Claude Code | `~/.claude/CLAUDE.md` or `~/.claude/rules/{topic}.md` | `{project}/.claude/CLAUDE.md` or `{project}/.claude/rules/*.md` |
| Cursor | `~/.cursorrules` | `{project}/.cursorrules` |
| Windsurf | `~/.windsurfrules` | `{project}/.windsurfrules` |
| Aider | `~/.aider.conf.yml` | `{project}/.aider.conf.yml` |
| Continue | `~/.continue/config.json` | `{project}/.continue/config.json` |
| Codex | Agent config | Project config |
| Other | Ask user for path | Ask user for path |

Auto-detect which agent is running. If unknown, ask the user where to write.

## Rules

- **Read before proposing** — ALWAYS read existing rules first. No blind proposals.
- ALWAYS propose, NEVER auto-write. User approves every memory update.
- Keep updates concise: 1-2 lines per learning, actionable.
- **No duplicates** — skip if learning already exists in rules.
- **Flag conflicts** — if proposed rule contradicts existing, present both and recommend.
- Prefer project-level for project-specific knowledge.
- Prefer user-level for universal patterns.
- Max 5 proposals per session — prioritize by impact.
- Configurable: edit this file to disable memory update proposals.
