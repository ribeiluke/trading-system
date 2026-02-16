import argparse
import asyncio

from shared.database import mongo
from shared.util.data_collector import get_latest_ask, get_latest_bid
from shared.models.trade_plan import TradeParams
from shared.util.stop import calculate_stop_loss
from shared.util.position import (
    calculate_position_size,
    is_this_symbol_being_traded
)
from shared.temporal import workflow_starter
from strategy import registry


async def start_workflow_safe(params):
    try:
        await workflow_starter.main(data=params)
    except Exception as e:
        print(f"Workflow failed for {params.user}: {e}")


async def handle_trading_signal(
    users,
    strategy_parameters,
    wait_time_seconds,
    entry_validation_dict,
    direction: str,
    strategy_name: str,
):
    print(f"Trading period has begun. Let's go {direction}!")

    workflow_tasks = []
    symbol = strategy_parameters.get("symbol", "")
    symbol = "".join(symbol.split("/"))
    atr_value = entry_validation_dict.get("atr", 0.0)
    sl_multiplier = strategy_parameters.get("sl_multiplier", 0.0)
    print(f"symbol: {symbol}")
    latest_price = get_latest_bid(symbol) if direction == "BUY" else get_latest_ask(symbol)

    for user in users:
        if not user.get("active", False):
            print(f"User {user['email']} is not active. Skipping.")
            continue

        email = user.get("email", "")

        stop_loss = calculate_stop_loss(
            side=direction,
            symbol=symbol,
            current_price=latest_price,
            atr_value=atr_value,
            atr_multiplier=sl_multiplier
        )

        trade_params = TradeParams(
            api_key=user.get("api_key", ""),
            api_secret=user.get("secret_key", ""),
            user=email.split("@")[0] if email else "",
            symbol=symbol,
            side=direction,
            quantity=0.0,
            stop_price=stop_loss,
            atr_value=atr_value,
            timeframe=strategy_parameters.get("timeframe", ""),
            atr_length=strategy_parameters.get("atr_period", 0),
            user_email=email,
            chat_id=user.get("chat_id", 0),
            split_equally=strategy_parameters.get("split_equally", False),
            num_levels=strategy_parameters.get("dca_levels", 1),
            atr_trailing_stop_mul=sl_multiplier,
            atr_take_profit_mul=strategy_parameters.get("tp_multiplier", 0.0),
            wait_time_seconds=wait_time_seconds,
            strategy_name=strategy_name or "",
        )

        trade_params.quantity, trade_params.quantity_decimals = calculate_position_size(
            api_key=trade_params.api_key,
            api_secret=trade_params.api_secret,
            symbol=trade_params.symbol,
            current_price=latest_price,
            stop_price=trade_params.stop_price,
            risk=trade_params.risk_per_trade
        )

        try:
            if not is_this_symbol_being_traded(
                    api_key=trade_params.api_key,
                    api_secret=trade_params.api_secret,
                    symbol=trade_params.symbol
                ):
                print(f"Starting workflow for {trade_params.user}")
                asyncio.create_task(start_workflow_safe(trade_params))
            else:
                print(f"User {trade_params.user} already in a position. Skipping.")

        except Exception as e:
            print(f"Error for {trade_params.user}: {e}")



async def main(timeframe: str = "15m", collection: str = "channel_breakout_sma"):
    while True:
        try:
            users = await mongo.get_users()
            wait_time_seconds = await mongo.get_waitime_from_mongodb(timeframe=timeframe)

            tasks = []
            for strategy_name, components in registry.strategy_registry.items():
                strategy_param_list = await mongo.get_many_strategy_params(
                    timeframe=timeframe, collection=strategy_name
                )
                for strategy_parameters in strategy_param_list:
                    task = components["func"](
                        strategy_parameters=strategy_parameters,
                        users=users,
                        wait_time_seconds=wait_time_seconds,
                        strategy_name=strategy_name
                    )
                    tasks.append(task)

            await asyncio.gather(*tasks)

        except Exception as e:
            print(f"Error: {e}")
            continue
        await asyncio.sleep(wait_time_seconds)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run the trading bot with specified parameters.")
    parser.add_argument(
        "--timeframe",
        type=str,
        default="1h",
        help="Specify the timeframe for the bot (e.g., 1m, 5m, 15m, 1h, 4h). Default is 1h.",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="channel_breakout_sma",
        help="Specify the strategy. Default is 'channel_breakout_sma'.",
    )

    # Parse the arguments
    args = parser.parse_args()

    try:
        asyncio.run(main(timeframe=args.timeframe, collection=args.collection))
    except KeyboardInterrupt:
        print("Bot stopped by user.")
