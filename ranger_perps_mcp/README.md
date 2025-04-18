# Ranger Finance MCP Server

This project provides a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for interacting with the [Ranger Finance API](https://www.app.ranger.finance/trade).

It allows LLMs (like Claude via its desktop app) to query market data and prepare trading transactions using Ranger's Smart Order Router (SOR) and Data APIs.

**Note:** Trading tools (`sor_*`) return base64 encoded transaction messages. These messages **must be signed and submitted** to the Solana network by the user or client application. This MCP server does _not_ handle private keys or transaction signing.

## Features

- **SOR Tools:** Get quotes, prepare transactions to increase, decrease, or close positions.
- **Data Tools:** Fetch positions, trade history, liquidations data (latest, totals, signals, heatmap, largest), funding/borrow rates (arbs, accumulated, extreme, OI-weighted, trend).
- **Modular Design:** Uses FastMCP's `mount` feature to separate SOR and Data API logic.
- **Configuration:** Uses `.env` file for API key and base URLs.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ranger-mcp-server
    ```
2.  **Install dependencies:** We recommend using `uv`.
    ```bash
    uv venv # Create virtual environment
    source .venv/bin/activate # Or .\venv\Scripts\activate on Windows
    uv pip install -e . # Install in editable mode
    ```
3.  **Configure API Key:**
    - Copy `.env.example` to `.env`.
    - Edit `.env` and replace `"sk_test_limited456"` with your actual Ranger API key.
    - Verify the `RANGER_SOR_BASE_URL` and `RANGER_DATA_BASE_URL` are correct.

## Usage

### Running the Server (Standalone)

You can run the server directly using the installed script or python:

```bash
# Using the installed script
ranger-mcp
```

or

```bash
# Using python directly
python src/ranger_mcp/__main__.py
```

This will start the MCP server using the default **stdio** transport.

### Using with FastMCP CLI

You can use the `fastmcp` CLI for development and installation:

- **Development (with Inspector):**
  ```bash
  # Make sure you have Node.js/npm installed for the inspector
  fastmcp dev src/ranger_mcp/hub.py:ranger_mcp
  ```
- **Install in Claude Desktop:**
  ```bash
  # This command assumes Claude Desktop and uv are installed
  # It installs the server with necessary dependencies in an isolated env
  fastmcp install src/ranger_mcp/hub.py:ranger_mcp --name "Ranger Finance API"
  ```

### Interacting with the Server

Once running (either standalone or via `fastmcp install`), you can interact with the server using an MCP client (like Claude Desktop or programmatically using `fastmcp.Client`).

Available tools will be prefixed (e.g., `sor_get_trade_quote`, `data_get_positions`).

**Example Interaction (Conceptual):**

_User (to Claude):_ "Get a quote to buy 1 SOL with 100 USDC collateral using Ranger."
_Claude (using MCP):_ Calls tool `sor_get_trade_quote` with appropriate parameters.
_Claude (to User):_ "Ranger quotes an average price of $XXX.XX for 1 SOL with $100 collateral..."

_User:_ "Okay, execute that trade."
_Claude:_ Calls tool `sor_increase_position`.
_Claude:_ "Okay, I've prepared the transaction. Here is the message: `[base64_message]`. Please sign and submit this using your wallet."
