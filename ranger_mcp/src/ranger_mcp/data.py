import httpx
from typing import Any, Literal
from pydantic import Field

from fastmcp import FastMCP, Context
from ranger_mcp.settings import settings
from ranger_mcp.models import (
    Platform, SizeDenomination,
    GetPositionsResponse, GetTradeHistoryResponse, Liquidation, LiquidationTotals,
    CapitulationSignal, LiquidationHeatmapEntry, LargestLiquidation, FundingRateArb,
    AccumulatedRate, ExtremeFundingRates, OiWeightedFundingRate, FundingRateTrend
)
from fastmcp.exceptions import ToolError

# Data MCP Server instance
data_mcp = FastMCP("RangerData")

# Helper function for making API calls


async def _call_ranger_data_api(endpoint: str, params: dict[str, Any] | None = None) -> Any:
    """Calls the Ranger Data API."""
    headers = {"x-api-key": settings.api_key}
    url = f"{settings.data_base_url}{endpoint}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_detail = e.response.text
            try:
                error_detail = e.response.json().get("message", error_detail)
            except Exception:
                pass
            error_msg = f"Ranger Data API Error ({status_code}): {error_detail}"
            # Add specific error messages if needed
            raise ToolError(error_msg) from e
        except httpx.RequestError as e:
            raise ToolError(
                f"Network error calling Ranger Data API: {e}") from e
        except Exception as e:
            raise ToolError(
                f"Unexpected error interacting with Ranger Data API: {e}") from e

# --- Data Tools (Using tools because GET params are needed) ---


@data_mcp.tool(name="get_positions")
async def get_positions(
    public_key: str = Field(description="User's Solana wallet address"),
    platforms: list[Platform] | None = Field(
        default=None, description="Optional list of platforms to filter by (e.g., ['DRIFT', 'FLASH'])"),
    symbols: list[str] | None = Field(
        default=None, description="Optional list of symbols to filter by (e.g., ['SOL-PERP', 'BTC-PERP'])"),
    from_date: str | None = Field(
        default=None, description="Optional earliest position date (YYYY-MM-DDTHH:MM:SSZ). Defaults to 2 days ago."),
    ctx: Context | None = None
) -> GetPositionsResponse:
    """Retrieve user positions across venues, with optional filters."""
    if ctx:
        await ctx.info(f"Fetching positions for {public_key}")
    params = {
        "public_key": public_key,
        "platforms": platforms,
        "symbols": symbols,
        "from": from_date,
    }
    # Filter out None values before sending
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/positions", params=params)
    return GetPositionsResponse(**response_data)


@data_mcp.tool(name="get_trade_history")
async def get_trade_history(
    public_key: str = Field(description="User's Solana wallet address"),
    platforms: list[Platform] | None = Field(
        default=None, description="Optional platforms filter"),
    symbols: list[str] | None = Field(
        default=None, description="Optional symbols filter"),
    start_time: str | None = Field(
        default=None, description="Optional start time (YYYY-MM-DDTHH:MM:SSZ). Defaults to 30 days ago."),
    end_time: str | None = Field(
        default=None, description="Optional end time (YYYY-MM-DDTHH:MM:SSZ). Defaults to now."),
    ctx: Context | None = None
) -> GetTradeHistoryResponse:
    """Retrieve user trade history across venues, with optional filters."""
    if ctx:
        await ctx.info(f"Fetching trade history for {public_key}")
    params = {
        "public_key": public_key,
        "platforms": platforms,
        "symbols": symbols,
        "start_time": start_time,
        "end_time": end_time,
    }
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/trade_history", params=params)
    return GetTradeHistoryResponse(**response_data)

# --- Liquidations Tools ---


@data_mcp.tool(name="get_latest_liquidations")
async def get_latest_liquidations(ctx: Context | None = None) -> list[Liquidation]:
    """Fetches the 10 most recent liquidation events."""
    if ctx:
        await ctx.info("Fetching latest liquidations")
    response_data = await _call_ranger_data_api("/v1/liquidations/latest")
    return [Liquidation(**item) for item in response_data]


@data_mcp.tool(name="get_liquidation_totals")
async def get_liquidation_totals(ctx: Context | None = None) -> LiquidationTotals:
    """Provides total USD value of liquidations over recent time intervals (1h, 4h, 12h, 24h)."""
    if ctx:
        await ctx.info("Fetching liquidation totals")
    response_data = await _call_ranger_data_api("/v1/liquidations/totals")
    return LiquidationTotals(**response_data)


@data_mcp.tool(name="get_liquidation_capitulation_signals")
async def get_liquidation_capitulation_signals(
    threshold: float | None = Field(
        default=2.0, ge=0, description="Z-score threshold to trigger a signal (default: 2.0)"),
    # Granularity seems less useful here based on docs, but keeping for completeness
    # granularity: Literal["15m", "30m", "1h", "4h", "1d"] | None = Field(default="1h", description="Time granularity for analysis"),
    ctx: Context | None = None
) -> list[CapitulationSignal]:
    """Identifies potential market capitulation events based on liquidation volume exceeding statistical norms (Z-score)."""
    if ctx:
        await ctx.info(f"Fetching liquidation capitulation signals (threshold: {threshold})")
    params = {"threshold": threshold}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/liquidations/capitulation", params=params)
    return [CapitulationSignal(**item) for item in response_data]


