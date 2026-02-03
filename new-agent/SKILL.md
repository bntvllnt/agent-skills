---
name: new-agent
description: |
  Create a new OpenClaw agent workspace repo + Discord channel following the jarvis-workspace standard.
  Triggers: "new agent", "create agent", "bootstrap agent", "agent workspace", "create workspace repo".
license: MIT
compatibility: Requires `gh` + git, and OpenClaw Discord + cron tooling.
metadata:
  version: "0.1"
allowed-tools: exec read write edit message cron
---

# New Agent (workspace bootstrap)

Create a brand-new agent/workspace that **inherits shared protocols, thinking patterns, and templates** via the shared-library submodule, and enforces the strict GitHub/Discord standards.

## Router

| If the user says… | Do this |
|---|---|
| “create a new agent …” | Run **Bootstrap (full)** |
| “create the discord channel only” | Run **Discord channel only** |
| “harden repo settings / protections” | Run **Harden existing repo** |
| “update shared mapping” | Run **Update TOOLS mapping** |

## Safety / invariants

- Never push directly to `main` (branch protection will enforce it).
- Never enable force-push or allow main deletion.
- Keep shared-library mapping file **local-only** (do not commit `TOOLS.md` into openclaw-shared-library; pre-commit blocks it).

## Bootstrap (full)

### Inputs
- agentName (kebab-case suggested): e.g. `sentry`, `atlas`, `nova`
- owner (default `bntvllnt`)
- visibility (default `private`)
- description (1 line)
- topics (default jarvis set)

### Steps

1) **Create/harden GitHub repo**

Repo name: `<agentName>-workspace`

Apply the jarvis-workspace standard:
- projects/wiki off
- squash-only merges
- delete branch on merge
- auto-merge on
- branch protection on `main`:
  - PR required
  - 1 approval
  - dismiss stale approvals
  - require conversation resolution
  - require linear history
  - no force pushes
  - no deletion
  - enforce admins

2) **Clone + scaffold local workspace**

Local path: `/home/ubuntu/.openclaw/<agentName>-workspace`

Add shared library as submodule:
- path: `library/`
- url: `https://github.com/bntvllnt/openclaw-shared-library.git`

3) **Discord channel**

Create `#<agentName>-workspace` under the repos category.
Set topic:
`Repo: https://github.com/<owner>/<agentName>-workspace — autopilot logs + threads for work items.`

4) **Update mapping** (local-only)

Update:
`/home/ubuntu/.openclaw/shared-library/TOOLS.md`

Add line:
`owner/repo -> channelId`

5) **4am sync cron**

Ensure the 4am sync cron exists and will include this new repo (either by scanning the mapping or by adding the path).

## References

- Script (shared-library): `library/scripts/new-agent.sh`
- Discord category id (repos): `1468025498872582350`
- Guild id: `1360625061853401378`
