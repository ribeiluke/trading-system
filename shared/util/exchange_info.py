from shared.config.auth import get_futures_unauthenticated_client

def get_minimum_notional(symbol: str) -> float:
    client = get_futures_unauthenticated_client()
    exchange_info = client.rest_api.exchange_information()
    symbols_info = exchange_info.data().symbols
    for symbol_info in symbols_info:
        if symbol_info.symbol == symbol:
            for filter in symbol_info.filters:
                if filter.filter_type == "MIN_NOTIONAL":
                    return float(filter.notional)
    
    return 0.0


def get_price_precision(symbol: str) -> float:
    client = get_futures_unauthenticated_client()
    exchange_info = client.rest_api.exchange_information()
    symbols_info = exchange_info.data().symbols
    for symbol_info in symbols_info:
        if symbol_info.symbol == symbol:
            for filter in symbol_info.filters:
                if filter.filter_type == "PRICE_FILTER":
                    return float(filter.tick_size)
    
    return 0.0


def get_quantity_precision(symbol: str) -> float:
    client = get_futures_unauthenticated_client()
    exchange_info = client.rest_api.exchange_information()
    symbols_info = exchange_info.data().symbols
    for symbol_info in symbols_info:
        if symbol_info.symbol == symbol:
            for filter in symbol_info.filters:
                if filter.filter_type == "LOT_SIZE":
                    return float(filter.step_size)
    
    return 0.0