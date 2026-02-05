# Layout Management

Layouts control how panes are arranged within a window.

## Built-in Layouts

| Layout | Description |
|--------|-------------|
| `even-horizontal` | Panes spread evenly left to right |
| `even-vertical` | Panes spread evenly top to bottom |
| `main-horizontal` | Large pane on top, others below |
| `main-vertical` | Large pane on left, others on right |
| `tiled` | Panes in grid pattern |

## Apply Layout

```bash
# Apply specific layout
tmux select-layout even-horizontal
tmux select-layout even-vertical
tmux select-layout main-horizontal
tmux select-layout main-vertical
tmux select-layout tiled

# Cycle through layouts
# Key binding: C-b Space

# Previous layout
tmux select-layout -o
```

## Main Pane Size

For `main-horizontal` and `main-vertical` layouts:

```bash
# Set main pane height (for main-horizontal)
tmux set-window-option main-pane-height 60%

# Set main pane width (for main-vertical)
tmux set-window-option main-pane-width 60%

# Set in cells instead of percentage
tmux set-window-option main-pane-height 30
tmux set-window-option main-pane-width 100
```

## Custom Layouts

Layouts can be saved and restored using layout strings:

```bash
# Get current layout string
tmux list-windows -F "#{window_layout}"

# Apply custom layout string
tmux select-layout "layout-string-here"
```

Layout string format: `checksum,width x height,position,pane-info...`

## Layout Examples

### IDE Layout (main + 2 side)

```bash
# Create panes
tmux split-window -h -p 30
tmux split-window -v -t :.1

# Or apply main-vertical
tmux select-layout main-vertical
tmux set-window-option main-pane-width 70%
```

```
┌──────────────────┬──────────┐
│                  │          │
│      Main        │  Side 1  │
│      (70%)       │          │
│                  ├──────────┤
│                  │  Side 2  │
└──────────────────┴──────────┘
```

### Dashboard (2x2 grid)

```bash
tmux split-window -v
tmux split-window -h
tmux select-pane -t :.0
tmux split-window -h
tmux select-layout tiled
```

```
┌──────────┬──────────┐
│   Pane   │   Pane   │
│    0     │    1     │
├──────────┼──────────┤
│   Pane   │   Pane   │
│    2     │    3     │
└──────────┴──────────┘
```

### Horizontal Stack

```bash
tmux split-window -v
tmux split-window -v
tmux select-layout even-vertical
```

```
┌─────────────────────┐
│       Pane 0        │
├─────────────────────┤
│       Pane 1        │
├─────────────────────┤
│       Pane 2        │
└─────────────────────┘
```

### Monitor Layout (1 big + 3 small)

```bash
tmux split-window -h -p 40
tmux split-window -v -t :.1
tmux split-window -v -t :.2
```

```
┌──────────────┬─────────┐
│              │  Pane 1 │
│              ├─────────┤
│    Pane 0    │  Pane 2 │
│    (main)    ├─────────┤
│              │  Pane 3 │
└──────────────┴─────────┘
```

## Persist Layout

Save and restore layouts in `.tmux.conf`:

```bash
# Save a layout
LAYOUT=$(tmux list-windows -F "#{window_layout}")
echo "select-layout $LAYOUT" >> ~/.tmux-layouts/ide.conf

# Restore
tmux source-file ~/.tmux-layouts/ide.conf
```

## Automatic Layout on Window Size

```bash
# Re-apply layout when terminal resizes
set-hook -g client-resized 'select-layout tiled'
```

## Scripting Layouts

```bash
#!/bin/bash
# Create development layout

create_dev_layout() {
    local session=$1
    local window=$2

    # Main editor (left 60%)
    # File tree (top right 40%, height 30%)
    # Terminal (bottom right)

    tmux split-window -h -t $session:$window -p 40
    tmux split-window -v -t $session:$window.1 -p 70

    # Set names
    tmux select-pane -t $session:$window.0 -T "Editor"
    tmux select-pane -t $session:$window.1 -T "Files"
    tmux select-pane -t $session:$window.2 -T "Terminal"
}

# Usage
create_dev_layout "dev" 0
```

## Other Layouts

### Pip (Picture-in-Picture)

Small pane overlaying main:

```bash
# Create popup (tmux 3.2+)
tmux display-popup -E "htop"
```

### Balanced Split

Equal-sized panes regardless of count:

```bash
# After creating panes
tmux select-layout tiled
```
