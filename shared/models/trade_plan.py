# placeholder shared model
from dataclasses import dataclass

LIMIT_TRADING_TASK_QUEUE_NAME = "LIMIT_TRADING_TASK_QUEUE"

@dataclass
class TradeParams:
    api_key: str
    api_secret: str
    user: str
    symbol: str
    side: str
    quantity: float
    stop_price: float
    atr_value: float
    timeframe: str
    atr_length: int
    user_email: str
    chat_id: int
    split_equally: bool
    num_levels: int
    atr_trailing_stop_mul: float
    atr_take_profit_mul: float
    wait_time_seconds: int
    strategy_name: str
    risk_per_trade: float = 0.02
    leverage: int = 10
    quantity_decimals: int = 2


@dataclass
class OrderParams:
    trade_params: TradeParams
    order_id: int

@dataclass
class ManagePositionParams(OrderParams):
    algo_id: int