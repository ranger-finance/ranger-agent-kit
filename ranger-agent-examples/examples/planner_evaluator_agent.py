"""
Planner-Evaluator Agent Example

This script demonstrates a planner-evaluator agent pattern using mcp-agent:
- The planner LLM generates a trading plan (market, side, size, collateral)
- The evaluator LLM critiques/approves the plan
- If approved, the agent executes the plan by calling the MCP server

Requirements:
- Install mcp-agent: pip install mcp-agent
- Start the Ranger MCP server (see USER_MANUAL.md)
- Configure your LLM provider (e.g., OpenAI, Anthropic) as per mcp-agent docs
"""

import asyncio
from mcp_agent.llm.evaluator_optimizer import EvaluatorOptimizerLLM, QualityRating
from mcp_agent.llm.openai import OpenAIAugmentedLLM
from mcp_agent.mcp.gen_client import gen_client

# Example prompts (customize as needed)
PLANNER_PROMPT = """
Given the current market conditions, generate a trading plan for SOL-PERP. Specify side (buy/sell), size, and collateral.
"""
EVALUATOR_PROMPT = """
Evaluate the following trading plan for logic, risk, and market conditions. Approve only if reasonable.
"""


async def main():
    # Set up planner and evaluator LLMs
    planner = OpenAIAugmentedLLM(instruction=PLANNER_PROMPT)
    evaluator = OpenAIAugmentedLLM(instruction=EVALUATOR_PROMPT)
    planner_llm = EvaluatorOptimizerLLM(
        optimizer=planner,
        evaluator=evaluator,
        llm_factory=OpenAIAugmentedLLM,
        min_rating=QualityRating.GOOD,
    )

    # Generate and evaluate a trading plan
    plan = await planner_llm("Generate a trading plan for SOL-PERP.")
    print("Proposed plan:", plan)

    if plan.get("approved", False):
        # Extract plan details
        params = {
            "market": plan.get("market", "SOL-PERP"),
            "side": plan.get("side", "buy"),
            "size": plan.get("size", 1.0),
            "collateral": plan.get("collateral", 100.0),
            "account": "YourSolanaAccountAddressHere"
        }
        # Execute the plan
        async with gen_client("ranger_mcp", base_url="http://localhost:8000") as client:
            try:
                quote = await client.call_tool("sor_get_trade_quote", params)
                print("Trade quote:", quote)
            except Exception as e:
                print("Error executing plan:", e)
    else:
        print("Plan was not approved by evaluator.")

if __name__ == "__main__":
    asyncio.run(main())
