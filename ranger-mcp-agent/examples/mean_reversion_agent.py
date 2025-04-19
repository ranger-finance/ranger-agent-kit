"""
Mean Reversion Trading Agent Example

This script demonstrates a simple mean reversion strategy using the Ranger MCP server:
- Fetches recent liquidation volumes
- Calculates a Z-score for the latest liquidation event
- If the Z-score exceeds a threshold, gets a trade quote (and optionally prepares a transaction)

Requirements:
- pip install mcp-agent numpy
- Start the Ranger MCP server (see USER_MANUAL.md)
"""

import asyncio
import numpy as np
from mcp_agent.mcp.gen_client import gen_client

ACCOUNT = "YourSolanaAccountAddressHere"
Z_THRESHOLD = 2.0  # Example threshold for signal


async def main():
    async with gen_client("ranger_mcp", base_url="http://localhost:8000") as client:
        # 1. Fetch recent liquidation volumes
        try:
            liq_data = await client.call_tool("data_get_latest_liquidations", {"market": "SOL-PERP", "limit": 20})
            volumes = [item["volume"] for item in liq_data]
            latest = volumes[-1]
            mean = np.mean(volumes[:-1])
            std = np.std(volumes[:-1])
            z = (latest - mean) / std if std > 0 else 0
            print(f"Latest liquidation volume: {latest}, Z-score: {z:.2f}")
        except Exception as e:
            print("Error fetching liquidation data:", e)
            return

        # 2. If Z-score exceeds threshold, get a trade quote
        if z > Z_THRESHOLD:
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
                # Optionally, prepare a transaction:
                # tx = await client.call_tool("sor_increase_position", params)
                # print("Prepared transaction:", tx)
            except Exception as e:
                print("Error getting trade quote or preparing transaction:", e)
        else:
            print("No mean reversion signal detected.")

if __name__ == "__main__":
    asyncio.run(main())
