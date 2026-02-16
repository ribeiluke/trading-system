import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from shared.models.trade_plan import LIMIT_TRADING_TASK_QUEUE_NAME, TradeParams
from .workflows.trade_workflow import LimitTrading


async def main(data: TradeParams) -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("temporal:7233")

    try:
        result = await client.execute_workflow(
            LimitTrading.run,
            data,
            id=f"{data.strategy_name}-{data.user}-{data.symbol}",
            task_queue=LIMIT_TRADING_TASK_QUEUE_NAME,
        )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())