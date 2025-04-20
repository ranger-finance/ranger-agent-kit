from typing import Annotated, Any, Literal
from pydantic import BaseModel, Field

# --- SOR Models ---

TradingSide = Literal["Long", "Short"]
SizeDenomination = Literal["SOL", "BTC", "ETH"]  # Add others as needed
CollateralDenomination = Literal["USDC"]
AdjustmentTypeIncrease = Literal["Increase"]
AdjustmentTypeDecrease = Literal["DecreaseFlash",
                                 "DecreaseJupiter", "DecreaseDrift", "DecreaseAdrena"]
AdjustmentTypeClose = Literal["CloseFlash",
                              "CloseJupiter", "CloseDrift", "CloseAdrena", "CloseAll"]
AdjustmentTypeCollateral = Literal["DepositCollateralFlash", "DepositCollateralJupiter",
                                   "DepositCollateralDrift", "WithdrawCollateralFlash", "WithdrawCollateralJupiter", "WithdrawCollateralDrift"]
# Currently only Drift supported by API
AdjustmentTypeWithdraw = Literal["WithdrawBalanceDrift"]


class QuoteParams(BaseModel):
    fee_payer: str = Field(
        description="The public key of the fee payer account")
    symbol: SizeDenomination
    side: TradingSide
    size: float = Field(
        gt=0, description="The size of the position in base asset")
    collateral: float = Field(
        gt=0, description="The amount of collateral to use (in USDC)")
    size_denomination: SizeDenomination
    collateral_denomination: CollateralDenomination = "USDC"
    adjustment_type: AdjustmentTypeIncrease | AdjustmentTypeDecrease | AdjustmentTypeClose
    target_venues: list[Literal["Jupiter", "Flash", "Drift"]] | None = Field(
        default=None, description="Optional list of target venues")
    slippage_bps: int | None = Field(
        default=None, ge=0, description="Slippage tolerance in basis points (e.g., 100 for 1%)")
    priority_fee_micro_lamports: int | None = Field(
        default=None, ge=0, description="Priority fee in micro lamports")


class IncreasePositionParams(QuoteParams):
    adjustment_type: AdjustmentTypeIncrease = "Increase"
    expected_price: float | None = Field(
        default=None, description="Optional expected price for the trade, in USD.")


class DecreasePositionParams(BaseModel):
    fee_payer: str = Field(
        description="The public key of the fee payer account")
    symbol: SizeDenomination
    side: TradingSide
    size: float = Field(
        gt=0, description="The size to decrease by in base asset")
    collateral: float = Field(
        ge=0, description="The amount of collateral to withdraw (in USDC)")
    size_denomination: SizeDenomination
    collateral_denomination: CollateralDenomination = "USDC"
    adjustment_type: AdjustmentTypeDecrease
    target_venues: list[Literal["Jupiter", "Flash", "Drift"]] | None = Field(
        default=None, description="Optional list of target venues")
    slippage_bps: int | None = Field(
        default=None, ge=0, description="Slippage tolerance in basis points (e.g., 100 for 1%)")
    priority_fee_micro_lamports: int | None = Field(
        default=None, ge=0, description="Priority fee in micro lamports")
    expected_price: float | None = Field(
        default=None, description="Optional expected price for the trade, in USD.")


class ClosePositionParams(BaseModel):
    fee_payer: str = Field(
        description="The public key of the fee payer account")
    symbol: SizeDenomination
    side: TradingSide
    adjustment_type: AdjustmentTypeClose
    slippage_bps: int | None = Field(
        default=None, ge=0, description="Slippage tolerance in basis points (e.g., 100 for 1%)")
    priority_fee_micro_lamports: int | None = Field(
        default=None, ge=0, description="Priority fee in micro lamports")
    expected_price: float | None = Field(
        default=None, description="Optional expected price for the trade, in USD.")


class WithdrawBalanceParams(BaseModel):
    fee_payer: str = Field(
        description="The public key of the fee payer account")
    symbol: str = Field(
        description="The token symbol to withdraw (e.g., USDC)")
    amount: float = Field(gt=0, description="The amount to withdraw")
    sub_account_id: int | None = Field(
        default=0, description="The sub-account ID to withdraw from (Drift specific, defaults to 0)")
    adjustment_type: AdjustmentTypeWithdraw = "WithdrawBalanceDrift"


