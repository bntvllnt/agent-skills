# tmux Skill

Complete tmux terminal multiplexer management for AI agents.

## What This Does

Enables full tmux control:
- Session lifecycle (create, attach, detach, kill)
- Window management (create, rename, navigate, close)
- Pane operations (split, resize, move, zoom)
- Copy mode and buffers
- Configuration and key bindings
- Scripting and automation

## Entry Points

| Say | Action |
|-----|--------|
| "create tmux session dev" | Create named session |
| "split pane horizontally" | Split current pane |
| "list sessions" | Show all sessions |
| "attach to main" | Attach to session |
| "show tmux config" | Display configuration |

## References

- `references/session-management.md` - Session lifecycle
- `references/window-management.md` - Window operations
- `references/pane-management.md` - Pane operations
- `references/layouts.md` - Layout management
- `references/copy-mode.md` - Copy/paste
- `references/configuration.md` - Config and options
- `references/keybindings.md` - Key binding management
- `references/scripting.md` - Automation and scripting

## Requirements

- tmux 3.0+ installed
- Unix-like OS (Linux/macOS/WSL)
