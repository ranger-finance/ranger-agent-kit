# Example Agents for Ranger Perps MCP

This folder contains runnable examples of agents built using the [`mcp-agent`](https://github.com/lastmile-ai/mcp-agent) framework, connecting to the [Ranger Perps MCP Server](../../ranger_perps_mcp/README.md).

## Example Patterns

- **Single Tool Call Agent:**
  - Calls a single tool (e.g., get a trade quote) from the MCP server.
- **Multi-Step Orchestrator Agent:**
  - Chains multiple tool calls (e.g., fetch positions, then get a quote, then prepare a transaction).
- **Planner-Evaluator Agent:**
  - Uses a planner LLM to generate a trading plan, and an evaluator LLM to critique or approve it before execution.
- **Human-in-the-Loop Agent:**
  - Pauses for user input or approval at key steps (e.g., before submitting a transaction).

Each script demonstrates how to:

- Connect to the MCP server
- List and call available tools
- Compose workflows using agent patterns

See individual scripts for details and usage instructions.
