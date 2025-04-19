#!/bin/bash

set -e

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "'uv' is not installed. Please install it from https://github.com/astral-sh/uv (e.g., 'pip install uv' or 'brew install uv') and re-run this script."
    exit 1
fi

# Paths
MCP_DIR="ranger_perps_mcp"
AGENT_DIR="ranger-agent-examples/examples"
MCP_VENV="$MCP_DIR/.venv"
MCP_LOG="mcp_server.log"
AGENT_LOG="agent.log"

# 1. Setup MCP server environment
cd "$MCP_DIR"
if [ ! -d ".venv" ]; then
    echo "Creating Python venv for MCP server..."
    uv venv
fi
source .venv/bin/activate

echo "Installing MCP server dependencies..."
uv pip install -e .

# 2. Ensure .env exists
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "Copying .env.example to .env"
    cp .env.example .env
    echo "Please edit $MCP_DIR/.env to add your API key and URLs!"
fi

cd ..

# 3. Install agent dependencies (in user/global env)
uv pip install mcp-agent

# 4. Start tmux session
SESSION="ranger_mcp_demo"
tmux new-session -d -s $SESSION

# 5. Start MCP server in pane 0
tmux send-keys -t $SESSION:0 "cd $MCP_DIR && source .venv/bin/activate && python src/ranger_mcp/__main__.py 2>&1 | tee ../$MCP_LOG" C-m

# 6. Start agent in pane 1
tmux split-window -h -t $SESSION:0
tmux send-keys -t $SESSION:0.1 "cd $AGENT_DIR && python single_tool_call_agent.py 2>&1 | tee ../../$AGENT_LOG" C-m

# 7. Attach to tmux session
tmux select-pane -t $SESSION:0.0
tmux attach-session -t $SESSION 