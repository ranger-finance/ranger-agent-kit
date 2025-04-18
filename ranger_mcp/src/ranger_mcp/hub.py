import fastmcp
from fastmcp import FastMCP
from ranger_mcp.sor import sor_mcp
from ranger_mcp.data import data_mcp
from ranger_mcp.settings import settings

# Main Ranger MCP Hub Server instance
# You can add dependencies needed by *any* mounted server here,
# or manage them within each sub-server's FastMCP definition.
ranger_mcp = FastMCP(
    "RangerFinance",
    instructions=(
        "This server allows interaction with Ranger Finance APIs. "
        "Use 'sor_*' tools for trading operations (quote, increase, decrease, close) "
        "and 'data_*' tools for fetching market data (positions, history, liquidations, funding)."
        " Trading tools return base64 transaction messages that need external signing."
    ),
    # Example of adding dependencies needed by sub-servers if not defined there
    # dependencies=["httpx>=0.25.0", "pydantic-settings>=2.0.0"]
)

# Mount the SOR and Data sub-servers
# We use simple prefixes 'sor' and 'data'
ranger_mcp.mount("sor", sor_mcp)
ranger_mcp.mount("data", data_mcp)

# Optional: Add a top-level status tool for the hub


@ranger_mcp.tool()
async def ranger_status() -> dict:
    """Checks the status of the Ranger MCP Hub and base URLs."""
    # Simple check, could be enhanced to ping API endpoints
    return {
        "status": "OK",
        "sor_base_url": str(settings.sor_base_url),
        "data_base_url": str(settings.data_base_url),
        "fastmcp_version": fastmcp.__version__
    }
