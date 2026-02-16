import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from shared.temporal.activities.limit_trading import TradingLimitActivities
from shared.models.trade_plan import LIMIT_TRADING_TASK_QUEUE_NAME

from shared.temporal.workflows.trade_workflow import LimitTrading


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

    worker = Worker(
        client,
        task_queue=LIMIT_TRADING_TASK_QUEUE_NAME,
        workflows=[LimitTrading],
        activities=[
            activities.enter_limit,
            activities.is_order_filled,
            activities.cancel_limit,
            activities.place_stop_order,
            activities.manage_position
        ],
    )

    await worker.run()



if __name__ == "__main__":
    asyncio.run(main())