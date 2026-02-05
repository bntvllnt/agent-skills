# Session Management

Sessions are the top-level containers in tmux. They persist after detaching.

## List Sessions

```bash
# List all sessions
tmux ls
tmux list-sessions

# Detailed format
tmux list-sessions -F "#{session_id}: #{session_name} (#{session_windows} windows) #{?session_attached,attached,detached}"
```

## Create Session

```bash
# New session with default name
tmux new

# Named session
tmux new -s myproject

# Named session with initial window name
tmux new -s myproject -n editor

# Create detached (background)
tmux new -d -s background-job

# Create with initial command
tmux new -s logs -d 'tail -f /var/log/syslog'

# Create in specific directory
tmux new -s project -c ~/projects/myapp
```

## Attach to Session

```bash
# Attach to most recent
tmux attach
tmux a

# Attach to named session
tmux attach -t myproject
tmux a -t myproject

# Attach and detach other clients
tmux attach -d -t myproject

# Create if doesn't exist, attach if does
tmux new -A -s myproject
```

## Detach from Session

```bash
# From command line (inside tmux)
tmux detach

# Key binding: C-b d

# Detach other clients
tmux detach-client -a
```

## Switch Session

```bash
# Switch to named session
tmux switch-client -t other-session

# Previous session
tmux switch-client -l

# Next/previous
tmux switch-client -n
tmux switch-client -p

# Key binding: C-b s (interactive chooser)
# Key binding: C-b ( / C-b ) (prev/next)
```

## Rename Session

```bash
# Rename current session
tmux rename-session newname

# Rename specific session
tmux rename-session -t oldsession newsession

# Key binding: C-b $
```

## Kill Session

**Requires confirmation** - kills all windows and panes.

```bash
# Kill named session
tmux kill-session -t myproject

# Kill all sessions except current
tmux kill-session -a

# Kill all sessions except named
tmux kill-session -a -t keep-this

# Kill entire server (all sessions)
tmux kill-server
```

## Session Info

```bash
# Show session options
tmux show-options -g

# Display session info
tmux display-message -p "Session: #{session_name}, Windows: #{session_windows}"

# Check if session exists
tmux has-session -t myproject && echo "exists"
```

## Session Groups

Link windows across sessions:

```bash
# Create session in group
tmux new -s grouped -t existing-session

# Sessions in same group share windows
```

## Hooks

```bash
# Run command on session creation
set-hook -g session-created 'display-message "New session created"'

# Run command on client attach
set-hook -g client-attached 'refresh-client -S'
```

## Scripting Example

```bash
#!/bin/bash
# Create development environment

SESSION="dev"

# Create session with first window
tmux new-session -d -s $SESSION -n editor

# Create additional windows
tmux new-window -t $SESSION -n server
tmux new-window -t $SESSION -n logs

# Send commands to windows
tmux send-keys -t $SESSION:editor 'nvim .' Enter
tmux send-keys -t $SESSION:server 'npm run dev' Enter
tmux send-keys -t $SESSION:logs 'tail -f logs/*.log' Enter

# Attach to session
tmux attach -t $SESSION
```
