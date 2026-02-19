from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from shared.temporal.activities.testnet_limit_trading import TestnetTradingLimitActivities
    from shared.models.trade_plan import (
        ManagePositionParams,
        OrderParams,
        TradeParams,
        ManagePositionIterationParams,
        TRADING_TASK_QUEUE_NAME
    )
    from shared.util.telegram import send_telegram_message



@workflow.defn
class TestnetLimitTrading:
    @workflow.run
    async def run(self, trade_params: TradeParams) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=10,
            maximum_interval=timedelta(seconds=2.0)
        )

        # Set leverage
        try:
            trade_params.leverage = await workflow.execute_activity_method(
                TestnetTradingLimitActivities.demo_set_leverage,
                trade_params,
                start_to_close_timeout=timedelta(seconds=5.0),
                retry_policy=retry_policy,
            )
        except ActivityError as set_leverage_error:
            workflow.logger.error(f"Failed to set leverage: {set_leverage_error}")
            raise set_leverage_error

        # Enter a trade
        try:
            order_id = await workflow.execute_activity_method(
                TestnetTradingLimitActivities.demo_enter_limit,
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
                TestnetTradingLimitActivities.demo_is_order_filled,
                OrderParams(
                    trade_params=trade_params, order_id=order_id
                ),
                start_to_close_timeout=timedelta(seconds=30.0),
                retry_policy=retry_policy,
            )

            workflow.logger.info(f"Order {order_id} filled status: {is_filled}")

        except ActivityError as filled_err:
            workflow.logger.error(f"Order check failed: {filled_err}")
            # Attempt to cancel the order
            try:
                status = await workflow.execute_activity_method(
                    TestnetTradingLimitActivities.demo_cancel_limit,
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
            TestnetTradingLimitActivities.demo_place_stop_order,
            trade_params,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )

        await workflow.start_child_workflow(
            TestnetManagePositionWorkflow.run,
            ManagePositionParams(
                trade_params=trade_params,
                order_id=order_id,
                algo_id=algo_id
            ),
            id=f"manage-{trade_params.user}-{trade_params.symbol}",
            task_queue=TRADING_TASK_QUEUE_NAME,
            run_timeout=timedelta(weeks=10),
            parent_close_policy=workflow.ParentClosePolicy.ABANDON
        )

@workflow.defn
class TestnetManagePositionWorkflow:
    @workflow.run
    async def run(self, params: ManagePositionParams):
        trailing_stop_price = params.trade_params.stop_price
        take_profit_triggered = False
        finished = False

        retry_policy = RetryPolicy(maximum_attempts=3)

        while not finished:
            result = await workflow.execute_activity_method(
                TestnetTradingLimitActivities.demo_manage_position_iteration,
                ManagePositionIterationParams(
                    params=params,
                    trailing_stop_price=trailing_stop_price,
                    take_profit_triggered=take_profit_triggered
                ),
                start_to_close_timeout=timedelta(minutes=1.0),
                retry_policy=retry_policy,
            )

            trailing_stop_price = result.trailing_stop_price
            take_profit_triggered = result.take_profit_triggered
            finished = result.finished
            params.trade_params.atr_value = result.atr_value

            if not finished:
                # Sleep inside workflow (does not block worker)
                await workflow.sleep(params.trade_params.wait_time_seconds)
        return "POSITION CLOSED"