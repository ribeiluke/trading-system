import os

from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures,
    ConfigurationRestAPI,
    DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)


def get_futures_client(api_key: str, api_secret: str) -> DerivativesTradingUsdsFutures:
    # Create configuration for the REST API
    configuration_rest_api = ConfigurationRestAPI(
        api_key=api_key,
        api_secret=api_secret,
        base_path=DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
    )

    # Initialize DerivativesTradingUsdsFutures client
    client = DerivativesTradingUsdsFutures(config_rest_api=configuration_rest_api)
    return client


def get_futures_unauthenticated_client() -> DerivativesTradingUsdsFutures:
    configuration_rest_api = ConfigurationRestAPI(
    api_key=os.getenv("API_KEY", ""),
    api_secret=os.getenv("API_SECRET", ""),
    base_path=os.getenv(
        "BASE_PATH", DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
    ),
    )

    # Initialize DerivativesTradingUsdsFutures client
    client = DerivativesTradingUsdsFutures(config_rest_api=configuration_rest_api)
    return client