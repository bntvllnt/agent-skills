# Memory Update Protocol

> **Agent:** Load this file whenever proposing rule/memory updates: `done` Step 4 (session learnings), `fix` PREVENT step (bug prevention rules), or any action that produces learnings worth persisting. Read the user's agent config (global + project rules) before proposing.

Shared protocol for reading agent config, classifying learnings, targeting the right files, and proposing updates. Used by multiple actions.

---

## Step 1: Read Existing Rules (MANDATORY)

**Before proposing anything, understand what already exists.**

Detect which agent is running, then read **all** config files that exist at both levels:

```
Project-level (check all that exist):
  {project}/CLAUDE.md
  {project}/.claude/CLAUDE.md
  {project}/.claude/rules/*
  {project}/AGENTS.md
  {project}/.cursorrules
  {project}/.windsurfrules
  {project}/.aider.conf.yml
  {project}/.continue/config.json
  {project}/codex.md
  {project}/.opencode/config

User-level (check all that exist):
  ~/.claude/CLAUDE.md
  ~/.claude/rules/*
  ~/.cursorrules
  ~/.windsurfrules
  ~/.aider.conf.yml
  ~/.continue/config.json
  ~/.codex/config or ~/codex.md
  ~/.opencode/config

No config files found at either level?
  → Flag for Step 4: propose creating with initial rules from session
```

Build a mental model:
- What thinking patterns are already defined?
- What coding standards exist?
- What quality gates are configured?
- What project-specific conventions are enforced?
- What security/testing rules exist?
- What anti-patterns are already documented?

**Why:** Proposals that duplicate existing rules waste time. Proposals that contradict existing rules cause confusion. Understanding the hierarchy ensures updates slot in correctly.

## Step 2: Extract Learnings

From the retro and session history, identify learnings in 6 categories:

| Category | What to extract | Example |
|----------|----------------|---------|
| **Thinking patterns** | Reasoning approaches that worked/failed | "Tree-of-thought for multi-approach decisions in auth" |
| **Coding rules** | Code standards discovered during implementation | "Always validate JWT expiry before checking claims" |
| **Project rules** | Codebase conventions the agent should follow | "This project uses barrel exports — add to index.ts" |
| **Quality checks** | New checklist items from bugs or review findings | "Auth features need rate limiting check" |
| **Process rules** | Workflow improvements from the session | "Run integration tests before unit tests in this project" |
| **Patterns & Anti-patterns** | User preferences, repeated requests, mistakes, failed approaches, regressions | "User always wants error boundaries around async components" |

**Note on bug fixes:** Bug fixes trigger lightweight PREVENT proposals inline during `ship` (max 2, coding rules/anti-patterns/quality checks only). See regression-testing.md Step 7. PREVENT uses the same agent-detection and file-targeting logic from Step 3 (Classify & Target) above. The `done` memory update handles session-wide learnings across all categories. When extracting learnings here, **skip proposals already saved during PREVENT** to avoid duplicates.

**Patterns** capture what to remember so the agent improves across sessions:
- **User preferences**: coding style requests, architecture preferences, naming conventions the user enforces ("user prefers explicit return types on all functions")
- **Repeated requests**: things the user asks for repeatedly that should be default behavior ("always add loading states to async UI")
- **Project knowledge**: implicit rules learned during the session ("this project's DB queries require explicit transaction wrapping")
- **Anti-patterns**: wrong assumptions, failed approaches, regressions introduced ("never modify auth middleware without running full test suite first")
- **Workflow preferences**: how the user likes to work ("user prefers small commits, one per logical change")

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
| Thinking pattern (universal) | User-level | Agent's user-level config (see targets table) |
| Thinking pattern (project) | Project-level | Agent's project-level config (see targets table) |
| Coding rule (universal) | User-level | Agent's user-level config |
| Coding rule (language-specific) | User-level | Agent's user-level config (prefer topic-specific file if supported) |
| Coding rule (project-specific) | Project-level | Agent's project-level config |
| Project convention | Project-level | Agent's project-level config |
| Quality check | Project-level | Agent's project-level config |
| Process rule (universal) | User-level | Agent's user-level config |
| Process rule (project) | Project-level | Agent's project-level config |
| User preference (universal) | User-level | Agent's user-level config |
| User preference (project-specific) | Project-level | Agent's project-level config |
| Anti-pattern (universal) | User-level | Agent's user-level config |
| Anti-pattern (project-specific) | Project-level | Agent's project-level config |

