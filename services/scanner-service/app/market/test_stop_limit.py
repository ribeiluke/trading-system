import os
import logging

from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures,
    ConfigurationRestAPI,
    DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)
from binance_sdk_derivatives_trading_usds_futures.rest_api.models import (
    NewOrderSideEnum,
    NewOrderTimeInForceEnum,
    NewAlgoOrderSideEnum,
    NewAlgoOrderPositionSideEnum,
    NewAlgoOrderTimeInForceEnum,
    NewAlgoOrderWorkingTypeEnum,
    NewAlgoOrderNewOrderRespTypeEnum,
)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create configuration for the REST API
configuration_rest_api = ConfigurationRestAPI(
    api_key=os.getenv("API_KEY", ""),
    api_secret=os.getenv("API_SECRET", ""),
    base_path=os.getenv(
        "BASE_PATH", DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
    ),
)

# Initialize DerivativesTradingUsdsFutures client
client = DerivativesTradingUsdsFutures(config_rest_api=configuration_rest_api)


def test_order():
    try:
        # order_book = client.rest_api.order_book(symbol="ETHUSDT", limit=5)
        # order_book = order_book.data()

        # response = client.rest_api.new_order(
        #     symbol="ETHUSDT",
        #     side=NewOrderSideEnum["BUY"].value,
        #     type="LIMIT",
        #     quantity=0.01,
        #     price=order_book.bids[-1].root[0],
        #     time_in_force=NewOrderTimeInForceEnum["GTC"].value,
        # )

        order_book = client.rest_api.order_book(symbol="ETHUSDT", limit=20)
        order_book = order_book.data()

        # data = response.data()
        # logging.info(f"test_order() response: {data}")

        response = client.rest_api.new_algo_order(
            algo_type="CONDITIONAL",
            symbol="ETHUSDT",
            side=NewAlgoOrderSideEnum.SELL,
            type="STOP",                     # STOP = stop-limit
            time_in_force=NewAlgoOrderTimeInForceEnum.GTC,
            quantity=0.01,
            price=order_book.bids[-1].root[0],                     # limit order price AFTER trigger
            trigger_price=order_book.bids[-10].root[0],             # stop price
            price_protect="TRUE",
            reduce_only="true",
            new_order_resp_type=NewAlgoOrderNewOrderRespTypeEnum.RESULT,
        )

        rate_limits = response.rate_limits
        logging.info(f"test_order() rate limits: {rate_limits}")

        data = response.data()
        logging.info(f"test_order() response: {data}")
    except Exception as e:
        logging.error(f"test_order() error: {e}")


if __name__ == "__main__":
    test_order()