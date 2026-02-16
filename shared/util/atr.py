from shared.util.data_collector import get_data
from shared.util.indicator import ATR

def get_latest_atr(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    atr_length: int = 100,
) -> float:
    if "/" in instrument:
        instrument = "".join(instrument.split("/"))
    data = get_data(instrument=instrument, interval=timeframe)
    data["ATR"] = ATR(data, atr_length)
    return data["ATR"].values[-2]