**Routing rule:** Use the Agent Config Targets table below to resolve "agent's project/user-level config" to the correct file path. If the detected agent has both agent-specific and universal (`AGENTS.md`) project config, prefer agent-specific. If target file doesn't exist → propose creating it in Step 4.

## Step 4: Propose

Present a numbered list so the user can cherry-pick. Each item = exact text + target file + section. No ambiguity, copy-paste ready.

### Presentation Method

**If agent has `AskUserQuestion` (or equivalent multi-select UI):**

Use it with `multiSelect: true`. Each option = one numbered learning. User picks which to apply.

```
AskUserQuestion:
  question: "Which learnings should I save to agent config?"
  multiSelect: true
  options:
    - label: "#1 {short summary}"
      description: "ADD to {file} § {section}: {exact text}"
    - label: "#2 {short summary}"
      description: "ADD to {file} § {section}: {exact text}"
    ...
```

**If agent has no multi-select UI (fallback):**

Print numbered list, ask user to reply with numbers:

    ### Proposed Agent Config Updates

    Based on this session, I suggest saving these learnings:

    1. [{target file} § {section}] **{type}**: "{exact text to add}"
       _Context: {why this matters / when observed}_

    2. [{target file} § {section}] **{type}**: "{exact text to add}"
       _Context: {why this matters / when observed}_

    3. [{target file} § {section}] **{type}**: "{exact text to add}"
       _Context: {why this matters / when observed}_

    **Conflicts with existing rules:**
    - {existing rule} vs {proposed rule}: {recommendation}

    Apply which? [all / 1,3 / none]

**Type labels:** `rule`, `preference`, `anti-pattern`, `coding standard`, `pattern`

**Target file shorthand:**
- `{project config}` = agent's project-level config (resolved via Agent Config Targets table)
- `{user config}` = agent's user-level config (resolved via Agent Config Targets table)
- `P/AGENTS.md` = `{project}/AGENTS.md` (universal fallback)

If a target file doesn't exist, add a final item: "Create {file} with selected rules? [y/n]"

## Agent Config Targets

| Agent | User-level | Project-level (agent-specific) | Project-level (universal) |
|-------|-----------|-------------------------------|--------------------------|
| Claude Code | `~/.claude/CLAUDE.md` or `~/.claude/rules/{topic}.md` | `{project}/CLAUDE.md` or `{project}/.claude/rules/` | `{project}/AGENTS.md` |
| Cursor | `~/.cursorrules` | `{project}/.cursorrules` | `{project}/AGENTS.md` |
| Windsurf | `~/.windsurfrules` | `{project}/.windsurfrules` | `{project}/AGENTS.md` |
| Aider | `~/.aider.conf.yml` | `{project}/.aider.conf.yml` | `{project}/AGENTS.md` |
| Continue | `~/.continue/config.json` | `{project}/.continue/config.json` | `{project}/AGENTS.md` |
| Codex | `~/.codex/config` or `~/codex.md` | `{project}/codex.md` | `{project}/AGENTS.md` |
| OpenCode | `~/.opencode/config` | `{project}/.opencode/config` | `{project}/AGENTS.md` |
| Other | Ask user for path | Ask user for path | `{project}/AGENTS.md` |

**Routing logic:**
- Detect which agent is running → use Agent Config Targets table to find correct file paths
- Project-specific learnings → agent's project-level config (agent-specific column preferred)
- Universal patterns → agent's user-level config
- `{project}/AGENTS.md` is the universal fallback for any agent without its own project config
- Auto-detect which agent is running. If unknown, ask the user.

### Proposal Format Examples (by agent)

When proposing a rule, target the correct file for the detected agent:

Claude Code:
```
[{project}/CLAUDE.md § Coding Rules] rule: "Always null-check optional user fields before access"
_Prevents: null reference errors on incomplete profiles_
```

Cursor:
```
[{project}/.cursorrules § Rules] rule: "Always null-check optional user fields before access"
_Prevents: null reference errors on incomplete profiles_
```

Windsurf:
```
[{project}/.windsurfrules § Rules] rule: "Always null-check optional user fields before access"
_Prevents: null reference errors on incomplete profiles_
```

Codex:
```
[{project}/codex.md § Rules] rule: "Always null-check optional user fields before access"
_Prevents: null reference errors on incomplete profiles_
```

OpenCode:
```
[{project}/.opencode/config § Rules] rule: "Always null-check optional user fields before access"
_Prevents: null reference errors on incomplete profiles_
```

Universal (any agent):
```
[{project}/AGENTS.md § Coding Rules] rule: "Always null-check optional user fields before access"
_Prevents: null reference errors on incomplete profiles_
```

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
