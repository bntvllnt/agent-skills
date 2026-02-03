# new-agent

Bootstraps a new OpenClaw agent workspace repo + Discord channel using the **jarvis-workspace** standard.

What it enforces:
- GitHub: squash-only merges, delete-branch-on-merge, projects/wiki off
- Branch protection on `main`: PR-only, 1 approval, linear history, conversation resolution, no force push, no deletion, admins included
- Shared protocols/templates via `library/` submodule (openclaw-shared-library)
- Discord channel creation + local repo→channel mapping

See `SKILL.md` for the router + procedure.
