# Ranger MCP Agent Examples

This folder demonstrates how to build AI agents that interact with the [Ranger Perps MCP Server](../ranger_perps_mcp/README.md) using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) and the [`mcp-agent`](https://github.com/lastmile-ai/mcp-agent) framework.

## What can you build with `ranger_perps_mcp`?

- **Automated Trading Agents:**
  - Fetch real-time market data, get trade quotes, and prepare transactions for perpetuals trading on Solana.
  - Use SOR tools to generate and manage trading transactions (increase, decrease, close positions, withdraw, etc.).
- **Portfolio Management Bots:**
  - Query open positions, trade history, and liquidation data for a given account.
  - Build dashboards or notification systems for portfolio health and risk.
- **LLM-Driven Workflows:**
  - Integrate with LLMs (like Claude, GPT-4, etc.) to create conversational trading assistants.
  - Use agent patterns (orchestrator, planner-evaluator, human-in-the-loop) to automate or semi-automate trading workflows.

## Example Agents

This folder contains example agents that demonstrate:

- Connecting to the Ranger MCP server as an MCP client
- Calling tools such as `sor_get_trade_quote` and `data_get_positions`
- Composing multi-step workflows using the [`mcp-agent`](https://github.com/lastmile-ai/mcp-agent) framework

See the `examples/` subfolder for runnable agent scripts and workflow patterns.

## References

- [Ranger Perps MCP Server](../ranger_perps_mcp/README.md)
- [USER_MANUAL.md](../ranger_perps_mcp/USER_MANUAL.md)
- [`mcp-agent` framework](https://github.com/lastmile-ai/mcp-agent)
- [Anthropic agent patterns](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)
