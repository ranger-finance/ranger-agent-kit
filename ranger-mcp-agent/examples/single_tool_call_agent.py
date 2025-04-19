"""
Single Tool Call Agent Example

This script demonstrates how to connect to the Ranger Perps MCP server using mcp-agent,
list available tools, and call the 'sor_get_trade_quote' tool.

Requirements:
- Install mcp-agent: pip install mcp-agent
- Start the Ranger MCP server (see USER_MANUAL.md)
"""

import asyncio
from mcp_agent.mcp.gen_client import gen_client


async def main():
    # Connect to the local MCP server (default: http://localhost:8000)
    async with gen_client("ranger_mcp", base_url="http://localhost:8000") as client:
        print("Connected to Ranger MCP server.")

        # List available tools
        tools = await client.list_tools()
        print("Available tools:", [tool["name"] for tool in tools])

        # Prepare parameters for a trade quote (example values)
        params = {
            "market": "SOL-PERP",
            "side": "buy",
            "size": 1.0,
            "collateral": 100.0,
            "account": "YourSolanaAccountAddressHere"
        }

        # Call the 'sor_get_trade_quote' tool
        try:
            result = await client.call_tool("sor_get_trade_quote", params)
            print("Trade quote result:", result)
        except Exception as e:
            print("Error calling tool:", e)

if __name__ == "__main__":
    asyncio.run(main())
