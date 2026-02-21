import logging
import time
import traceback
from datetime import datetime, timezone, timedelta
from typing import Optional
from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures
)
from binance_sdk_derivatives_trading_usds_futures.rest_api.models import (
    NewAlgoOrderNewOrderRespTypeEnum,
    NewOrderSideEnum,
    NewOrderPriceMatchEnum,
    NewOrderTimeInForceEnum,
    OrderBookResponse,
    PositionInformationV3Response
)
from fastapi import params

from shared.database.mongo import log_to_db
from shared.models.trade_plan import ManagePositionIterationResult
from shared.util.atr import get_latest_atr
from shared.util.stop import get_current_atr_trailing_stop
from shared.util.telegram import send_telegram_message

class TradingService:
    def set_leverage(
        self, symbol: str, leverage: int, client: DerivativesTradingUsdsFutures
    ) -> int:
        try:
            response = client.rest_api.change_initial_leverage(
                symbol=symbol, leverage=leverage
            )
            logging.info(f"Leverage set response: {response}")
            return response.data().leverage
        except Exception as e:
            logging.error(f"set_leverage() error: {e}")
            raise

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        client: DerivativesTradingUsdsFutures,
        quantity_decimals: int,
        is_enter: bool = True
    ) -> int:
        pass

    def select_price_from_order_book(
        self, 
        symbol: str,
        side: str,
        client: DerivativesTradingUsdsFutures,
        order_book_limit: int = 5,
        is_enter: bool = True
    ) -> float:
        try:
            order_book = client.rest_api.order_book(symbol, order_book_limit)
            order_book = order_book.data()
            if is_enter:
                price = (
                    order_book.bids[-1].root[0] if side == "BUY" else order_book.asks[-1].root[0]
                )
            else:
                price = (
                    order_book.bids[2].root[0] if side == "SELL" else order_book.asks[2].root[0]
                )
            return price
        except Exception as e:
            logging.error(f"select_price_from_order_book() error: {e}")
            raise
    
    def cancel_order(
        self, symbol: str, order_id: int, client: DerivativesTradingUsdsFutures
    ) -> str:
        try:
            logging.info(f"Cancelling order with ID: {order_id}")
            response = client.rest_api.cancel_order(
                symbol=symbol,
                order_id=order_id
            )
            logging.info(f"Cancel order response: {response}")
            return response.data().status
        except Exception as e:
            logging.error(f"cancel_order() error: {e}")
            raise

    def cancel_order_for_manage_position(
        self, symbol: str, order_id: int, client: DerivativesTradingUsdsFutures
    ) -> str:
        num_retries = 5
        while num_retries > 0:
            try:
                status = self.cancel_order(symbol=symbol, order_id=order_id, client=client)
                if status == "CANCELED":
                    logging.info(f"Order {order_id} successfully canceled.")
                    return status
            except Exception as e:
                num_retries -= 1
                logging.warning(f"Failed to cancel order {order_id}, retries left: {num_retries}")
                time.sleep(2)
    
    def cancel_all_orders_for_symbol(
        self, symbol: str, client: DerivativesTradingUsdsFutures
    ):
        try:
            open_orders = client.rest_api.cancel_all_open_orders(symbol=symbol).data()
            logging.info(f"Cancelled orders: {open_orders}")
        except Exception as e:
            logging.error(f"cancel_all_orders_for_symbol() error: {e}")
            raise
    
    def check_limit_order_filled(
        self,
        symbol: str,
        order_id: int,
        client: DerivativesTradingUsdsFutures,
        wait_time_seconds: int = 1,
    ) -> bool:
        pass
    
    def get_algo_order_status(
        self, algo_id: str, client: DerivativesTradingUsdsFutures
    ) -> str:
        try:
            order_status = client.rest_api.query_algo_order(
                algo_id=algo_id
            ).data()
            return order_status.algo_status #NEW, EXPIRED, FINISHED or REJECTED
        except Exception as e:
            logging.error(f"get_algo_order_status() error: {e}")
            raise

    def stop_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        stop_price: float,
        client: DerivativesTradingUsdsFutures
    ) -> int:
        try:
            stop_side = "SELL" if side == "BUY" else "BUY"
            order = client.rest_api.new_algo_order(
                algo_type="CONDITIONAL",
                symbol=symbol,
                side=NewOrderSideEnum[stop_side].value,
                type="STOP_MARKET",
                quantity=quantity,
                trigger_price=stop_price,
                price_protect="TRUE",
                close_position="true",
                time_in_force=NewOrderTimeInForceEnum["GTC"].value,
                new_order_resp_type=NewAlgoOrderNewOrderRespTypeEnum.RESULT,
            )
            return order.data().algo_id
        except Exception as e:
            logging.error(f"stop_order() error: {e}")
            raise
    
    def stop_order_limit(
        self,
        symbol: str,
        side: str,
        quantity: float,
        stop_price: float,
        client: DerivativesTradingUsdsFutures
    ) -> int:
        try:
            stop_side = "SELL" if side == "BUY" else "BUY"
            order = client.rest_api.new_algo_order(
                algo_type="CONDITIONAL",
                symbol=symbol,
                side=NewOrderSideEnum[stop_side].value,
                type="STOP",
                quantity=quantity,
                price=stop_price,
                trigger_price=stop_price,
                price_protect="TRUE",
                reduce_only="true",
                time_in_force=NewOrderTimeInForceEnum["GTC"].value,
                new_order_resp_type=NewAlgoOrderNewOrderRespTypeEnum.RESULT,
            )
            return order.data().algo_id
        except Exception as e:
            logging.error(f"stop_order() error: {e}")
            raise

    def get_position(
            self, client: DerivativesTradingUsdsFutures, symbol: str
        ) -> Optional[PositionInformationV3Response]:
        open_positions = client.rest_api.position_information_v3(symbol=symbol).data()
        return open_positions[0] if open_positions else None
    
    def get_take_profit_price(
        self, entry_price: float, atr_value: float, atr_take_profit_mul: float, side: str
    ) -> float:
        if side == "BUY":
            return entry_price + (atr_take_profit_mul * atr_value)
        else:
            return entry_price - (atr_take_profit_mul * atr_value)
    
    def check_take_profit_triggered(
        self, current_price: float, take_profit_price: float, side: str
    ) -> bool:
        if side == "BUY":
            return current_price >= take_profit_price
        else:
            return current_price <= take_profit_price
    
    def check_trailing_stop_triggered(
        self, current_price: float, trailing_stop_price: float, side: str
    ) -> bool:
        if side == "BUY":
            return current_price <= trailing_stop_price
        else:
            return current_price >= trailing_stop_price
    
    async def manage_position_iteration(
        self,
        user: str,
        symbol: str,
        side: str,
        atr_value: float,
        atr_take_profit_mul: float,
        chat_id: int,
        leverage: int,
        algo_id: int,
        timeframe: str,
        atr_length: int,
        quantity_decimals: int,
        trailing_stop_price: float,
        take_profit_triggered: bool,
        client: DerivativesTradingUsdsFutures
    ):
        pass
