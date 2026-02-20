from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from shared.temporal.activities.limit_trading import TradingLimitActivities
    from shared.temporal.activities.market_trading import TradingMarketActivities
    from shared.models.trade_plan import (
        ManagePositionParams,
        OrderParams,
        TradeParams,
        ManagePositionIterationParams,
        TRADING_TASK_QUEUE_NAME
    )



@workflow.defn
class LimitTrading:
    @workflow.run
    async def run(self, trade_params: TradeParams) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=5,
            maximum_interval=timedelta(seconds=2.0)
        )

        # Set leverage
        try:
            trade_params.leverage = await workflow.execute_activity_method(
                TradingLimitActivities.set_leverage,
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
                TradingLimitActivities.enter_limit,
                trade_params,
                start_to_close_timeout=timedelta(seconds=5.0),
                retry_policy=retry_policy,
            )
        except ActivityError as enter_err:
            workflow.logger.error(f"Failed to enter trade: {enter_err}")
            raise enter_err

        deadline = workflow.now() + timedelta(seconds=30)

        while workflow.now() < deadline:
            try:
                is_filled = await workflow.execute_activity_method(
                    TradingLimitActivities.is_order_filled,
                    OrderParams(
                        trade_params=trade_params, order_id=order_id
                    ),
                    start_to_close_timeout=timedelta(seconds=5.0),
                    retry_policy=retry_policy,
                )
                workflow.logger.info(f"Order {order_id} filled status: {is_filled}")
                if is_filled:
                    break
                await workflow.sleep(5)
            except ActivityError as filled_err:
                workflow.logger.error(f"Order check failed: {filled_err}")
                raise filled_err

        if not is_filled:
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
            except ActivityError as cancel_error:
                workflow.logger.error(f"Cancel failed: {cancel_error}")
                if "-2011" in str(cancel_error):
                    workflow.logger.warning(
                        "Order already filled during cancellation attempt."
                    )
                else:
                    raise cancel_error
    
        algo_id = await workflow.execute_activity_method(
            TradingLimitActivities.place_stop_order,
            trade_params,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )

        await workflow.start_child_workflow(
            ManageLimitPositionWorkflow.run,
            ManagePositionParams(
                trade_params=trade_params,
                order_id=order_id,
                algo_id=algo_id
            ),
            id=f"manage-limit-{trade_params.user}-{trade_params.symbol}",
            task_queue=TRADING_TASK_QUEUE_NAME,
            run_timeout=timedelta(weeks=10.0),
            parent_close_policy=workflow.ParentClosePolicy.ABANDON
        )

@workflow.defn
class ManageLimitPositionWorkflow:
    @workflow.run
    async def run(self, params: ManagePositionParams):
        trailing_stop_price = params.trade_params.stop_price
        take_profit_triggered = False
        finished = False

        retry_policy = RetryPolicy(maximum_attempts=3)

        while not finished:
            result = await workflow.execute_activity_method(
                TradingLimitActivities.manage_position_iteration,
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
                await workflow.sleep((params.trade_params.wait_time_seconds) / 2)
        return "POSITION CLOSED"


@workflow.defn
class MarketTrading:
    @workflow.run
    async def run(self, trade_params: TradeParams) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=10,
            maximum_interval=timedelta(seconds=2.0)
        )

        # Set leverage
        try:
            trade_params.leverage = await workflow.execute_activity_method(
                TradingMarketActivities.set_market_leverage,
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
                TradingMarketActivities.enter_market,
                trade_params,
                start_to_close_timeout=timedelta(seconds=5.0),
                retry_policy=retry_policy,
            )
        except ActivityError as enter_err:
            workflow.logger.error(f"Failed to enter trade: {enter_err}")
            raise enter_err

        algo_id = await workflow.execute_activity_method(
                    TradingMarketActivities.place_market_stop_order,
                    trade_params,
                    start_to_close_timeout=timedelta(seconds=5),
                    retry_policy=retry_policy,
                )

        await workflow.start_child_workflow(
            ManageMarketPositionWorkflow.run,
            ManagePositionParams(
                trade_params=trade_params,
                order_id=order_id,
                algo_id=algo_id
            ),
            id=f"manage-market-{trade_params.user}-{trade_params.symbol}",
            task_queue=TRADING_TASK_QUEUE_NAME,
            run_timeout=timedelta(weeks=10),
            parent_close_policy=workflow.ParentClosePolicy.ABANDON
        )

@workflow.defn
class ManageMarketPositionWorkflow:
    @workflow.run
    async def run(self, params: ManagePositionParams):
        trailing_stop_price = params.trade_params.stop_price
        take_profit_triggered = False
        finished = False

        retry_policy = RetryPolicy(maximum_attempts=3)

        while not finished:
            result = await workflow.execute_activity_method(
                TradingMarketActivities.manage_market_position_iteration,
                ManagePositionIterationParams(
                    params=params,
                    trailing_stop_price=trailing_stop_price,
                    take_profit_triggered=take_profit_triggered
                ),
                start_to_close_timeout=timedelta(seconds=5.0),
                retry_policy=retry_policy,
            )

            trailing_stop_price = result.trailing_stop_price
            take_profit_triggered = result.take_profit_triggered
            finished = result.finished
            params.trade_params.atr_value = result.atr_value

            if not finished:
                # Sleep inside workflow (does not block worker)
                await workflow.sleep((params.trade_params.wait_time_seconds) / 2)
        return "POSITION CLOSED"