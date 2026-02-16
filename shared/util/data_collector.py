import httpx
import logging
import pandas as pd

from binance_sdk_derivatives_trading_usds_futures.rest_api.models import (
    KlineCandlestickDataIntervalEnum,
)

from shared.config.auth import get_futures_unauthenticated_client


logging.basicConfig(level=logging.INFO)


def get_data(
    instrument="BTCUSDT",
    interval="1h",
    forMarketCondition=False,
    plain=True,
    limit=1500,
):
    url = (
        "https://api.binance.com/api/v3/klines?symbol="
        + instrument
        + "&interval="
        + interval
        + "&limit="
        + str(limit)
    )
    data = httpx.get(url).json()
    df = pd.DataFrame(
        data,
        columns=[
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ],
    )
    df_ohlc = df.iloc[:, 0:6]

    if plain:  # in case the user wants the data with no indicators
        return df_ohlc.astype("float64")
    

def get_candlestick_data(
    symbol: str, timeframe: str, limit: int = 1000, plain: bool = True
):
    try:
        client = get_futures_unauthenticated_client()
        response = client.rest_api.kline_candlestick_data(
            symbol=symbol,
            interval=KlineCandlestickDataIntervalEnum[f"INTERVAL_{timeframe}"].value,
            limit=limit
        )

        data = response.data()

        df = pd.DataFrame(
        data,
        columns=[
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
            ],
        )
        df_ohlc = df.iloc[:, 0:6]

        if plain:  # in case the user wants the data with no indicators
            return df_ohlc.astype("float64")
    except Exception as e:
        logging.error(f"get_candlestick_data() error: {e}")


def get_latest_bid(symbol: str) -> float:
    try:
        client = get_futures_unauthenticated_client()
        order_book = client.rest_api.order_book(symbol, 5)
        order_book = order_book.data()
        return float(order_book.bids[0].root[0])
    except Exception as e:
        logging.error(f"get_latest_bid() error: {e}")


def get_latest_ask(symbol: str) -> float:
    try:
        client = get_futures_unauthenticated_client()
        order_book = client.rest_api.order_book(symbol, 5)
        order_book = order_book.data()
        return float(order_book.asks[0].root[0])
    except Exception as e:
        logging.error(f"get_latest_ask() error: {e}")
