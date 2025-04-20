@data_mcp.resource("data://sample_resource")
async def sample_data_resource():
    """A sample resource for demonstration purposes."""
    return {"resource": "sample_data_resource", "description": "This is a sample resource for data_mcp."}

@data_mcp.resource("data://get_positions")
async def resource_get_positions():
    return {"resource": "get_positions", "description": "Retrieve user positions across venues, with optional filters."}

@data_mcp.resource("data://get_trade_history")
async def resource_get_trade_history():
    return {"resource": "get_trade_history", "description": "Retrieve user trade history across venues, with optional filters."}

@data_mcp.resource("data://get_latest_liquidations")
async def resource_get_latest_liquidations():
    return {"resource": "get_latest_liquidations", "description": "Fetches the 10 most recent liquidation events."}

@data_mcp.resource("data://get_liquidation_totals")
async def resource_get_liquidation_totals():
    return {"resource": "get_liquidation_totals", "description": "Provides total USD value of liquidations over recent time intervals (1h, 4h, 12h, 24h)."}

@data_mcp.resource("data://get_liquidation_capitulation_signals")
async def resource_get_liquidation_capitulation_signals():
    return {"resource": "get_liquidation_capitulation_signals", "description": "Identifies potential market capitulation events based on liquidation volume exceeding statistical norms (Z-score)."}

@data_mcp.resource("data://get_liquidation_heatmap")
async def resource_get_liquidation_heatmap():
    return {"resource": "get_liquidation_heatmap", "description": "Provides aggregated liquidation values (USD) bucketed by time granularity over the last 7 days."}

@data_mcp.resource("data://get_largest_liquidations")
async def resource_get_largest_liquidations():
    return {"resource": "get_largest_liquidations", "description": "Retrieves the largest individual liquidation events within a specified time window."}

@data_mcp.resource("data://get_funding_rate_arbs")
async def resource_get_funding_rate_arbs():
    return {"resource": "get_funding_rate_arbs", "description": "Identifies potential funding rate arbitrage opportunities between platforms."}

@data_mcp.resource("data://get_accumulated_funding_rates")
async def resource_get_accumulated_funding_rates():
    return {"resource": "get_accumulated_funding_rates", "description": "Retrieves historical accumulated funding rates."}

@data_mcp.resource("data://get_accumulated_borrow_rates")
async def resource_get_accumulated_borrow_rates():
    return {"resource": "get_accumulated_borrow_rates", "description": "Retrieves historical accumulated borrow rates."}

@data_mcp.resource("data://get_extreme_funding_rates")
async def resource_get_extreme_funding_rates():
    return {"resource": "get_extreme_funding_rates", "description": "Fetches markets with the highest and lowest accumulated funding rates."}

@data_mcp.resource("data://get_oi_weighted_funding_rates")
async def resource_get_oi_weighted_funding_rates():
    return {"resource": "get_oi_weighted_funding_rates", "description": "Provides the open interest-weighted average funding rate for each symbol across all platforms."}

@data_mcp.resource("data://get_funding_rate_trend")
async def resource_get_funding_rate_trend():
    return {"resource": "get_funding_rate_trend", "description": "Calculates the recent funding rate trend for a symbol (optionally by platform)."} 