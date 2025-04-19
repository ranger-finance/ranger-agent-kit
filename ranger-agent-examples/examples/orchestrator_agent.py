"""
Orchestrator Agent Example

This script demonstrates a multi-step workflow using mcp-agent:
1. Fetch open positions for an account
2. Get a trade quote
3. Prepare a transaction to increase position

Requirements:
- Install mcp-agent: pip install mcp-agent
- Start the Ranger MCP server (see USER_MANUAL.md)
"""

import asyncio
from mcp_agent.mcp.gen_client import gen_client

ACCOUNT = "YourSolanaAccountAddressHere"


async def main():
    async with gen_client("ranger_mcp", base_url="http://localhost:8000") as client:
        print("Connected to Ranger MCP server.")

        # 1. Fetch open positions
        try:
            positions = await client.call_tool("data_get_positions", {"account": ACCOUNT})
            print("Open positions:", positions)
        except Exception as e:
            print("Error fetching positions:", e)
            positions = None

        # 2. Get a trade quote
        params = {
            "market": "SOL-PERP",
            "side": "buy",
            "size": 1.0,
            "collateral": 100.0,
            "account": ACCOUNT
        }
        try:
            quote = await client.call_tool("sor_get_trade_quote", params)
            print("Trade quote:", quote)
        except Exception as e:
            print("Error getting trade quote:", e)
            quote = None

        # 3. Prepare a transaction to increase position (if quote succeeded)
        if quote:
            try:
                tx_params = params.copy()
                tx_params["quote_id"] = quote.get(
                    "quote_id")  # If required by your API
                tx = await client.call_tool("sor_increase_position", tx_params)
                print("Prepared transaction:", tx)
            except Exception as e:
                print("Error preparing transaction:", e)

if __name__ == "__main__":
    asyncio.run(main())
