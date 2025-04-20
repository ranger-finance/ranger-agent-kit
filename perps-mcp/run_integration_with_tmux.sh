#!/bin/bash

SESSION="mcp-test"
SERVER_CMD="source .venv/bin/activate && python src/ranger_mcp/__main__.py"
TEST_CMD="source .venv/bin/activate && sleep 3 && pytest -vv"

# Check for tmux
if ! command -v tmux &> /dev/null; then
  echo "tmux is not installed. Please install tmux and try again."
  exit 1
fi

# Check if session already exists
if tmux has-session -t $SESSION 2>/dev/null; then
  echo "tmux session '$SESSION' already exists. Kill it first or use a different name."
  exit 1
fi

# Start new tmux session and run server in first pane
TMUX="tmux -2"
$TMUX new-session -d -s $SESSION "$SERVER_CMD"

# Split window and run tests in second pane
$TMUX split-window -h -t $SESSION "$TEST_CMD"

# Focus on test pane
$TMUX select-pane -t $SESSION:0.1

# Attach to session so user can see output
$TMUX attach-session -t $SESSION

# After tests finish, kill the session
tmux kill-session -t $SESSION 