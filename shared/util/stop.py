from shared.config.settings import get_settings
from shared.util.data_collector import get_data
from shared.util.decimals import count_decimal_places_decimal
from shared.util.exchange_info import get_price_precision
from shared.util.indicator import ATR
settings = get_settings()

def get_current_atr_trailing_stop(
        symbol:str = settings.SYMBOL, 
        timeframe:str = settings.TIMEFRAME, 
        latest_market_price:float = 0.0, 
        latest_trail_price:float = 0.0, 
        atr_multiplier:float=settings.ATR_TRAILING_STOP_MUL,
        atr_value:float = 0.0,
        side: str = "BUY"
    ) -> float:

    if atr_value == 0.0:
        symbol = symbol.replace("/", "")
        data = get_data(instrument=symbol, interval=timeframe)
        data["ATR"] = ATR(DataFrame=data)
        atr_value = data["ATR"].values[-2]

    if latest_market_price == 0.0:
        latest_market_price = data["Close"].values[-1]

    if side == "BUY":
        current_atr_price = latest_market_price - (atr_value * atr_multiplier)
        return max(current_atr_price, latest_trail_price)
    else:
        current_atr_price = latest_market_price + (atr_value * atr_multiplier)
        return min(current_atr_price, latest_trail_price)


def calculate_stop_loss(
    side: str, symbol: str, current_price: float, atr_value: float, atr_multiplier: float
) -> float:
    if side == "BUY":
        stop_price = current_price - (atr_value * atr_multiplier)
    else:
        stop_price = current_price + (atr_value * atr_multiplier)

    price_precision = get_price_precision(symbol=symbol.replace("/", ""))
    number_of_decimals = count_decimal_places_decimal(price_precision)
    
    return round(stop_price, number_of_decimals)