from app.main import handle_trading_signal
from app.strategy import signals

async def handle_trading_signal_caller(
    users, strategy_parameters, wait_time_seconds, entry_validation_dict, strategy_name: str
):
    if entry_validation_dict["isTimeEnterLong"]:
        await handle_trading_signal(
            users=users,
            strategy_parameters=strategy_parameters,
            wait_time_seconds=wait_time_seconds,
            entry_validation_dict=entry_validation_dict,
            direction="BUY",
            strategy_name=strategy_name
        )

    if entry_validation_dict["isTimeEnterShort"]:
        await handle_trading_signal(
            users=users,
            strategy_parameters=strategy_parameters,
            wait_time_seconds=wait_time_seconds,
            entry_validation_dict=entry_validation_dict,
            direction="SELL",
            strategy_name=strategy_name
        )

async def channel_breakout_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.channel_breakout_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        length=strategy_parameters["length"],
        ma_length=strategy_parameters["sma_period"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )


async def engulfing_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.engulfing_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )

async def htf_range_ltf_mean_reversion_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_range_ltf_mean_reversion_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        rsi_len=strategy_parameters["rsi_period"],
        range_len=strategy_parameters["range_period"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )

async def htf_rsi_ltf_bullish_dec_volume_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_rsi_ltf_bullish_dec_volume_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        rsi_len=strategy_parameters["rsi_period"],
        sma_len=strategy_parameters["sma_period"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )

async def htf_rsi_ltf_bearish_dec_volume_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_rsi_ltf_bearish_dec_volume_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        rsi_len=strategy_parameters["rsi_period"],
        sma_len=strategy_parameters["sma_period"],
        lookback_len=strategy_parameters["lookback_period"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )


async def htf_rsi_ltf_walk_bb_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_rsi_ltf_walk_bb_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        rsi_len=strategy_parameters["rsi_period"],
        bb_len=strategy_parameters["bb_period"],
        bb_std=strategy_parameters["bb_std"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )


async def htf_ltf_sync_rsi_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_ltf_sync_rsi_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        rsi_len=strategy_parameters["rsi_period"],
        rsi_ma_len=strategy_parameters["rsi_ma_period"],
        atr_length=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )


async def htf_macd_ltf_channel_breakout_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_macd_ltf_channel_breakout_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        length=strategy_parameters["length"],
        macd_fast=strategy_parameters["macd_fast_period"],
        macd_slow=strategy_parameters["macd_slow_period"],
        macd_signal=strategy_parameters["macd_signal_period"],
        atr_period=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )


async def htf_ltf_sync_cci_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_ltf_sync_cci_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        htf_cci_period=strategy_parameters["htf_cci_period"],
        cci_period=strategy_parameters["cci_period"],
        atr_period=strategy_parameters["atr_period"],
    )

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )


async def htf_rsi_ltf_channel_breakout_run(
    strategy_parameters: dict, users: list, wait_time_seconds: int, strategy_name:str
):
    entry_validation_dict = signals.htf_rsi_ltf_channel_breakout_signal(
        instrument=strategy_parameters["symbol"],
        timeframe=strategy_parameters["timeframe"],
        htf_timeframe=strategy_parameters["higher_timeframe"],
        length=strategy_parameters["length"],
        rsi_len=strategy_parameters["rsi_period"],
        atr_period=strategy_parameters["atr_period"],
    )

    entry_validation_dict["isTimeEnterLong"] = True

    await handle_trading_signal_caller(
        users=users,
        strategy_parameters=strategy_parameters,
        wait_time_seconds=wait_time_seconds,
        entry_validation_dict=entry_validation_dict,
        strategy_name=strategy_name
    )

strategy_registry = {
    "channel_breakout_sma": {
        "runner": "channel_breakout_run",
        "func": channel_breakout_run
    },
    "engulfing": {
        "runner": "engulfing_run",
        "func": engulfing_run
    },
    "multi_timeframe_mean_reversion": {
        "runner": "htf_range_ltf_mean_reversion_run",
        "func": htf_range_ltf_mean_reversion_run
    },
    "multi_timeframe_bullish_dec_vol_rsi": {
        "runner": "htf_rsi_ltf_bullish_dec_volume_run",
        "func": htf_rsi_ltf_bullish_dec_volume_run
    },
    "multi_timeframe_bearish_dec_vol_rsi": {
        "runner": "htf_rsi_ltf_bearish_dec_volume_run",
        "func": htf_rsi_ltf_bearish_dec_volume_run
    },
    "multi_timeframe_bb_walk_band": {
        "runner": "htf_rsi_ltf_walk_bb_run",
        "func": htf_rsi_ltf_walk_bb_run
    },
    "multi_timeframe_sync_rsi": {
        "runner": "htf_ltf_sync_rsi_run",
        "func": htf_ltf_sync_rsi_run
    },
    "multi_timeframe_macd_channel_breakout": {
        "runner": "htf_macd_ltf_channel_breakout_run",
        "func": htf_macd_ltf_channel_breakout_run
    },
    "multi_timeframe_sync_cci": {
        "runner": "htf_ltf_sync_cci_run",
        "func": htf_ltf_sync_cci_run
    },
    "multi_timeframe_rsi_channel_breakout": {
        "runner": "htf_rsi_ltf_channel_breakout_run",
        "func": htf_rsi_ltf_channel_breakout_run
    },
}