@data_mcp.tool(name="get_liquidation_heatmap")
async def get_liquidation_heatmap(
    granularity: Literal["15m", "30m", "1h", "4h", "1d"] | None = Field(
        default="1h", description="Time bucket size (default: 1h)"),
    ctx: Context | None = None
) -> list[LiquidationHeatmapEntry]:
    """Provides aggregated liquidation values (USD) bucketed by time granularity over the last 7 days."""
    if ctx:
        await ctx.info(f"Fetching liquidation heatmap (granularity: {granularity})")
    params = {"granularity": granularity}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/liquidations/heatmap", params=params)
    return [LiquidationHeatmapEntry(**item) for item in response_data]


@data_mcp.tool(name="get_largest_liquidations")
async def get_largest_liquidations(
    granularity: Literal["15m", "30m", "1h", "4h", "1d", "7d"] | None = Field(
        default="1d", description="Time window to look back (default: 1d)"),
    limit: int | None = Field(
        default=50, ge=1, description="Maximum number of liquidations to return (default: 50)"),
    ctx: Context | None = None
) -> list[LargestLiquidation]:
    """Retrieves the largest individual liquidation events within a specified time window."""
    if ctx:
        await ctx.info(f"Fetching largest liquidations (granularity: {granularity}, limit: {limit})")
    params = {"granularity": granularity, "limit": limit}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/liquidations/largest", params=params)
    return [LargestLiquidation(**item) for item in response_data]


# --- Funding & Borrow Rates Tools ---

@data_mcp.tool(name="get_funding_rate_arbs")
async def get_funding_rate_arbs(
    min_diff: float | None = Field(
        default=0.0001, ge=0, description="Minimum absolute rate difference (decimal, e.g., 0.0001 for 0.01%)"),
    ctx: Context | None = None
) -> list[FundingRateArb]:
    """Identifies potential funding rate arbitrage opportunities between platforms."""
    if ctx:
        await ctx.info(f"Fetching funding rate arbs (min_diff: {min_diff})")
    params = {"min_diff": min_diff}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/funding_rates/arbs", params=params)
    return [FundingRateArb(**item) for item in response_data]


@data_mcp.tool(name="get_accumulated_funding_rates")
async def get_accumulated_funding_rates(
    symbol: str | None = Field(
        default=None, description="Filter by market symbol (e.g., SOL-PERP)"),
    granularity: Literal["1h", "4h", "1d"] | None = Field(
        default=None, description="Time aggregation level"),
    platform: Platform | None = Field(
        default=None, description="Filter by platform"),
    ctx: Context | None = None
) -> list[AccumulatedRate]:
    """Retrieves historical accumulated funding rates."""
    if ctx:
        await ctx.info(f"Fetching accumulated funding rates ({symbol=}, {granularity=}, {platform=})")
    params = {"symbol": symbol,
              "granularity": granularity, "platform": platform}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/funding_rates/accumulated", params=params)
    return [AccumulatedRate(**item) for item in response_data]


@data_mcp.tool(name="get_accumulated_borrow_rates")
async def get_accumulated_borrow_rates(
    symbol: str | None = Field(
        default=None, description="Filter by asset symbol (e.g., USDC)"),
    granularity: Literal["1h", "4h", "1d"] | None = Field(
        default=None, description="Time aggregation level"),
    platform: Platform | None = Field(
        default=None, description="Filter by platform"),
    ctx: Context | None = None
) -> list[AccumulatedRate]:
    """Retrieves historical accumulated borrow rates."""
    if ctx:
        await ctx.info(f"Fetching accumulated borrow rates ({symbol=}, {granularity=}, {platform=})")
    params = {"symbol": symbol,
              "granularity": granularity, "platform": platform}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/borrow_rates/accumulated", params=params)
    # Re-use AccumulatedRate model as structure is the same
    return [AccumulatedRate(**item) for item in response_data]


@data_mcp.tool(name="get_extreme_funding_rates")
async def get_extreme_funding_rates(
    granularity: Literal["1h", "4h"] | None = Field(
        default="1h", description="Time aggregation level"),
    limit: int | None = Field(
        default=10, ge=1, description="Number of highest/lowest rates to return"),
    ctx: Context | None = None
) -> ExtremeFundingRates:
    """Fetches markets with the highest and lowest accumulated funding rates."""
    if ctx:
        await ctx.info(f"Fetching extreme funding rates ({granularity=}, {limit=})")
    params = {"granularity": granularity, "limit": limit}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/funding_rates/extreme", params=params)
    return ExtremeFundingRates(**response_data)


@data_mcp.tool(name="get_oi_weighted_funding_rates")
async def get_oi_weighted_funding_rates(ctx: Context | None = None) -> list[OiWeightedFundingRate]:
    """Provides the open interest-weighted average funding rate for each symbol across all platforms."""
    if ctx:
        await ctx.info("Fetching OI-weighted funding rates")
    response_data = await _call_ranger_data_api("/v1/funding_rates/oi_weighted")
    return [OiWeightedFundingRate(**item) for item in response_data]


@data_mcp.tool(name="get_funding_rate_trend")
async def get_funding_rate_trend(
    symbol: str = Field(
        description="Market symbol to analyze (e.g., SOL-PERP)"),
    platform: Platform | None = Field(
        default=None, description="Optional platform filter"),
    ctx: Context | None = None
) -> list[FundingRateTrend]:
    """Calculates the recent funding rate trend for a symbol (optionally by platform)."""
    if ctx:
        await ctx.info(f"Fetching funding rate trend for {symbol} on {platform or 'all platforms'}")
    params = {"symbol": symbol, "platform": platform}
    params = {k: v for k, v in params.items() if v is not None}
    response_data = await _call_ranger_data_api("/v1/funding_rates/trend", params=params)
    return [FundingRateTrend(**item) for item in response_data]
