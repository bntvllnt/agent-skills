# Scripting & Automation

Programmatic tmux control for automation and scripting.

## Target Syntax

Target format: `session:window.pane`

```bash
# Session only
tmux send-keys -t mysession "command"

# Session and window (by index)
tmux send-keys -t mysession:2 "command"

# Session and window (by name)
tmux send-keys -t mysession:editor "command"

# Full target with pane
tmux send-keys -t mysession:2.1 "command"

# Current session
tmux send-keys -t :2 "command"

# Current window
tmux send-keys -t :.1 "command"

# Using IDs
tmux send-keys -t $0      # Session ID
tmux send-keys -t @2      # Window ID
tmux send-keys -t %5      # Pane ID
```

## Send Keys

```bash
# Send text
tmux send-keys -t target "echo hello"

# Send with Enter
tmux send-keys -t target "echo hello" Enter

# Send special keys
tmux send-keys -t target C-c          # Ctrl+C
tmux send-keys -t target C-d          # Ctrl+D
tmux send-keys -t target Escape       # Escape
tmux send-keys -t target Tab          # Tab
tmux send-keys -t target BSpace       # Backspace
tmux send-keys -t target Up Down      # Arrows

# Send literal text (no key interpretation)
tmux send-keys -t target -l "C-c is not Ctrl+C"

# Clear and send
tmux send-keys -t target C-c C-l "command" Enter
```

## Capture Pane Content

```bash
# Capture visible pane
tmux capture-pane -t target -p

# Capture with history
tmux capture-pane -t target -p -S -100    # Last 100 lines
tmux capture-pane -t target -p -S -       # Entire history

# Capture range
tmux capture-pane -t target -p -S 10 -E 20

# Capture with escape sequences (colors)
tmux capture-pane -t target -p -e

# Save to file
tmux capture-pane -t target -p > output.txt

# Capture to buffer
tmux capture-pane -t target -b mybuffer
tmux save-buffer -b mybuffer output.txt
```

## Display Message

```bash
# Display in status line
tmux display-message "Hello"

# Print to stdout
tmux display-message -p "Hello"

# With formats
tmux display-message -p "Session: #{session_name}"
tmux display-message -p "Window: #{window_index}:#{window_name}"
tmux display-message -p "Pane: #{pane_id} running #{pane_current_command}"
```

## Format Strings

Common format variables:

| Variable | Description |
|----------|-------------|
| `#{session_id}` | Session ID ($N) |
| `#{session_name}` | Session name |
| `#{session_windows}` | Number of windows |
| `#{window_id}` | Window ID (@N) |
| `#{window_index}` | Window index |
| `#{window_name}` | Window name |
| `#{window_active}` | 1 if active |
| `#{pane_id}` | Pane ID (%N) |
| `#{pane_index}` | Pane index |
| `#{pane_current_path}` | Current directory |
| `#{pane_current_command}` | Running command |
| `#{pane_pid}` | Process ID |
| `#{pane_width}` | Width in columns |
| `#{pane_height}` | Height in lines |

```bash
# List with custom format
tmux list-sessions -F "#{session_id}: #{session_name} (#{session_windows} windows)"
tmux list-windows -F "#{window_index}: #{window_name}"
tmux list-panes -F "#{pane_index}: #{pane_current_command} [#{pane_width}x#{pane_height}]"
```

## Conditionals in Formats

```bash
# Ternary
tmux list-windows -F "#{window_index}: #{?window_active,*,} #{window_name}"

# Comparison
tmux list-panes -F "#{?#{==:#{pane_current_command},vim},EDITING,OTHER}"

# Nested
tmux display-message -p "#{?#{>:#{window_width},100},Wide,#{?#{<:#{window_width},50},Narrow,Normal}}"
```

## Wait and Synchronization

```bash
# Wait for channel
tmux wait-for channel-name

# Signal channel
tmux wait-for -S channel-name

# Lock channel
tmux wait-for -L channel-name
tmux wait-for -U channel-name    # Unlock

# Example: Wait for command completion
tmux send-keys -t target "long-command; tmux wait-for -S done" Enter
tmux wait-for done
echo "Command finished"
```

## Run Shell Command

```bash
# Run and display output
tmux run-shell "date"

# Run in background
tmux run-shell -b "sleep 5; tmux display-message 'Done'"

# Run in specific pane
tmux run-shell -t target "pwd"
```

