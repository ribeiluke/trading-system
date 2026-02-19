from shared.config.auth import (
    get_futures_client, get_futures_testnet_client
)


def get_futures_usdt_balance(api_key: str, api_secret: str) -> float:
    """
    This function gets usdt balance in the futures market.
    """
    client = get_futures_client(api_key=api_key, api_secret=api_secret)
    account_balances = client.rest_api.futures_account_balance_v2()
    account_balances = account_balances.data()
    for account_balance in account_balances:
        if account_balance.asset == "USDT":
            return float(account_balance.balance)
    return 0.0


def get_testnet_futures_usdt_balance(api_key: str, api_secret: str) -> float:
    """
    This function gets usdt balance in the futures market.
    """
    client = get_futures_testnet_client(
        api_key=api_key, api_secret=api_secret
    )
    account_balances = client.rest_api.futures_account_balance_v2()
    account_balances = account_balances.data()
    for account_balance in account_balances:
        if account_balance.asset == "USDT":
            return float(account_balance.balance)
    return 0.0


def get_maximum_leverage(api_key: str, api_secret: str, symbol: str) -> int:
    """
    This function gets the current leverage for a given symbol.
    """
    client = get_futures_client(api_key=api_key, api_secret=api_secret)
    leverage_info = client.rest_api.notional_and_leverage_brackets(symbol=symbol)
    leverage_info = leverage_info.data().actual_instance
    if len(leverage_info) > 0:
        leverage_info = leverage_info[0].brackets
        for leverage in leverage_info:
            return leverage.initial_leverage
    return 10