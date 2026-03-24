# Codebase Intelligence (TypeScript Structural Analysis)

> **Agent:** Load this file when working with a TypeScript codebase. Provides graph-based structural analysis via CLI.

**Method:** CLI via `npx`. TypeScript codebases only.

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
npx codebase-intelligence <command> --json <path> [flags]
```

Always use `--json` for machine-readable output. Timeout: 30s per command. Non-zero exit or timeout = silent fallback to grep/glob/read.

---

## Commands

### Discovery

| Command | Purpose | Example | Fallback |
|---------|---------|---------|----------|
| `overview` | Codebase snapshot: file count, module count, graph shape, top metrics | `npx codebase-intelligence overview --json ./src` | `find` + manual counting |
| `modules` | Module structure and cross-dependencies | `npx codebase-intelligence modules --json ./src` | Grep for import paths |
| `groups` | Top-level directory aggregates with metrics | `npx codebase-intelligence groups --json ./src` | `ls` + manual inspection |
| `clusters` | Louvain community detection — file groupings | `npx codebase-intelligence clusters --json ./src` | Manual folder analysis |
| `search` | BM25 keyword search across codebase | `npx codebase-intelligence search --json ./src "query"` | `grep` / Grep tool |

### Analysis

| Command | Purpose | Example | Fallback |
|---------|---------|---------|----------|
| `hotspots` | Rank files by architectural metric | `npx codebase-intelligence hotspots --json ./src --metric complexity --limit 10` | Manual code review |
| `forces` | Cohesion/tension analysis per module | `npx codebase-intelligence forces --json ./src` | Manual architecture review |
| `dead-exports` | Unused exports safe for removal | `npx codebase-intelligence dead-exports --json ./src --limit 20` | Grep for unused exports |
| `file` | Detailed context for a single file: imports, exports, coupling, complexity | `npx codebase-intelligence file --json ./src/index.ts` | Read + manual analysis |
| `changes` | Git diff analysis with risk assessment (coupling, blast radius, complexity delta) | `npx codebase-intelligence changes --json ./src` | `git diff` + manual risk classification |

### Impact & Tracing

| Command | Purpose | Example | Fallback |
|---------|---------|---------|----------|
| `dependents` | File-level blast radius — who imports this file? | `npx codebase-intelligence dependents --json ./src/utils.ts` | Grep for import references |
| `symbol` | Callers/callees for a specific function or export | `npx codebase-intelligence symbol --json ./src functionName` | Grep for function references |
| `impact` | Symbol-level transitive blast radius | `npx codebase-intelligence impact --json ./src parseCodebase` | Manual call chain tracing |
| `processes` | Entry-point execution flow tracing | `npx codebase-intelligence processes --json ./src` | Manual code path tracing |
| `rename` | Discover all references for safe refactoring | `npx codebase-intelligence rename --json ./src oldName` | Grep + find-replace |

---

## Flags

| Flag | Applies To | Description |
|------|-----------|-------------|
| `--json` | All commands | Machine-readable JSON output (ALWAYS use) |
| `--force` | All commands | Rebuild cache even if valid |
| `--limit <n>` | hotspots, dead-exports, others | Restrict result count |
| `--metric <m>` | hotspots | Select ranking metric (see below) |

---

## Metrics (for `--metric` flag)

| Metric | What It Measures |
|--------|-----------------|
| `pagerank` | Most-referenced files by graph importance |
| `betweenness` | Bridge files connecting disconnected modules |
| `coupling` | File entanglement (fan-out ratio) |
| `cohesion` | Module internal cohesiveness |
| `tension` | Files pulled across modules (entropy-based) |
| `churn` | Git commit frequency |
| `complexity` | Average cyclomatic complexity of exports |
| `blast-radius` | Transitive dependents affected by change |
| `dead-exports` | Unused exports safe for removal |
| `coverage` | Test file existence per source file |
| `escape-velocity` | Module should become its own package |

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

