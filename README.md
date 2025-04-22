<p align="center">
  <img src="assets/rangerAgentKit.png" alt="Ranger Agent Kit Banner" width="320" />
</p>

# ranger-agent-kit

**ranger-agent-kit** is a toolkit and framework for building advanced, modular agents for decentralized perpetuals (perps) trading. It empowers developers, traders, and researchers to automate strategies, interact with DeFi perps protocols, and build next-generation trading infrastructure.

---

## Repository Structure

- **`perps-mcp/`**  
  The core Model Context Protocol (MCP) server for Ranger Perps. Contains the backend code, configuration, and server logic for handling agent requests, market data, and protocol integration.

  - `src/ranger_mcp/`: Main Python package for the MCP server, including data models, API logic, and entrypoint.
  - `USER_MANUAL.md`: Detailed instructions for running and configuring the MCP server.

- **`ranger-agent-examples/`**  
  Example agents and agent orchestration scripts built using the MCP agent framework.

  - `examples/`: Ready-to-run agent scripts (mean reversion, orchestrator, planner, etc.) demonstrating different strategies and workflows.

- **`ranger-web-agent/`**  
  Contains web-based agent demos or notebooks, such as Jupyter notebooks for building autonomous web agents.

---

## Powered by Model Context Protocol & mcp-agent

Ranger Agent Kit is built on top of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) and leverages the [mcp-agent](https://github.com/lastmile-ai/mcp-agent) framework. This enables:

- Seamless integration with any MCP server (including the Ranger Perps MCP server)
- Composable, production-ready agent patterns
- Easy orchestration of LLMs, tool calls, and multi-agent workflows

> Learn more about [mcp-agent](https://github.com/lastmile-ai/mcp-agent) and [MCP](https://modelcontextprotocol.io/introduction).

---

## What Can You Build?

- **Automated Trading Agents**: Fetch real-time market data, get trade quotes, and prepare transactions for perps trading on Solana.
- **Portfolio Management Bots**: Query open positions, trade history, and liquidation data for a given account.
- **LLM-Driven Workflows**: Integrate with LLMs to create conversational trading assistants or automate trading workflows.
- **Mean Reversion & Arbitrage Strategies**: Use liquidation and funding rate data to detect and act on trading opportunities.
- **Custom Integrations**: Easily add new data sources, strategies, or protocol adapters to your agent's toolbox.

---

## Example: Mean Reversion Trading Agent

A simple agent that fetches recent liquidation data, calculates a Z-score, and prepares a trade if a threshold is exceeded.

```python
import asyncio
from ranger_mcp_agent.examples.mean_reversion_agent import run_mean_reversion_agent

if __name__ == "__main__":
    asyncio.run(run_mean_reversion_agent())
```

See more examples in the [`examples/`](./examples) directory, including orchestrator, portfolio, and single-tool-call agents.

---

## Quickstart

1. **Install dependencies:**
   ```bash
   pip install mcp-agent numpy
   ```
2. **Start the Ranger MCP server:**
   - Follow the instructions in [USER_MANUAL.md](./ranger_perps_mcp/USER_MANUAL.md) to start the server (default: http://localhost:8000).
3. **Set your account address:**
   - Edit the `ACCOUNT` variable in the example scripts to your Solana account address.
4. **Run an example agent:**
   ```bash
   python examples/mean_reversion_agent.py
   # or
   python examples/orchestrator_agent.py
   ```
5. **(Optional) Change MCP server URL:**
   - If your MCP server is running elsewhere, update the `base_url` in the scripts.

---

## References

- [Ranger Perps MCP Server](./ranger_perps_mcp/README.md)
- [USER_MANUAL.md](./ranger_perps_mcp/USER_MANUAL.md)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [mcp-agent Examples](https://github.com/lastmile-ai/mcp-agent/tree/main/examples)

---

## Contributing

We welcome all contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Roadmap

- Durable execution and workflow pausing/resuming
- More advanced trading strategies and analytics
- Additional protocol integrations
- Enhanced LLM and agent orchestration features

---

## License

[MIT](./LICENSE)