class FeeBreakdown(BaseModel):
    # Note: Field name mismatch in example (base_fee vs base_fee_per_unit)
    base_fee: float | None = None
    base_fee_per_unit: float | None = None
    spread_fee: float | None = None
    volatility_fee: float | None = None
    margin_fee: float | None = None
    close_fee: float | None = None
    open_fee: float | None = None
    other_fees: float | None = None


class QuoteDetails(BaseModel):
    base: float
    total_fee_per_unit: float | None = None  # Not always present
    fee: float | None = None  # Present in Jupiter quote example
    total: float
    fee_breakdown: FeeBreakdown


class VenueAllocation(BaseModel):
    venue_name: str
    collateral: float
    size: float
    quote: QuoteDetails
    price: float | None = None  # Only present in increase_position response example
    order_available_liquidity: float
    venue_available_liquidity: float


class QuoteResponse(BaseModel):
    venues: list[VenueAllocation]
    total_collateral: float
    total_size: float
    average_price: float


class SorApiResponse(BaseModel):
    message: str  # Base64 encoded transaction message for increase/decrease/close
    meta: QuoteResponse
    average_price: float | None = None  # Present in increase/decrease/close
    size: float | None = None  # Present in increase/decrease/close

# --- Data Models ---


Platform = str  # Allow any string for platform to support new protocols


class Position(BaseModel):
    id: str
    symbol: str
    side: TradingSide
    quantity: float
    entry_price: float
    liquidation_price: float | None = None  # Seems optional in some cases
    position_leverage: float
    real_collateral: float
    borrow_fee: float
    funding_fee: float
    open_fee: float
    close_fee: float
    created_at: str  # Using str for simplicity, could use datetime
    opened_at: str
    platform: str  # Changed from Platform to str


class GetPositionsResponse(BaseModel):
    positions: list[Position]


class Trade(BaseModel):
    id: str
    symbol: str
    side: TradingSide
    quantity: float
    entry_price: float
    fill_price: float
    position_leverage: float
    realized_pnl: float
    fees_paid: float
    order_type: str
    order_action: str
    is_closed: bool
    created_at: str
    opened_at: str
    platform: str  # Changed from Platform to str
    tx_signature: str


class GetTradeHistoryResponse(BaseModel):
    trades: list[Trade]


class Liquidation(BaseModel):
    id: str
    market_id: str
    user_account: str
    liquidator: str
    platform: str  # Changed from Platform to str
    quantity: float
    price: float
    created_at: str
    liquidator_reward: float
    insurance_fund_fee: float


class LiquidationTotals(BaseModel):
    last_1h: float
    last_4h: float
    last_12h: float
    last_24h: float


class CapitulationSignal(BaseModel):
    symbol: str
    platform: str  # Changed from Platform to str
    z_score: float
    total_liquidated: float
    mean_liquidation: float
    std_dev: float


class LiquidationHeatmapEntry(BaseModel):
    symbol: str
    platform: str  # Changed from Platform to str
    start: str  # Timestamp string
    total_liquidated_usd: float


class LargestLiquidation(BaseModel):
    symbol: str
    platform: str  # Changed from Platform to str
    timestamp: str
    quantity: float
    price: float
    value_usd: float
    liquidator_reward: float


class FundingRateArb(BaseModel):
    symbol: str
    platform_a: str  # Changed from Platform to str
    rate_a: float
    platform_b: str  # Changed from Platform to str
    rate_b: float
    rate_diff: str  # Representing Decimal


class AccumulatedRate(BaseModel):
    platform: str  # Changed from Platform to str
    symbol: str
    created_at: str
    accumulated_rate: str  # Decimal string
    base_granularity: str


class ExtremeFundingRates(BaseModel):
    highest: list[AccumulatedRate]
    lowest: list[AccumulatedRate]


class OiWeightedFundingRate(BaseModel):
    symbol: str
    funding_rate_updated_at: str
    open_interest_updated_at: str
    oi_weighted_funding_rate: str  # Decimal string


class FundingRateTrend(BaseModel):
    symbol: str
    platform: str  # Changed from Platform to str
    mean: float
    std_dev: float
    z_score: float
    trend: Literal["flat", "upward", "downward"]
    latest: float
