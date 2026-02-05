# Copy Mode

Copy mode allows text selection, searching, and copying from pane history.

## Enter/Exit Copy Mode

```bash
# Enter copy mode
tmux copy-mode

# Key binding: C-b [

# Exit copy mode: q or Escape
```

## Navigation (Vi Mode)

Set vi mode in config:
```bash
set-window-option -g mode-keys vi
```

| Key | Action |
|-----|--------|
| `h j k l` | Left/down/up/right |
| `w b` | Word forward/backward |
| `0 $` | Start/end of line |
| `g G` | Top/bottom of history |
| `C-u C-d` | Page up/down |
| `H M L` | Top/middle/bottom of screen |
| `f F` | Find char forward/backward |
| `/ ?` | Search forward/backward |
| `n N` | Next/previous search match |

## Navigation (Emacs Mode)

Default mode or set explicitly:
```bash
set-window-option -g mode-keys emacs
```

| Key | Action |
|-----|--------|
| `C-p C-n` | Up/down |
| `C-b C-f` | Left/right |
| `M-b M-f` | Word backward/forward |
| `C-a C-e` | Start/end of line |
| `M-< M->` | Top/bottom of history |
| `C-v M-v` | Page down/up |
| `C-s C-r` | Search forward/backward |

## Selection

### Vi Mode

```bash
# Start selection
Space          # Start character-wise selection
v              # Start character-wise selection (alternative)
V              # Start line-wise selection
C-v            # Start block (rectangle) selection

# Modify selection
o              # Move cursor to other end of selection

# Copy selection
Enter          # Copy and exit
y              # Copy and exit (alternative)
```

### Emacs Mode

```bash
# Start selection
C-Space        # Start selection

# Copy selection
M-w            # Copy and exit
```

## Copy to System Clipboard

### macOS

```bash
# In .tmux.conf
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
bind-key -T copy-mode-vi Enter send-keys -X copy-pipe-and-cancel "pbcopy"
```

### Linux (X11)

```bash
# In .tmux.conf
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"
```

### Linux (Wayland)

```bash
# In .tmux.conf
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "wl-copy"
```

## Paste

```bash
# Paste most recent buffer
tmux paste-buffer

# Key binding: C-b ]

# Choose buffer to paste
tmux choose-buffer

# Key binding: C-b =
```

## Buffer Management

```bash
# List buffers
tmux list-buffers

# Key binding: C-b #

# Show buffer content
tmux show-buffer
tmux show-buffer -b buffer0

# Save buffer to file
tmux save-buffer -b buffer0 ~/clipboard.txt

# Load file to buffer
tmux load-buffer ~/clipboard.txt

# Delete buffer
tmux delete-buffer
tmux delete-buffer -b buffer0

# Set buffer content
tmux set-buffer "text content"
```

## Search

### In Copy Mode

```bash
# Forward search
/pattern       # Vi mode
C-s pattern    # Emacs mode

# Backward search
?pattern       # Vi mode
C-r pattern    # Emacs mode

# Next/previous match
n / N          # Vi mode
C-s / C-r      # Emacs mode (repeat)
```

### Incremental Search

```bash
# Enable in config
set-window-option -g incremental-search on
```

## History Limit

```bash
# Set scrollback buffer size (lines)
set-option -g history-limit 50000

# Default is 2000
```

## Mouse Support

```bash
# Enable mouse in config
set-option -g mouse on

# With mouse enabled:
# - Click to position cursor
# - Drag to select
# - Right-click to paste
# - Scroll wheel navigates history
```

## Copy Mode Configuration

```bash
# ~/.tmux.conf

# Vi keys
set-window-option -g mode-keys vi

# Start selection with v
bind-key -T copy-mode-vi v send-keys -X begin-selection

# Rectangle select with C-v
bind-key -T copy-mode-vi C-v send-keys -X rectangle-toggle

# Copy with y
bind-key -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# Don't exit copy mode on mouse release
bind-key -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-selection -x
```

## Scripting Copy Mode

```bash
# Capture pane content
tmux capture-pane -p                    # Print to stdout
tmux capture-pane -S -100               # Last 100 lines
tmux capture-pane -p > pane-content.txt # Save to file

# Capture with escape sequences (colors)
tmux capture-pane -e -p

# Capture entire history
tmux capture-pane -S - -E - -p

# Copy specific text to buffer
tmux set-buffer "specific text"

# Send buffer content to command
tmux save-buffer - | grep "pattern"
```

## Quick Copy Recipes

### Copy Last Command Output

```bash
# Bind to key
bind-key C-c capture-pane -S -1 -E -1 \; save-buffer - \; delete-buffer
```

### Copy Visible Pane

```bash
tmux capture-pane -p
```

### Copy URL Under Cursor

Use plugins like `tmux-urlview` or `tmux-open`:

```bash
# With tmux-urlview
# Press u in copy mode to open urlview
```
