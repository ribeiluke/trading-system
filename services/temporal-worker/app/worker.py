import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from shared.temporal.activities.limit_trading import TradingLimitActivities
from shared.temporal.activities.market_trading import TradingMarketActivities
from shared.models.trade_plan import TRADING_TASK_QUEUE_NAME

from shared.temporal.activities.testnet_limit_trading import TestnetTradingLimitActivities
from shared.temporal.workflows.trade_workflow import (
    LimitTrading,
    ManageLimitPositionWorkflow,
    MarketTrading,
    ManageMarketPositionWorkflow
)
from shared.temporal.workflows.testnet_trade_workflow import (
    TestnetLimitTrading, TestnetManagePositionWorkflow
)


async def connect_temporal():
    address = os.getenv("TEMPORAL_SERVER", "temporal:7233")

    while True:
        try:
            print(f"Connecting to Temporal at {address}...")
            client = await Client.connect(address, namespace="default")
            print("Connected to Temporal ✅")
            return client
        except Exception as e:
            print(f"Temporal not ready yet: {e}")
            await asyncio.sleep(3)


async def main() -> None:
    client: Client = await connect_temporal()

    activities = TradingLimitActivities()
    testnet_activities = TestnetTradingLimitActivities()
    market_activities = TradingMarketActivities()

    worker = Worker(
        client,
        task_queue=TRADING_TASK_QUEUE_NAME,
        workflows=[
            LimitTrading,
            ManageLimitPositionWorkflow,
            MarketTrading,
            ManageMarketPositionWorkflow,
            TestnetLimitTrading,
            TestnetManagePositionWorkflow
        ],
        activities=[
            activities.set_leverage,
            activities.enter_limit,
            activities.is_order_filled,
            activities.cancel_limit,
            activities.place_stop_order,
            activities.manage_position_iteration,
            market_activities.set_market_leverage,
            market_activities.enter_market,
            market_activities.place_market_stop_order,
            market_activities.manage_market_position_iteration,
            testnet_activities.demo_set_leverage,
            testnet_activities.demo_enter_limit,
            testnet_activities.demo_is_order_filled,
            testnet_activities.demo_cancel_limit,
            testnet_activities.demo_place_stop_order,
            testnet_activities.demo_manage_position_iteration
        ],
    )

    await worker.run()




if __name__ == "__main__":
    asyncio.run(main())