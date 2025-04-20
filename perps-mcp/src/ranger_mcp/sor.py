import httpx
from typing import Any

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from ranger_mcp.settings import settings
from ranger_mcp.models import (
    QuoteParams,
    IncreasePositionParams,
    DecreasePositionParams,
    ClosePositionParams,
    WithdrawBalanceParams,
    SorApiResponse,
    QuoteResponse
)

# SOR MCP Server instance
sor_mcp = FastMCP("RangerSOR")

# Helper function for making API calls


async def _call_ranger_api(endpoint: str, method: str, data: dict | None = None) -> dict:
    """Calls the Ranger SOR API."""
    headers = {
        "x-api-key": settings.api_key,
        "Content-Type": "application/json"
    }
    url = f"{settings.sor_base_url}{endpoint}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "GET":
                # Currently no GET endpoints in SOR
                raise NotImplementedError(
                    "GET method not implemented for SOR helper")
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx
            return response.json()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_detail = e.response.text
            try:
                error_json = e.response.json()
                error_detail = error_json.get("message", error_detail)
            except Exception:
                pass  # Keep the raw text if JSON parsing fails

            error_msg = f"Ranger API Error ({status_code}): {error_detail}"
            if status_code == 401:
                error_msg = "Ranger API Error (401): Missing or invalid API key. Check your .env file."
            elif status_code == 403:
                error_msg = "Ranger API Error (403): Invalid API Key provided."
            elif status_code == 429:
                error_msg = "Ranger API Error (429): Rate limit exceeded."
            elif status_code == 400:
                error_msg = f"Ranger API Error (400 Bad Request): {error_detail}"

            raise ToolError(error_msg) from e
        except httpx.RequestError as e:
            raise ToolError(f"Network error calling Ranger API: {e}") from e
        except Exception as e:
            # Catch unexpected errors during the request/response processing
            raise ToolError(
                f"Unexpected error interacting with Ranger API: {e}") from e

# --- SOR Tools ---


@sor_mcp.tool(name="get_trade_quote")
async def get_trade_quote(
    params: QuoteParams,
    ctx: Context | None = None  # Optional context for logging etc.
) -> QuoteResponse:
    """
    Get a quote for a potential trade, including price, liquidity, and routing.
    Does NOT execute the trade. Use increase/decrease/close position tools to execute.
    """
    if ctx:
        await ctx.info(f"Getting quote for {params.size} {params.symbol} {params.side}")
    # The quote endpoint returns the meta part of the SorApiResponse directly
    response_data = await _call_ranger_api("/v1/order_metadata", "POST", params.model_dump(exclude_none=True))
    # Validate and return the response using the QuoteResponse model
    return QuoteResponse(**response_data)


@sor_mcp.tool(name="increase_position")
async def increase_position(
    params: IncreasePositionParams,
    ctx: Context | None = None
) -> str:
    """
    Open a new position or increase the size of an existing one.
    Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.
    """
    if ctx:
        await ctx.info(f"Increasing position: {params.size} {params.symbol} {params.side}")
    response_data = await _call_ranger_api("/v1/increase_position", "POST", params.model_dump(exclude_none=True))
    api_response = SorApiResponse(**response_data)
    if ctx:
        await ctx.info(f"Received transaction message. Average price: {api_response.average_price}")
    return api_response.message


@sor_mcp.tool(name="decrease_position")
async def decrease_position(
    params: DecreasePositionParams,
    ctx: Context | None = None
) -> str:
    """
    Decrease the size of an existing position using a specific venue.
    Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.
    """
    if ctx:
        await ctx.info(f"Decreasing position: {params.size} {params.symbol} {params.side} via {params.adjustment_type}")
    response_data = await _call_ranger_api("/v1/decrease_position", "POST", params.model_dump(exclude_none=True))
    api_response = SorApiResponse(**response_data)
    if ctx:
        await ctx.info(f"Received transaction message. Average price: {api_response.average_price}")
    return api_response.message


@sor_mcp.tool(name="close_position")
async def close_position(
    params: ClosePositionParams,
    ctx: Context | None = None
) -> str:
    """
    Close an existing position completely, potentially specifying a venue or closing all.
    Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.
    """
    if ctx:
        await ctx.info(f"Closing position: {params.symbol} {params.side} via {params.adjustment_type}")
    # Note: ClosePositionParams doesn't include size/collateral/denominations as per API doc
    response_data = await _call_ranger_api("/v1/close_position", "POST", params.model_dump(exclude_none=True))
    api_response = SorApiResponse(**response_data)
    if ctx:
        await ctx.info(f"Received transaction message. Average price: {api_response.average_price}")
    return api_response.message


@sor_mcp.tool(name="withdraw_balance_drift")
async def withdraw_balance(
    params: WithdrawBalanceParams,
    ctx: Context | None = None
) -> str:
    """
    Withdraw available balance from a Drift sub-account.
    Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.
    """
    if ctx:
        await ctx.info(f"Withdrawing {params.amount} {params.symbol} from Drift sub-account {params.sub_account_id}")
    response_data = await _call_ranger_api("/v1/withdraw_balance", "POST", params.model_dump(exclude_none=True))
    # Response structure for withdraw_balance is different, directly contains 'message'
    if "message" not in response_data:
        raise ToolError(
            f"Unexpected response format from withdraw_balance: {response_data}")
    if ctx:
        await ctx.info(f"Received withdraw transaction message.")
    return response_data["message"]

# Note: Deposit/Withdraw Collateral endpoints are marked as WIP in the API docs, so they are omitted here.
# They could be added similarly if/when they become available.

@sor_mcp.resource("sor://get_trade_quote")
def resource_get_trade_quote() -> dict:
    return {
        "resource": "get_trade_quote",
        "description": "Get a quote for a potential trade, including price, liquidity, and routing. Does NOT execute the trade.",
        "parameters": ["params"]
    }

@sor_mcp.resource("sor://increase_position")
def resource_increase_position() -> dict:
    return {
        "resource": "increase_position",
        "description": "Open a new position or increase the size of an existing one. Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.",
        "parameters": ["params"]
    }

@sor_mcp.resource("sor://decrease_position")
def resource_decrease_position() -> dict:
    return {
        "resource": "decrease_position",
        "description": "Decrease the size of an existing position using a specific venue. Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.",
        "parameters": ["params"]
    }

@sor_mcp.resource("sor://close_position")
def resource_close_position() -> dict:
    return {
        "resource": "close_position",
        "description": "Close an existing position completely, potentially specifying a venue or closing all. Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.",
        "parameters": ["params"]
    }

@sor_mcp.resource("sor://withdraw_balance_drift")
def resource_withdraw_balance_drift() -> dict:
    return {
        "resource": "withdraw_balance_drift",
        "description": "Withdraw available balance from a Drift sub-account. Returns a base64 encoded transaction message that needs to be signed and submitted by the user/client.",
        "parameters": ["params"]
    }
