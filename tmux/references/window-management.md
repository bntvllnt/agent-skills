# Window Management

Windows are tabs within a session. Each window contains one or more panes.

## List Windows

```bash
# List windows in current session
tmux list-windows

# List windows in specific session
tmux list-windows -t mysession

# Custom format
tmux list-windows -F "#{window_index}: #{window_name} #{?window_active,*,}"

# Key binding: C-b w (interactive chooser)
```

## Create Window

```bash
# New window
tmux new-window

# Named window
tmux new-window -n mywindow

# Window at specific index
tmux new-window -t :3

# Window in specific session
tmux new-window -t mysession:

# Window with initial command
tmux new-window -n htop htop

# Window in specific directory
tmux new-window -c ~/projects

# Key binding: C-b c
```

## Switch Window

```bash
# By index
tmux select-window -t :0
tmux select-window -t :1

# By name
tmux select-window -t :mywindow

# Last window
tmux select-window -l

# Next/previous
tmux next-window
tmux previous-window

# Key bindings:
# C-b 0-9     Go to window N
# C-b n       Next window
# C-b p       Previous window
# C-b l       Last window
```

## Rename Window

```bash
# Rename current window
tmux rename-window newname

# Rename specific window
tmux rename-window -t :2 newname

# Key binding: C-b ,
```

## Move Window

```bash
# Move to index
tmux move-window -t :5

# Swap windows
tmux swap-window -t :3

# Move to another session
tmux move-window -t othersession:
```

## Link Window

Share a window across sessions:

```bash
# Link window from another session
tmux link-window -s source:2 -t target:

# Unlink window
tmux unlink-window -t :2
```

## Kill Window

**Requires confirmation** - kills all panes in window.

```bash
# Kill current window
tmux kill-window

# Kill specific window
tmux kill-window -t :2

# Kill window by name
tmux kill-window -t :mywindow

# Key binding: C-b & (with confirmation)
```

## Find Window

```bash
# Find window by name/content
tmux find-window searchterm

# Key binding: C-b f
```

## Window Options

```bash
# Set window option
tmux set-window-option automatic-rename off

# Set for all windows
tmux set-window-option -g automatic-rename off

# Show window options
tmux show-window-options
```

## Monitor Activity

```bash
# Enable activity monitoring
tmux set-window-option -t :2 monitor-activity on

# Enable silence monitoring (alert after N seconds of no output)
tmux set-window-option -t :2 monitor-silence 30
```

## Window Styles

```bash
# Set window status style
tmux set-window-option window-status-style "fg=white,bg=black"

# Set active window style
tmux set-window-option window-status-current-style "fg=black,bg=green"
```

## Scripting Example

```bash
#!/bin/bash
# Setup project windows

SESSION="project"

# Ensure session exists
tmux has-session -t $SESSION 2>/dev/null || tmux new-session -d -s $SESSION

# Create windows
tmux new-window -t $SESSION -n code
tmux new-window -t $SESSION -n terminal
tmux new-window -t $SESSION -n git

# Setup each window
tmux send-keys -t $SESSION:code 'nvim .' Enter
tmux send-keys -t $SESSION:git 'lazygit' Enter

# Select first window
tmux select-window -t $SESSION:0
```
