# Configuration

tmux configuration via `~/.tmux.conf` and options.

## Config File

```bash
# Default location
~/.tmux.conf

# Alternative locations
~/.config/tmux/tmux.conf    # XDG compliant
/etc/tmux.conf              # System-wide

# Reload config
tmux source-file ~/.tmux.conf

# Bind reload to key
bind-key r source-file ~/.tmux.conf \; display-message "Config reloaded"
```

## Option Types

| Type | Scope | Set Command |
|------|-------|-------------|
| Server | Entire server | `set-option -s` |
| Session | Single/all sessions | `set-option` / `set-option -g` |
| Window | Single/all windows | `set-window-option` / `set-window-option -g` |
| Pane | Single pane | `set-option -p` |

## Common Options

### General

```bash
# Set prefix key
set-option -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix

# Start windows/panes at 1 (not 0)
set-option -g base-index 1
set-window-option -g pane-base-index 1

# Renumber windows when one is closed
set-option -g renumber-windows on

# History limit
set-option -g history-limit 50000

# Enable mouse
set-option -g mouse on

# Escape time (for vim)
set-option -sg escape-time 0

# Repeat time for key bindings
set-option -g repeat-time 500
```

### Display

```bash
# Terminal colors
set-option -g default-terminal "tmux-256color"
set-option -ga terminal-overrides ",xterm-256color:Tc"

# Focus events (for vim)
set-option -g focus-events on

# Status bar position
set-option -g status-position top

# Display time for messages
set-option -g display-time 3000

# Display time for pane numbers
set-option -g display-panes-time 3000
```

### Key Modes

```bash
# Vi mode in copy
set-window-option -g mode-keys vi

# Vi mode in status line (command prompt)
set-option -g status-keys vi
```

## Status Line

```bash
# Status bar colors
set-option -g status-style "bg=#282a36,fg=#f8f8f2"

# Left side
set-option -g status-left-length 50
set-option -g status-left "[#S] "

# Right side
set-option -g status-right-length 100
set-option -g status-right "#H | %Y-%m-%d %H:%M"

# Window status
set-window-option -g window-status-format " #I:#W "
set-window-option -g window-status-current-format " #I:#W* "
set-window-option -g window-status-current-style "bg=blue,fg=white"

# Separator
set-window-option -g window-status-separator ""

# Update interval (seconds)
set-option -g status-interval 5
```

### Status Line Variables

| Variable | Description |
|----------|-------------|
| `#S` | Session name |
| `#W` | Window name |
| `#I` | Window index |
| `#P` | Pane index |
| `#H` | Hostname |
| `#h` | Hostname (short) |
| `#T` | Pane title |
| `#F` | Window flags |

## Pane Borders

```bash
# Border colors
set-option -g pane-border-style "fg=#444444"
set-option -g pane-active-border-style "fg=#00ff00"

# Show pane titles in border
set-option -g pane-border-status top
set-option -g pane-border-format " #{pane_index}: #{pane_title} "
```

## Window Options

```bash
# Automatic rename
set-window-option -g automatic-rename on
set-window-option -g automatic-rename-format "#{pane_current_command}"

# Activity monitoring
set-window-option -g monitor-activity on
set-option -g visual-activity on

# Aggressive resize
set-window-option -g aggressive-resize on
```

## View/Modify Options

```bash
# Show all global options
tmux show-options -g

# Show all window options
tmux show-window-options -g

# Show specific option
tmux show-options -g status-style

# Show option value only
tmux show-options -gv status-style
```

## Conditional Configuration

```bash
# Check tmux version
%if #{>=:#{version},3.2}
    # tmux 3.2+ settings
    set-option -g extended-keys on
%endif

# Check if SSH session
%if #{SSH_CONNECTION}
    set-option -g status-right "SSH | #H"
%endif

# Check OS
%if #{==:#{host},Darwin}
    # macOS settings
    bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
%endif
```

## User Options

Custom options prefixed with `@`:

```bash
# Set user option
set-option -g @my-setting "value"

# Read user option
tmux show-options -gv @my-setting
```

## Environment Variables

```bash
# Update environment on attach
set-option -g update-environment "SSH_AUTH_SOCK SSH_AGENT_PID"

# Set environment variable
set-environment -g MY_VAR "value"

# Unset
set-environment -g -u MY_VAR
```

## Example Configuration

```bash
# ~/.tmux.conf

# --- General ---
set-option -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix

set-option -g base-index 1
set-window-option -g pane-base-index 1
set-option -g renumber-windows on
set-option -g history-limit 50000
set-option -g mouse on
set-option -sg escape-time 0

# --- Display ---
set-option -g default-terminal "tmux-256color"
set-option -ga terminal-overrides ",xterm-256color:Tc"
set-option -g focus-events on

# --- Keys ---
set-window-option -g mode-keys vi
set-option -g status-keys vi

# Vim-style pane navigation
bind-key h select-pane -L
bind-key j select-pane -D
bind-key k select-pane -U
bind-key l select-pane -R

# Easy splits
bind-key | split-window -h -c "#{pane_current_path}"
bind-key - split-window -v -c "#{pane_current_path}"

# New window in current path
bind-key c new-window -c "#{pane_current_path}"

# --- Status ---
set-option -g status-position top
set-option -g status-style "bg=#1e1e2e,fg=#cdd6f4"
set-option -g status-left "[#S] "
set-option -g status-right "#H | %H:%M"
set-window-option -g window-status-current-style "bg=#89b4fa,fg=#1e1e2e"

# --- Borders ---
set-option -g pane-border-style "fg=#45475a"
set-option -g pane-active-border-style "fg=#89b4fa"

# --- Clipboard ---
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# --- Reload ---
bind-key r source-file ~/.tmux.conf \; display-message "Config reloaded"
```
