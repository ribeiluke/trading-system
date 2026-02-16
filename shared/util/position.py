from shared.config.auth import get_futures_client
from shared.util.account import get_futures_usdt_balance
from shared.util.decimals import count_decimal_places_decimal
from shared.util.exchange_info import get_minimum_notional, get_quantity_precision


def calculate_position_size(
    api_key: str,
    api_secret: str,
    symbol: str,
    current_price: float,
    stop_price: float,
    risk: float
) -> tuple[float, int]:
    balance = get_futures_usdt_balance(api_key=api_key, api_secret=api_secret)

    max_loss= balance * risk

    min_notional = get_minimum_notional(symbol=symbol)
    quantity_precision = get_quantity_precision(symbol=symbol)
    number_of_decimals = count_decimal_places_decimal(quantity_precision)


    adjusted_risk_per_unit = abs(current_price - stop_price)

    if adjusted_risk_per_unit == 0:
        return 0.0

    position_size = max_loss / adjusted_risk_per_unit

    notional = current_price * position_size

    if notional < min_notional:
        position_size = (min_notional + 1) / current_price

    return round(position_size, number_of_decimals), number_of_decimals


def check_open_positions(api_key: str, api_secret: str, symbol: str) -> bool:
    client = get_futures_client(api_key=api_key, api_secret=api_secret)
    open_positions = client.rest_api.position_information_v2(symbol=symbol).data()
    for position in open_positions:
        if position.entry_price != "0.0":
            return True
    return False


def check_open_orders(api_key: str, api_secret: str, symbol: str) -> bool:
    client = get_futures_client(api_key=api_key, api_secret=api_secret)
    open_orders = client.rest_api.current_all_open_orders(symbol=symbol).data()
    return len(open_orders) > 0


def check_algo_open_orders(api_key: str, api_secret: str, symbol: str) -> bool:
    client = get_futures_client(api_key=api_key, api_secret=api_secret)
    open_orders = client.rest_api.current_all_algo_open_orders(symbol=symbol).data()
    return len(open_orders) > 0


def is_this_symbol_being_traded(api_key: str, api_secret: str, symbol: str) -> bool:
    if (check_open_positions(api_key, api_secret, symbol) or 
        check_open_orders(api_key, api_secret, symbol) or 
        check_algo_open_orders(api_key, api_secret, symbol)
    ):
        return True
    return False