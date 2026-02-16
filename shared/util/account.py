from shared.config.auth import get_futures_client


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