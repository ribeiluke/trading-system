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

class LimitService:
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
        try:
            order = client.rest_api.new_order(
                symbol=symbol,
                side=NewOrderSideEnum[side].value,
                type="LIMIT",
                quantity=quantity,
                reduce_only="false" if is_enter else "true",
                price_match=NewOrderPriceMatchEnum["QUEUE"].value,
                time_in_force=(
                    NewOrderTimeInForceEnum["GTC"].value 
                    if is_enter 
                    else NewOrderTimeInForceEnum["GTC"].value
                ),
                good_till_date = (
                    None if is_enter
                    else int((datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp())
                )
            )
            return order.data().order_id
        except Exception as e:
            logging.error(f"new_order() error: {e}")

            msg = str(e)

            # ✅ retry timestamp problems
            if "-1111" in msg:
                logging.warning(
                    "Precision is over the maximum defined for this asset. Retrying..."
                )
                time.sleep(2)
                try:
                    return self.place_limit_order(
                        symbol,
                        side,
                        round(quantity, quantity_decimals-1),
                        client,
                        quantity_decimals,
                        is_enter
                    )
                except Exception as e:
                    logging.error(f"Retry failed: {e}")
                    raise
            raise

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
    
    def exit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        client: DerivativesTradingUsdsFutures,
        order_book_limit: int = 5
    ) -> int:
        try:
            order_book = client.rest_api.order_book(symbol, order_book_limit)
            order_book = order_book.data()
            price = (
                order_book.bids[2].root[0] if side == "SELL" else order_book.asks[2].root[0]
            )
            order = client.rest_api.new_order(
                symbol=symbol,
                side=NewOrderSideEnum[side].value,
                type="LIMIT",
                quantity=quantity,
                price=price,
                time_in_force=NewOrderTimeInForceEnum["GTC"].value,
            )
            return order.data().order_id
        except Exception as e:
            logging.error(f"new_order() error: {e}")
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
        deadline = datetime.now(timezone.utc) + timedelta(seconds=wait_time_seconds)

        while datetime.now(timezone.utc) < deadline:
            try:
                order = client.rest_api.query_order(
                    symbol=symbol,
                    order_id=order_id
                )

                status = order.data().get("status", "")
                if status == "FILLED":
                    return True

            except Exception as e:
                msg = str(e)

                # ✅ retry timestamp problems
                if "-1021" in msg:
                    logging.warning("Clock drift detected. Retrying...")
                    time.sleep(2)
                    continue

                # other errors → real failures
                logging.exception("query_order failed")
                raise

            time.sleep(5)

        logging.info("Order not filled within deadline")
        return False
    
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
    
    async def manage_position(
        self,
        user: str,
        symbol: str,
        side: str,
        stop_price: float,
        atr_value: float,
        atr_take_profit_mul: float,
        chat_id: int,
        leverage: int,
        algo_id: int,
        timeframe: str,
        atr_length: int,
        wait_time_seconds: int,
        quantity_decimals: int,
        client: DerivativesTradingUsdsFutures
    ):

        """Manages a single iteration of the position logic."""
        isDone = False
        trailing_stop_price = stop_price
        take_profit_triggered = False
        take_profit_order_id = None
        while not isDone:
            try:
                position = self.get_position(client=client, symbol=symbol)
                if position is None:
                    stop_order_status = self.get_algo_order_status(algo_id=algo_id, client=client)
                    if (
                        stop_order_status == "FINISHED" 
                        or stop_order_status == "EXPIRED"
                        or stop_order_status == "REJECTED"
                    ):
                        if chat_id:
                            await send_telegram_message(chat_id, f"Position closed on {symbol}👀")
                        isDone = True
                    continue
                current_price = float(position.mark_price)
                position_pnl = float(position.un_realized_profit)
                current_entry_price = float(position.entry_price)
                position_size = abs(float(position.position_amt))
                take_profit_price = self.get_take_profit_price(
                    entry_price=current_entry_price,
                    atr_value=atr_value,
                    atr_take_profit_mul=atr_take_profit_mul,
                    side=side
                )

                print("\n-----------------------------------")
                print("\tBot Update")
                print(f"Symbol: {position.symbol}")
                print(f"Current price: {current_price}")
                print(f"position size: {position_size}")
                print(f"Current Entry price: {current_entry_price}")
                print(f"Current profit: ${position_pnl}")
                print(f"Current trailing stop price: {trailing_stop_price}")
                print(f"Current take profit price: {take_profit_price}")
                print(f"User: {user}")

                # Log data to the database
                log_data = {
                    "symbol": position.symbol,
                    "position": "Long" if side == "BUY" else "Short",
                    "leverage": leverage,
                    "current_price": current_price,
                    "position_size": position_size,
                    "current_entry_price": current_entry_price,
                    "current_profit": position_pnl,
                    "trailing_stop_price": trailing_stop_price,
                    "take_profit_price": take_profit_price,
                    "user": user,
                    "timestamp": datetime.now(timezone.utc),
                }
                log_to_db(data=log_data)
                print("Log successfully sent to the database.")

                # Check take profit
                if self.check_take_profit_triggered(current_price, take_profit_price, side):
                    if not take_profit_triggered:
                        take_profit_size = round((position_size / 2), quantity_decimals)
                        take_profit_order_id = self.place_limit_order(
                            symbol=symbol,
                            side="SELL" if side == "BUY" else "BUY",
                            quantity=take_profit_size,
                            client=client,
                            is_enter=False
                        )
                        is_filled = self.check_limit_order_filled(
                            symbol=symbol,
                            order_id=take_profit_order_id,
                            client=client,
                            wait_time_seconds=30
                        )

                        if chat_id and is_filled:
                            await send_telegram_message(chat_id, f"Take profit taken on {symbol}💰")
                            take_profit_triggered = True
                        
                        if not is_filled:
                            logging.warning(
                                f"Take profit order {take_profit_order_id} not filled within deadline."
                            )
                            self.cancel_order_for_manage_position(
                                symbol=symbol, order_id=take_profit_order_id, client=client
                            )

                # Check trailing stop
                if self.check_trailing_stop_triggered(current_price, trailing_stop_price, side):
                    position_size = position_size
                    _ = self.place_limit_order(
                        symbol=symbol,
                        side="SELL" if side == "BUY" else "BUY",
                        quantity=position_size,
                        client=client,
                        is_enter=False
                    )

                else:
                    atr_value = get_latest_atr(
                        instrument=symbol,
                        timeframe=timeframe,
                        atr_length=atr_length,
                    )
                    trailing_stop_price = get_current_atr_trailing_stop(
                        symbol=symbol,
                        atr_multiplier=atr_take_profit_mul,
                        latest_market_price=current_price,
                        latest_trail_price=trailing_stop_price,
                        atr_value=atr_value,
                        side=side,
                        timeframe=timeframe,
                    )
                
                time.sleep(wait_time_seconds)
            except Exception as e:
                logging.critical(f"Fatal error in manage_position loop: {e}")
                traceback.print_exc()
    
    async def manage_position_iteration(
        self,
        user: str,
        symbol: str,
        side: str,
        stop_price: float,
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
        """Run a single iteration of position management logic"""
        try:
            # Get current position
            position = self.get_position(client=client, symbol=symbol)
            if position is None:
                stop_order_status = self.get_algo_order_status(algo_id=algo_id, client=client)
                if stop_order_status in ["FINISHED", "EXPIRED", "REJECTED"]:
                    if chat_id:
                        await send_telegram_message(chat_id, f"Position closed on {symbol}👀")
                    return ManagePositionIterationResult(
                            atr_value=atr_value,
                            take_profit_triggered=take_profit_triggered,
                            trailing_stop_price=trailing_stop_price,
                            finished=True
                        )
                return ManagePositionIterationResult(
                        atr_value=atr_value,
                        take_profit_triggered=take_profit_triggered,
                        trailing_stop_price=trailing_stop_price,
                        finished=False
                    )

            current_price = float(position.mark_price)
            position_pnl = float(position.un_realized_profit)
            current_entry_price = float(position.entry_price)
            position_size = abs(float(position.position_amt))
            take_profit_price = self.get_take_profit_price(
                entry_price=current_entry_price,
                atr_value=atr_value,
                atr_take_profit_mul=atr_take_profit_mul,
                side=side
            )

            # Log to DB
            log_data = {
                "symbol": position.symbol,
                "position": "Long" if side == "BUY" else "Short",
                "leverage": leverage,
                "current_price": current_price,
                "position_size": position_size,
                "current_entry_price": current_entry_price,
                "current_profit": position_pnl,
                "trailing_stop_price": trailing_stop_price,
                "take_profit_price": take_profit_price,
                "user": user,
                "timestamp": datetime.now(timezone.utc),
            }
            log_to_db(data=log_data)

            # Check take profit
            if self.check_take_profit_triggered(current_price, take_profit_price, side):
                if not take_profit_triggered:
                    take_profit_size = round((position_size / 2), quantity_decimals)
                    take_profit_order_id = self.place_limit_order(
                        symbol=symbol,
                        side="SELL" if side == "BUY" else "BUY",
                        quantity=take_profit_size,
                        client=client,
                        is_enter=False
                    )
                    is_filled = self.check_limit_order_filled(
                        symbol=symbol,
                        order_id=take_profit_order_id,
                        client=client,
                        wait_time_seconds=30
                    )

                    if chat_id and is_filled:
                        await send_telegram_message(chat_id, f"Take profit taken on {symbol}💰")
                        take_profit_triggered = True
                    
                    if not is_filled:
                        logging.warning(
                            f"Take profit order {take_profit_order_id} not filled within deadline."
                        )
                        self.cancel_order_for_manage_position(
                            symbol=symbol, order_id=take_profit_order_id, client=client
                        )

            # Check trailing stop
            if self.check_trailing_stop_triggered(current_price, trailing_stop_price, side):
                position_size = position_size
                _ = self.place_limit_order(
                    symbol=symbol,
                    side="SELL" if side == "BUY" else "BUY",
                    quantity=position_size,
                    client=client,
                    is_enter=False
                )
            else:
                atr_value = get_latest_atr(
                    instrument=symbol,
                    timeframe=timeframe,
                    atr_length=atr_length,
                )
                trailing_stop_price = get_current_atr_trailing_stop(
                    symbol=symbol,
                    atr_multiplier=atr_take_profit_mul,
                    latest_market_price=current_price,
                    latest_trail_price=trailing_stop_price,
                    atr_value=atr_value,
                    side=side,
                    timeframe=timeframe,
                )

            return ManagePositionIterationResult(
                atr_value=atr_value,
                take_profit_triggered=take_profit_triggered,
                trailing_stop_price=trailing_stop_price,
                finished=False
            )

        except Exception as e:
            logging.critical(f"Error in manage_position_iteration: {e}")
            traceback.print_exc()
            return ManagePositionIterationResult(
                atr_value=atr_value,
                take_profit_triggered=take_profit_triggered,
                trailing_stop_price=trailing_stop_price,
                finished=False
            )