## Hooks

```bash
# Session hooks
set-hook -g session-created 'display-message "Session created"'
set-hook -g session-closed 'run-shell "echo closed >> ~/tmux.log"'

# Window hooks
set-hook -g window-linked 'display-message "Window added"'
set-hook -g window-unlinked 'display-message "Window removed"'

# Pane hooks
set-hook -g pane-focus-in 'run-shell "echo #{pane_id} focused"'
set-hook -g pane-exited 'display-message "Pane exited"'

# Client hooks
set-hook -g client-attached 'refresh-client -S'
set-hook -g client-detached 'display-message "Client detached"'

# Alert hooks
set-hook -g alert-activity 'display-message "Activity in #{window_name}"'

# List hooks
tmux show-hooks -g

# Remove hook
set-hook -gu session-created
```

## Scripting Examples

### Development Environment

```bash
#!/bin/bash
SESSION="dev"
PROJECT_DIR="$HOME/project"

# Kill existing session
tmux kill-session -t $SESSION 2>/dev/null

# Create session with editor window
tmux new-session -d -s $SESSION -n editor -c $PROJECT_DIR

# Split for terminal
tmux split-window -t $SESSION:editor -v -p 30 -c $PROJECT_DIR

# Create server window
tmux new-window -t $SESSION -n server -c $PROJECT_DIR

# Create logs window with splits
tmux new-window -t $SESSION -n logs -c $PROJECT_DIR
tmux split-window -t $SESSION:logs -h -c $PROJECT_DIR

# Send commands
tmux send-keys -t $SESSION:editor.0 "nvim ." Enter
tmux send-keys -t $SESSION:server "npm run dev" Enter
tmux send-keys -t $SESSION:logs.0 "tail -f logs/app.log" Enter
tmux send-keys -t $SESSION:logs.1 "tail -f logs/error.log" Enter

# Select editor window
tmux select-window -t $SESSION:editor

# Attach
tmux attach -t $SESSION
```

### Monitoring Dashboard

```bash
#!/bin/bash
SESSION="monitor"

tmux new-session -d -s $SESSION -n dashboard

# Create 2x2 grid
tmux split-window -t $SESSION -h
tmux split-window -t $SESSION:0.0 -v
tmux split-window -t $SESSION:0.2 -v

# Send monitoring commands
tmux send-keys -t $SESSION:0.0 "htop" Enter
tmux send-keys -t $SESSION:0.1 "watch -n 1 'df -h'" Enter
tmux send-keys -t $SESSION:0.2 "tail -f /var/log/syslog" Enter
tmux send-keys -t $SESSION:0.3 "nethogs" Enter

tmux attach -t $SESSION
```

### CI/CD Runner

```bash
#!/bin/bash
# Run tests in tmux, wait for completion

SESSION="ci-$$"
tmux new-session -d -s $SESSION "npm test; tmux wait-for -S tests-done"
tmux wait-for tests-done

# Capture output
OUTPUT=$(tmux capture-pane -t $SESSION -p -S -)
tmux kill-session -t $SESSION

# Check result
if echo "$OUTPUT" | grep -q "PASS"; then
    echo "Tests passed"
    exit 0
else
    echo "Tests failed"
    echo "$OUTPUT"
    exit 1
fi
```

### Remote Execution

```bash
#!/bin/bash
# Execute command on multiple servers

SERVERS=("server1" "server2" "server3")
COMMAND="uptime"
SESSION="multi-exec"

tmux new-session -d -s $SESSION

for i in "${!SERVERS[@]}"; do
    if [ $i -gt 0 ]; then
        tmux split-window -t $SESSION
        tmux select-layout -t $SESSION tiled
    fi
    tmux send-keys -t $SESSION:0.$i "ssh ${SERVERS[$i]} '$COMMAND'" Enter
done

# Synchronize input
tmux set-window-option -t $SESSION synchronize-panes on
tmux attach -t $SESSION
```

## Control Mode

For programmatic integration:

```bash
# Start in control mode
tmux -C

# Or attach in control mode
tmux -C attach

# Outputs structured events like:
# %begin 1234567890 1 0
# %end 1234567890 1 0
# %window-add @1
# %session-changed $0 main
```
