from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from shared.temporal.activities.limit_trading import TradingLimitActivities
    from shared.models.trade_plan import ManagePositionParams, OrderParams, TradeParams
    from shared.util.telegram import send_telegram_message



@workflow.defn
class LimitTrading:
    @workflow.run
    async def run(self, trade_params: TradeParams) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=10,
            maximum_interval=timedelta(seconds=2.0)
        )

        # Enter a trade
        try:
            order_id = await workflow.execute_activity_method(
                TradingLimitActivities.enter_limit,
                trade_params,
                start_to_close_timeout=timedelta(seconds=10.0),
                retry_policy=retry_policy,
            )
        except ActivityError as enter_err:
            workflow.logger.error(f"Failed to enter trade: {enter_err}")
            raise enter_err

        # Check if the order is filled
        try:
            is_filled, message = await workflow.execute_activity_method(
                TradingLimitActivities.is_order_filled,
                OrderParams(
                    trade_params=trade_params, order_id=order_id
                ),
                start_to_close_timeout=timedelta(minutes=1.0),
                retry_policy=retry_policy,
            )

            workflow.logger.info(f"Order {order_id} filled status: {is_filled}")

        except ActivityError as filled_err:
            workflow.logger.error(f"Order check failed: {filled_err}")
            # Attempt to cancel the order
            try:
                status = await workflow.execute_activity_method(
                    TradingLimitActivities.cancel_limit,
                    OrderParams(
                    trade_params=trade_params, order_id=order_id
                ),
                    start_to_close_timeout=timedelta(seconds=5.0),
                    retry_policy=retry_policy,
                )
                workflow.logger.info(
                    f"Cancel successful. Confirmation status: {status}"
                )
                return f"Order {order_id} was not filled and has been cancelled. Status: {status}"
            except TimeoutError as cancel_error:
                workflow.logger.error(f"Cancel failed: {cancel_error}")
                raise cancel_error from filled_err
    
        algo_id = await workflow.execute_activity_method(
            TradingLimitActivities.place_stop_order,
            trade_params,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )

        await workflow.execute_activity_method(
            TradingLimitActivities.manage_position,
            ManagePositionParams(
                trade_params=trade_params,
                order_id=order_id,
                algo_id=algo_id
            ),
            start_to_close_timeout=timedelta(weeks=5.0),
            retry_policy=retry_policy,
        )