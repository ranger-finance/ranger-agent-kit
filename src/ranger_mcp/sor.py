@sor_mcp.resource("sor://sample_resource")
async def sample_sor_resource():
    """A sample resource for demonstration purposes."""
    return {"resource": "sample_sor_resource", "description": "This is a sample resource for sor_mcp."}

@sor_mcp.resource("sor://get_trade_quote")
async def resource_get_trade_quote():
    return {"resource": "get_trade_quote", "description": "Get a quote for a potential trade, including price, liquidity, and routing."}

@sor_mcp.resource("sor://increase_position")
async def resource_increase_position():
    return {"resource": "increase_position", "description": "Open a new position or increase the size of an existing one."}

@sor_mcp.resource("sor://decrease_position")
async def resource_decrease_position():
    return {"resource": "decrease_position", "description": "Decrease the size of an existing position using a specific venue."}

@sor_mcp.resource("sor://close_position")
async def resource_close_position():
    return {"resource": "close_position", "description": "Close an existing position completely, potentially specifying a venue or closing all."}

@sor_mcp.resource("sor://withdraw_balance_drift")
async def resource_withdraw_balance_drift():
    return {"resource": "withdraw_balance_drift", "description": "Withdraw available balance from a Drift sub-account."} 