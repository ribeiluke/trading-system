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
from shared.temporal.activities.service.trading_service import TradingService

class MarketService(TradingService):
    def place_market_order(
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
                type="MARKET",
                quantity=quantity,
                reduce_only="false" if is_enter else "true"
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
                    return self.place_market_order(
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
        take_profit_order_id: Optional[int],
        client: DerivativesTradingUsdsFutures
    ):
        """Run a single iteration of position management logic"""
        try:
            # Get current position
            position = self.get_position(client=client, symbol=symbol)
            if position is None:
                stop_order_status = self.get_algo_order_status(algo_id=algo_id, client=client)
                if stop_order_status in ["FINISHED", "EXPIRED", "REJECTED", "CANCELED"]:
                    if chat_id:
                        await send_telegram_message(chat_id, f"Position closed on {symbol}👀")
                    return ManagePositionIterationResult(
                            atr_value=atr_value,
                            take_profit_triggered=take_profit_triggered,
                            trailing_stop_price=trailing_stop_price,
                            take_profit_order_id=take_profit_order_id,
                            finished=True
                        )
                return ManagePositionIterationResult(
                        atr_value=atr_value,
                        take_profit_triggered=take_profit_triggered,
                        trailing_stop_price=trailing_stop_price,
                        take_profit_order_id=take_profit_order_id,
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
                    take_profit_order_id = self.place_market_order(
                        symbol=symbol,
                        side="SELL" if side == "BUY" else "BUY",
                        quantity=take_profit_size,
                        client=client,
                        is_enter=False,
                        quantity_decimals=quantity_decimals
                    )

                    if chat_id:
                        await send_telegram_message(chat_id, f"Take profit taken on {symbol}💰")
                        take_profit_triggered = True

            # Check trailing stop
            if self.check_trailing_stop_triggered(current_price, trailing_stop_price, side):
                position_size = position_size
                _ = self.place_market_order(
                    symbol=symbol,
                    side="SELL" if side == "BUY" else "BUY",
                    quantity=position_size,
                    client=client,
                    is_enter=False,
                    quantity_decimals=quantity_decimals
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
                take_profit_order_id=take_profit_order_id,
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
