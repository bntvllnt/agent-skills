# Pane Management

Panes are individual terminal areas within a window.

## Split Panes

```bash
# Horizontal split (left | right)
tmux split-window -h

# Vertical split (top / bottom)
tmux split-window -v

# Split with specific size (percentage)
tmux split-window -h -p 30   # 30% width
tmux split-window -v -p 20   # 20% height

# Split with specific size (lines/columns)
tmux split-window -h -l 50   # 50 columns
tmux split-window -v -l 10   # 10 lines

# Split with command
tmux split-window -h htop

# Split in specific directory
tmux split-window -h -c ~/projects

# Key bindings:
# C-b %   Split horizontal
# C-b "   Split vertical
```

## Navigate Panes

```bash
# By direction
tmux select-pane -U   # Up
tmux select-pane -D   # Down
tmux select-pane -L   # Left
tmux select-pane -R   # Right

# By index
tmux select-pane -t :.0
tmux select-pane -t :.1

# Last pane
tmux select-pane -l

# Next pane (cycle)
tmux select-pane -t :.+

# Key bindings:
# C-b Up/Down/Left/Right   Navigate
# C-b o                    Cycle panes
# C-b q                    Show pane numbers (then press number)
# C-b ;                    Last pane
```

## Resize Panes

```bash
# Resize by direction
tmux resize-pane -U 5    # Up 5 lines
tmux resize-pane -D 5    # Down 5 lines
tmux resize-pane -L 10   # Left 10 columns
tmux resize-pane -R 10   # Right 10 columns

# Resize to percentage
tmux resize-pane -x 50%  # 50% width
tmux resize-pane -y 30%  # 30% height

# Resize to specific size
tmux resize-pane -x 80   # 80 columns
tmux resize-pane -y 20   # 20 lines

# Zoom pane (toggle fullscreen)
tmux resize-pane -Z

# Key bindings:
# C-b z                   Toggle zoom
# C-b C-Up/Down/L/R       Resize (hold Ctrl)
# C-b M-Up/Down/L/R       Resize by 5 (hold Alt)
```

## Move/Swap Panes

```bash
# Swap with previous/next
tmux swap-pane -U
tmux swap-pane -D

# Swap with specific pane
tmux swap-pane -t :.2

# Rotate panes
tmux rotate-window         # Clockwise
tmux rotate-window -D      # Counter-clockwise

# Move pane to another window
tmux move-pane -t :2

# Join pane from another window
tmux join-pane -s :2.0     # Source from window 2, pane 0

# Break pane to new window
tmux break-pane

# Key bindings:
# C-b {       Swap with previous
# C-b }       Swap with next
# C-b C-o     Rotate panes
# C-b !       Break pane to window
```

## Kill Pane

**Requires confirmation** if pane has running process.

```bash
# Kill current pane
tmux kill-pane

# Kill specific pane
tmux kill-pane -t :.2

# Kill all except current
tmux kill-pane -a

# Key binding: C-b x (with confirmation)
```

## Pane Info

```bash
# List panes
tmux list-panes

# Detailed format
tmux list-panes -F "#{pane_index}: #{pane_current_command} [#{pane_width}x#{pane_height}]"

# Show pane ID
tmux display-message -p "#{pane_id}"

# Check pane activity
tmux list-panes -F "#{pane_index}: #{pane_current_command} #{?pane_dead,DEAD,}"
```

## Pane Options

```bash
# Set pane border style
tmux set-option pane-border-style "fg=gray"
tmux set-option pane-active-border-style "fg=green"

# Set pane title
tmux select-pane -T "My Pane Title"

# Display pane titles
tmux set-option pane-border-status top
```

## Synchronize Panes

Send input to all panes simultaneously:

```bash
# Toggle synchronization
tmux set-window-option synchronize-panes on
tmux set-window-option synchronize-panes off

# Useful for:
# - Running same command on multiple servers
# - Testing in parallel
```

## Mark Pane

```bash
# Mark pane (for swap/join operations)
tmux select-pane -m

# Clear mark
tmux select-pane -M

# Swap with marked pane
tmux swap-pane
```

## Respawn Pane

```bash
# Respawn dead pane with same command
tmux respawn-pane

# Respawn with different command
tmux respawn-pane "htop"

# Kill existing process and respawn
tmux respawn-pane -k "new-command"
```

## Pane Dimensions

```bash
# Get pane dimensions
tmux display-message -p "#{pane_width}x#{pane_height}"

# Get all pane info
tmux list-panes -F "#{pane_index}: #{pane_width}x#{pane_height} at #{pane_left},#{pane_top}"
```

## Scripting Example

```bash
#!/bin/bash
# Create IDE-like layout

SESSION="ide"

tmux new-session -d -s $SESSION -c ~/project

# Create panes: editor (main), terminal (bottom), sidebar (right)
tmux split-window -v -p 20 -t $SESSION:0   # Bottom terminal
tmux split-window -h -p 25 -t $SESSION:0.0  # Right sidebar

# Name panes
tmux select-pane -t $SESSION:0.0 -T "Editor"
tmux select-pane -t $SESSION:0.1 -T "Sidebar"
tmux select-pane -t $SESSION:0.2 -T "Terminal"

# Send commands
tmux send-keys -t $SESSION:0.0 'nvim .' Enter
tmux send-keys -t $SESSION:0.1 'tree -L 2' Enter

# Focus main editor pane
tmux select-pane -t $SESSION:0.0

tmux attach -t $SESSION
```
