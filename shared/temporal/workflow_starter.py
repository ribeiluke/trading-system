import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from shared.models.trade_plan import (
    TRADING_TASK_QUEUE_NAME,
    TradeParams
)
from .workflows.trade_workflow import LimitTrading, MarketTrading
from .workflows.testnet_trade_workflow import TestnetLimitTrading


async def main(data: TradeParams) -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("temporal:7233")

    try:
        if data.timeframe == "1m":
            result = await client.execute_workflow(
                LimitTrading.run,
                data,
                id=f"{data.strategy_name}-{data.user}-{data.symbol}",
                task_queue=TRADING_TASK_QUEUE_NAME,
            )
        else:
            result = await client.execute_workflow(
                MarketTrading.run,
                data,
                id=f"{data.strategy_name}-{data.user}-{data.symbol}",
                task_queue=TRADING_TASK_QUEUE_NAME,
            )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


async def testnet_main(data: TradeParams) -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("temporal:7233")

    try:
        result = await client.execute_workflow(
            TestnetLimitTrading.run,
            data,
            id=f"{data.strategy_name}-{data.user}-{data.symbol}",
            task_queue=TRADING_TASK_QUEUE_NAME,
        )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())