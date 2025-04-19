# How Are the Example Agents Built?

The example agents in this repository are built using the [`mcp-agent`](https://github.com/lastmile-ai/mcp-agent) framework, which provides a flexible foundation for constructing AI-driven workflows that interact with the Ranger Perps MCP server.

## General Architecture

- **MCP Client:** Each agent uses `mcp-agent`'s `gen_client` to connect to the MCP server (usually at `http://localhost:8000`).
- **Async/Await:** All agents are written using Python's `asyncio` for efficient, non-blocking tool calls.
- **Tool Calls:** Agents interact with the MCP server by calling tools such as `sor_get_trade_quote`, `data_get_positions`, and others.
- **Workflow Patterns:**
  - **Single Tool Call Agent:** Demonstrates a minimal agent that calls one tool (e.g., fetches a trade quote).
  - **Orchestrator Agent:** Chains multiple tool calls in a logical sequence (e.g., fetch positions, get a quote, prepare a transaction).
  - **Planner-Evaluator Agent:** Uses LLMs for plan generation and evaluation before executing trades. Built with `EvaluatorOptimizerLLM` from `mcp-agent`.
  - **Human-in-the-Loop Agent:** Pauses for user input/approval at key steps, using `console_input_callback` from `mcp-agent`.
  - **Mean Reversion Agent:** Implements a simple trading strategy by analyzing liquidation data and acting on statistical signals.
- **Extensibility:** You can easily adapt or extend these patterns to build more complex agents, integrate additional LLMs, or automate new trading strategies.

## Implementation Details

- **Configuration:** Each agent script specifies the MCP server URL and account details.
- **Error Handling:** Basic error handling is included for robustness.
- **LLM Integration:** Planner-evaluator agents use LLMs (e.g., OpenAI, Anthropic) for advanced decision-making.
- **Data Analysis:** Some agents (e.g., mean reversion) use libraries like `numpy` for statistical calculations.

See the `examples/` folder for code and comments illustrating each pattern.
