# Key Bindings

Customize tmux key bindings.

## Binding Syntax

```bash
# Basic binding
bind-key key command

# With prefix (default)
bind-key -T prefix key command

# Without prefix (root table)
bind-key -T root key command

# In copy mode
bind-key -T copy-mode-vi key command
bind-key -T copy-mode key command

# Repeat without prefix
bind-key -r key command
```

## Key Tables

| Table | Description |
|-------|-------------|
| `root` | Active without prefix |
| `prefix` | After pressing prefix (C-b) |
| `copy-mode` | In emacs copy mode |
| `copy-mode-vi` | In vi copy mode |

## List Bindings

```bash
# All bindings
tmux list-keys

# Specific table
tmux list-keys -T prefix
tmux list-keys -T copy-mode-vi

# Key binding: C-b ?
```

## Unbind

```bash
# Unbind in prefix table
unbind-key key

# Unbind in specific table
unbind-key -T root key
unbind-key -T copy-mode-vi key

# Unbind all
unbind-key -a
```

## Common Rebindings

### Change Prefix

```bash
# Use C-a instead of C-b
set-option -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix

# Double-tap prefix to send to app
bind-key a send-prefix
```

### Vim-Style Navigation

```bash
# Pane navigation
bind-key h select-pane -L
bind-key j select-pane -D
bind-key k select-pane -U
bind-key l select-pane -R

# Window navigation
bind-key -r C-h select-window -t :-
bind-key -r C-l select-window -t :+
```

### Vim-Style Resize

```bash
# Resize panes (repeatable)
bind-key -r H resize-pane -L 5
bind-key -r J resize-pane -D 5
bind-key -r K resize-pane -U 5
bind-key -r L resize-pane -R 5
```

### Better Splits

```bash
# More intuitive split keys
bind-key | split-window -h -c "#{pane_current_path}"
bind-key - split-window -v -c "#{pane_current_path}"
bind-key _ split-window -v -c "#{pane_current_path}"

# Retain current path in new window
bind-key c new-window -c "#{pane_current_path}"
```

### Quick Actions

```bash
# Reload config
bind-key r source-file ~/.tmux.conf \; display-message "Config reloaded"

# Toggle synchronize panes
bind-key S set-window-option synchronize-panes

# Quick session switch
bind-key s choose-tree -Zs

# Kill pane without confirm
bind-key x kill-pane

# Kill window without confirm
bind-key X kill-window
```

## Copy Mode Bindings

```bash
# Vi-style copy mode
set-window-option -g mode-keys vi

# Selection
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi C-v send-keys -X rectangle-toggle
bind-key -T copy-mode-vi V send-keys -X select-line

# Copy
bind-key -T copy-mode-vi y send-keys -X copy-selection-and-cancel
bind-key -T copy-mode-vi Enter send-keys -X copy-selection-and-cancel

# System clipboard (macOS)
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# System clipboard (Linux)
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# Search
bind-key -T copy-mode-vi / command-prompt -i -p "Search:" "send-keys -X search-forward-incremental \"%%%\""
```

## Mouse Bindings

```bash
# Enable mouse
set-option -g mouse on

# Don't exit copy mode on mouse release
unbind-key -T copy-mode-vi MouseDragEnd1Pane

# Right click to paste
bind-key -T root MouseDown3Pane paste-buffer
```

## Root Table Bindings

Bindings that work without prefix:

```bash
# Alt+arrow pane navigation
bind-key -T root M-Left select-pane -L
bind-key -T root M-Right select-pane -R
bind-key -T root M-Up select-pane -U
bind-key -T root M-Down select-pane -D

# Alt+number window switch
bind-key -T root M-1 select-window -t :1
bind-key -T root M-2 select-window -t :2
bind-key -T root M-3 select-window -t :3
```

## Repeatable Bindings

Use `-r` for bindings that can repeat without pressing prefix again:

```bash
# Resize with repeat
bind-key -r H resize-pane -L 2
bind-key -r J resize-pane -D 2
bind-key -r K resize-pane -U 2
bind-key -r L resize-pane -R 2

# Navigate windows with repeat
bind-key -r n next-window
bind-key -r p previous-window

# Set repeat time (ms)
set-option -g repeat-time 500
```

## Conditional Bindings

```bash
# Different behavior based on zoom state
bind-key z if-shell "tmux list-panes -F '#F' | grep -q Z" \
    "resize-pane -Z" \
    "resize-pane -Z"

# Toggle based on option
bind-key m if-shell "tmux show-options -w | grep -q 'monitor-activity on'" \
    "set-window-option monitor-activity off" \
    "set-window-option monitor-activity on"
```

## Run Commands

```bash
# Run shell command
bind-key T run-shell "date"

# Run in popup (tmux 3.2+)
bind-key G display-popup -E "lazygit"
bind-key F display-popup -E "fzf"

# Run and capture output
bind-key W run-shell "tmux list-windows | wc -l | xargs tmux display-message"
```

## Send Keys

```bash
# Send literal keys
bind-key C-l send-keys C-l  # Clear screen

# Send key sequence
bind-key C-k send-keys "clear" Enter
```

## Display Bindings

```bash
# Show all bindings
bind-key ? list-keys

# Show specific binding
# tmux list-keys | grep "key"
```

## Complete Example

```bash
# ~/.tmux.conf keybindings section

# Prefix
set-option -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix

# Reload
bind-key r source-file ~/.tmux.conf \; display-message "Reloaded"

# Splits
bind-key | split-window -h -c "#{pane_current_path}"
bind-key - split-window -v -c "#{pane_current_path}"

# Navigation (vim)
bind-key h select-pane -L
bind-key j select-pane -D
bind-key k select-pane -U
bind-key l select-pane -R

# Resize (vim, repeatable)
bind-key -r H resize-pane -L 5
bind-key -r J resize-pane -D 5
bind-key -r K resize-pane -U 5
bind-key -r L resize-pane -R 5

# Windows
bind-key -r n next-window
bind-key -r p previous-window
bind-key c new-window -c "#{pane_current_path}"

# Copy mode
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# Quick actions
bind-key S set-window-option synchronize-panes
bind-key x kill-pane
bind-key X kill-window

# Popups (tmux 3.2+)
bind-key g display-popup -E -w 80% -h 80% "lazygit"
```
