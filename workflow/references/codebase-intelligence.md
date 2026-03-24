# Codebase Intelligence (TypeScript Structural Analysis)

> **Agent:** Load this file when working with a TypeScript codebase. Provides graph-based structural analysis via CLI.

**Method:** CLI via `npx`. TypeScript codebases only.

---

## Documentation (Single Source of Truth)

Command reference, flags, metrics, data model, and tool selection guide live in the upstream repo — not here. Fetch the appropriate doc before first use:

| Doc | URL | When to Use |
|-----|-----|-------------|
| **llms.txt** (summary) | `https://raw.githubusercontent.com/bntvllnt/codebase-intelligence/main/llms.txt` | Quick orientation — commands, capabilities, tool selection |
| **llms-full.txt** (complete) | `https://raw.githubusercontent.com/bntvllnt/codebase-intelligence/main/llms-full.txt` | Full reference — architecture, data model, metrics, all CLI syntax, flags |

**Fetch once per session** using WebFetch or `curl`. These files are always up-to-date with the latest release.

---

## Detection Gate

Before using any command, verify both conditions:

```
1. tsconfig.json exists at project root (or nearest parent)
   → If missing: NOT a TypeScript project — skip all CI commands
2. npx codebase-intelligence --help exits successfully
   → If fails: CI not available — fall back to grep/glob/read
```

Cache detection result per session. Do not re-check on every command.

---

## Invocation Pattern

```bash
npx codebase-intelligence <command> <path> [flags] --json
```

Always use `--json` for machine-readable output. Timeout: 30s per command. Non-zero exit or timeout = silent fallback to grep/glob/read.

---

## Quick Reference (Common Workflows)

For full command syntax and flags, see `llms-full.txt` above.

| Question | Command |
|----------|---------|
| What does this codebase look like? | `npx codebase-intelligence overview ./src --json` |
| What are the riskiest files? | `npx codebase-intelligence hotspots ./src --metric complexity --json` |
| Tell me about file X | `npx codebase-intelligence file ./src <file> --json` |
| What breaks if I change file X? | `npx codebase-intelligence dependents ./src <file> --json` |
| What breaks if I change function X? | `npx codebase-intelligence impact ./src <symbol> --json` |
| Who calls this function? | `npx codebase-intelligence symbol ./src <name> --json` |
| What changed + risk? | `npx codebase-intelligence changes ./src --json` |
| Find unused exports | `npx codebase-intelligence dead-exports ./src --json` |
| Module architecture | `npx codebase-intelligence modules ./src --json` |
| Architectural tensions | `npx codebase-intelligence forces ./src --json` |
| Find all references for rename | `npx codebase-intelligence rename ./src <oldName> <newName> --json` |
| Execution flow tracing | `npx codebase-intelligence processes ./src --json` |
| File community clusters | `npx codebase-intelligence clusters ./src --json` |

---

## Fallback (When CI Unavailable)

Every CI command has a grep/glob/read equivalent. If CI is unavailable or fails, fall back silently:

| CI Command | Fallback |
|------------|----------|
| `overview` | `find` + manual file counting |
| `dependents` | Grep for import references |
| `symbol` | Grep for function references |
| `impact` | Manual call chain tracing |
| `hotspots` | Manual code review |
| `changes` | `git diff` + manual risk classification |
| `file` | Read + manual analysis |
| `forces` | Manual architecture review |
| `dead-exports` | Grep for unused exports |
| `modules` | Grep for import paths |
| `rename` | Grep + find-replace |
| `processes` | Manual code path tracing |
| `clusters` | Manual folder analysis |
| `groups` | `ls` + manual inspection |
| `search` | Grep tool |

---

## Cache

- Auto-stored in `.code-visualizer/` directory at project root
- Use `--force` to rebuild after significant structural changes
- Recommend adding `.code-visualizer/` to `.gitignore`

---

## Error Handling

```
Command fails or times out (30s)?
  → Log silently, fall back to grep/glob/read equivalent
  → Never surface CI errors to user
  → Never block workflow on CI availability
```
