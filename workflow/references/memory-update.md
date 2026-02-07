# Memory Update Protocol

> **Agent:** Load this file during `done` Step 4. Read the user's agent config (global + project rules) before proposing.

After retro, propose updating the agent's persistent memory with learnings from this session.

---

## Step 1: Read Existing Rules (MANDATORY)

**Before proposing anything, understand what already exists.**

Detect which agent is running, then read the correct target files:

```
Claude Code detected?
  → Read {project}/CLAUDE.md (project root)
  → Read ~/.claude/CLAUDE.md and ~/.claude/rules/ (user-level)

Other agent (Cursor, Windsurf, Aider, etc.)?
  → Read {project}/AGENTS.md (universal agent config)
  → Read agent-specific user-level config (see targets table)

Neither file exists?
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
| **Anti-patterns / Mistakes** | Mistakes made, wrong assumptions, failed approaches, regressions introduced | "Never modify auth middleware without running full test suite first" |

**Anti-patterns** capture what went wrong so it doesn't repeat:
- Wrong assumptions that led to wasted time
- Failed approaches that should be avoided
- Changes that caused regressions in other parts of the system
- Examples: "This project's DB queries require explicit transaction wrapping", "Changing the user model breaks 3 downstream services — always run integration tests"

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
| Thinking pattern (universal) | User-level | `~/.claude/CLAUDE.md` or `~/.claude/rules/` |
| Thinking pattern (project) | Project-level | Claude Code → `{project}/CLAUDE.md`; Others → `{project}/AGENTS.md` |
| Coding rule (universal) | User-level | `~/.claude/rules/coding-{language}.md` |
| Coding rule (language-specific) | User-level | `~/.claude/rules/coding-{language}.md` |
| Coding rule (project-specific) | Project-level | Claude Code → `{project}/CLAUDE.md`; Others → `{project}/AGENTS.md` |
| Project convention | Project-level | Claude Code → `{project}/CLAUDE.md`; Others → `{project}/AGENTS.md` |
| Quality check | Project-level | Claude Code → `{project}/CLAUDE.md`; Others → `{project}/AGENTS.md` |
| Process rule (universal) | User-level | `~/.claude/CLAUDE.md` or `~/.claude/rules/` |
| Process rule (project) | Project-level | Claude Code → `{project}/CLAUDE.md`; Others → `{project}/AGENTS.md` |
| Anti-pattern (universal) | User-level | `~/.claude/CLAUDE.md` or `~/.claude/rules/` |
| Anti-pattern (project-specific) | Project-level | Claude Code → `{project}/CLAUDE.md`; Others → `{project}/AGENTS.md` |

**Routing rule:** Claude Code project learnings → `{project}/CLAUDE.md`. All other agents → `{project}/AGENTS.md`. If target file doesn't exist → propose creating it in Step 4.

## Step 4: Propose

Present file-targeted proposals with exact content. Each proposal = exact text to add + exact target section. No ambiguity, copy-paste ready.

    ### Proposed Agent Config Updates

    Based on this session, I suggest updating your agent config:

    **{project}/CLAUDE.md** (project-level, Claude Code):
    - ADD rule: "{exact rule text}" → Section: {section name}
    - ADD anti-pattern: "{exact anti-pattern text}" → Section: Anti-patterns
    - {or "No updates needed"}

    **{project}/AGENTS.md** (project-level, other agents):
    - ADD rule: "{exact rule text}" → Section: {section name}
    - ADD coding standard: "{exact standard}" → Section: {section name}
    - {or "File not found — propose creating with initial rules? [y/n]"}

    **~/.claude/CLAUDE.md** (user-level, universal patterns):
    - ADD pattern: "{exact pattern text}" → Section: {section name}
    - {or "No universal learnings this session"}

    **Anti-patterns (prevent repeat mistakes):**
    - [{target file}] "{exact anti-pattern}" — learned from: {what went wrong}

    **Conflicts with existing rules:**
    - {existing rule} vs {proposed rule}: {recommendation}

    Update? [apply all / select / skip]

If a target file doesn't exist, propose creating it with initial content from this session's learnings.

## Agent Config Targets

| Agent | User-level | Project-level (agent-specific) | Project-level (universal) |
|-------|-----------|-------------------------------|--------------------------|
| Claude Code | `~/.claude/CLAUDE.md` or `~/.claude/rules/{topic}.md` | `{project}/CLAUDE.md` | `{project}/AGENTS.md` |
| Cursor | `~/.cursorrules` | `{project}/.cursorrules` | `{project}/AGENTS.md` |
| Windsurf | `~/.windsurfrules` | `{project}/.windsurfrules` | `{project}/AGENTS.md` |
| Aider | `~/.aider.conf.yml` | `{project}/.aider.conf.yml` | `{project}/AGENTS.md` |
| Continue | `~/.continue/config.json` | `{project}/.continue/config.json` | `{project}/AGENTS.md` |
| Codex | Agent config | Project config | `{project}/AGENTS.md` |
| Other | Ask user for path | Ask user for path | `{project}/AGENTS.md` |

**Routing logic:**
- Claude Code project learnings → `{project}/CLAUDE.md` (standard location)
- All other agents → `{project}/AGENTS.md` (universal agent config, project root)
- Universal patterns (any agent) → user-level config
- Auto-detect which agent is running. If unknown, ask the user.

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
