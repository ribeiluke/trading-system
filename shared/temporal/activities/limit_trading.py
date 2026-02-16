import asyncio

from temporalio import activity

from .service.limit_service import LimitService
from shared.config.auth import get_futures_client
from shared.models.trade_plan import ManagePositionParams, OrderParams, TradeParams
from shared.util.telegram import send_telegram_message

class TradingLimitActivities:
    def __init__(self):
        self.trading_service = LimitService()

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
                client=client
            )
            return order_id
        except Exception as e:
            activity.logger.exception(
                f"new_order() error: {e}"
            )
            raise

    @activity.defn
    async def is_order_filled(self, order_params:OrderParams) -> tuple[bool, str]:
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

                try:
                    await send_telegram_message(
                        chat_id=order_params.trade_params.chat_id,
                        message=message
                    )
                except Exception as e:
                    activity.logger.error(f"Telegram send failed: {e}")

            return is_filled, message if is_filled else ""
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
            raise
    
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
    async def manage_position(
        self,
        manage_position_params: ManagePositionParams,
    ):
        try:
            client = get_futures_client(
                manage_position_params.trade_params.api_key,
                manage_position_params.trade_params.api_secret
            )
            await self.trading_service.manage_position(
                user=manage_position_params.trade_params.user,
                symbol=manage_position_params.trade_params.symbol,
                side=manage_position_params.trade_params.side,
                stop_price=manage_position_params.trade_params.stop_price,
                atr_value=manage_position_params.trade_params.atr_value,
                atr_take_profit_mul=manage_position_params.trade_params.atr_take_profit_mul,
                chat_id=manage_position_params.trade_params.chat_id,
                leverage=manage_position_params.trade_params.leverage,
                algo_id=manage_position_params.algo_id,
                timeframe=manage_position_params.trade_params.timeframe,
                atr_length=manage_position_params.trade_params.atr_length,
                wait_time_seconds=manage_position_params.trade_params.wait_time_seconds,
                quantity_decimals=manage_position_params.trade_params.quantity_decimals,
                client=client
            )
        except Exception as e:
            activity.logger.exception(
                f"manage_position() error: {e}"
            )
            raise