"""
Human-in-the-Loop Agent Example

This script demonstrates a workflow where the agent fetches a trade quote,
then pauses for human approval before preparing a transaction.

Requirements:
- Install mcp-agent: pip install mcp-agent
- Start the Ranger MCP server (see USER_MANUAL.md)
"""

import asyncio
from mcp_agent.mcp.gen_client import gen_client
from mcp_agent.human_input.handler import console_input_callback

ACCOUNT = "YourSolanaAccountAddressHere"


async def main():
    async with gen_client("ranger_mcp", base_url="http://localhost:8000") as client:
        print("Connected to Ranger MCP server.")

        # Get a trade quote
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
            return

        # Pause for human approval
        approval = console_input_callback("Approve this trade? (yes/no): ")
        if approval.strip().lower() != "yes":
            print("Trade not approved by user.")
            return

        # Prepare the transaction
        try:
            tx = await client.call_tool("sor_increase_position", params)
            print("Prepared transaction:", tx)
        except Exception as e:
            print("Error preparing transaction:", e)

if __name__ == "__main__":
    asyncio.run(main())
