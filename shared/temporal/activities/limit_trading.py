import asyncio

from temporalio import activity

from .service.limit_service import LimitService
from shared.config.auth import get_futures_client
from shared.models.trade_plan import (
    ManagePositionIterationParams,
    ManagePositionParams,
    ManagePositionIterationResult,
    OrderParams,
    TradeParams
)
from shared.util.telegram import send_telegram_message

class TradingLimitActivities:
    def __init__(self):
        self.trading_service = LimitService()

    @activity.defn
    async def set_leverage(
        self, trade_params: TradeParams
    ) -> int:
        try:
            client = get_futures_client(trade_params.api_key, trade_params.api_secret)
            leverage = await asyncio.to_thread(
                self.trading_service.set_leverage,
                symbol=trade_params.symbol,
                leverage=trade_params.leverage,
                client=client
            )
            return leverage
        except Exception as e:
            activity.logger.exception(
                f"new_order() error: {e}"
            )
            raise

    @activity.defn
    async def enter_limit(
        self, trade_params: TradeParams
    ) -> int:
        try:
            client = get_futures_client(trade_params.api_key, trade_params.api_secret)
            order_id = await asyncio.to_thread(
                self.trading_service.place_limit_order,
                symbol=trade_params.symbol,
                side=trade_params.side,
                quantity=trade_params.quantity,
                quantity_decimals=trade_params.quantity_decimals,
                client=client
            )
            return order_id
        except Exception as e:
            activity.logger.exception(
                f"new_order() error: {e}"
            )
            raise

    @activity.defn
    async def is_order_filled(self, order_params:OrderParams) -> bool:
        try:
            client = get_futures_client(
                order_params.trade_params.api_key, order_params.trade_params.api_secret
            )
            is_filled = await asyncio.to_thread(
                self.trading_service.check_limit_order_filled,
                symbol=order_params.trade_params.symbol,
                order_id=order_params.order_id,
                client=client
            )

            if is_filled:
                message = (
                    f"New position started on {order_params.trade_params.symbol} " +
                    ("🚀" if order_params.trade_params.side == "BUY" else "☄️")
                )
                await send_telegram_message(
                    chat_id=order_params.trade_params.chat_id,
                    message=message
                )
            return is_filled
        except Exception as e:
            activity.logger.exception(
                f"check_limit_order_filled() error: {e}"
            )
            raise
    
    @activity.defn
    async def cancel_limit(self, order_params: OrderParams) -> str:
        try:
            client = get_futures_client(
                order_params.trade_params.api_key, order_params.trade_params.api_secret
            )
            status =  await asyncio.to_thread(
                self.trading_service.cancel_order,
                symbol=order_params.trade_params.symbol,
                order_id=order_params.order_id,
                client=client
            )
            return status
        except Exception as e:
            activity.logger.exception(
                f"cancel_order() error: {e}"
            )
            raise e
    
    @activity.defn
    async def place_stop_order(self, trade_params: TradeParams) -> int:
        try:
            client = get_futures_client(trade_params.api_key, trade_params.api_secret)
            algo_id = await asyncio.to_thread(
                self.trading_service.stop_order,
                symbol=trade_params.symbol,
                side=trade_params.side,
                quantity=trade_params.quantity,
                stop_price=trade_params.stop_price,
                client=client
            )
            return algo_id
        except Exception as e:
            activity.logger.exception(
                f"stop_order() error: {e}"
            )
            raise
    
    @activity.defn
    async def exit_market_for_limit_position(
        self, trade_params: TradeParams
    ) -> int:
        try:
            client = get_futures_client(trade_params.api_key, trade_params.api_secret)
            order_id = await asyncio.to_thread(
                self.trading_service.exit_market_order,
                symbol=trade_params.symbol,
                side=trade_params.side,
                quantity=trade_params.quantity,
                quantity_decimals=trade_params.quantity_decimals,
                client=client
            )

            await send_telegram_message(
                chat_id=trade_params.chat_id,
                message=f"Position closed on {trade_params.symbol}👀"
            )

            return order_id
        except Exception as e:
            activity.logger.exception(
                f"new_order() error: {e}"
            )
            raise

    @activity.defn
    async def manage_position_iteration(
        self,
        position_iter_params: ManagePositionIterationParams,
    ) -> ManagePositionIterationResult:
        try:
            client = get_futures_client(
                position_iter_params.params.trade_params.api_key,
                position_iter_params.params.trade_params.api_secret
            )
            result = await self.trading_service.manage_position_iteration(
                user=position_iter_params.params.trade_params.user,
                symbol=position_iter_params.params.trade_params.symbol,
                side=position_iter_params.params.trade_params.side,
                atr_value=position_iter_params.params.trade_params.atr_value,
                atr_take_profit_mul=position_iter_params.params.trade_params.atr_take_profit_mul,
                chat_id=position_iter_params.params.trade_params.chat_id,
                leverage=position_iter_params.params.trade_params.leverage,
                algo_id=position_iter_params.params.algo_id,
                timeframe=position_iter_params.params.trade_params.timeframe,
                atr_length=position_iter_params.params.trade_params.atr_length,
                quantity_decimals=position_iter_params.params.trade_params.quantity_decimals,
                trailing_stop_price=position_iter_params.trailing_stop_price,
                take_profit_triggered=position_iter_params.take_profit_triggered,
                take_profit_order_id=position_iter_params.take_profit_order_id,
                profit_count=position_iter_params.profit_count,
                client=client
            )
            return result
        except Exception as e:
            activity.logger.exception(
                f"manage_position_iteration() error: {e}"
            )
            raise