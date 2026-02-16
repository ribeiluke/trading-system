import pandas as pd

from shared.util.data_collector import get_data
from shared.util.indicator import (
    MA_for_indicators,
    RSI,
    ATR,
    MA,
    ENGULFING,
    BB,
    MACD,
    CCI
)


def crossed_above(a, b):
        return a[-2] > b[-2] and a[-3] < b[-3]

def crossed_below(a, b):
    return a[-2] < b[-2] and a[-3] > b[-3]

def prepare_ohlcv_for_resample(
    df: pd.DataFrame,
    time_col: str = "Open time",
    unit: str = "ms",
    tz: str = "UTC"
) -> pd.DataFrame:
    """
    Prepare OHLCV dataframe for resampling.

    - Converts time column to DatetimeIndex
    - Deduplicates candles by timestamp
    - Ensures correct OHLCV aggregation
    """

    df = df.copy()

    # --- Ensure datetime index ---
    if not isinstance(df.index, pd.DatetimeIndex):
        if time_col not in df.columns:
            raise ValueError(f"'{time_col}' column not found in dataframe")

        df[time_col] = pd.to_datetime(df[time_col], unit=unit, utc=(tz == "UTC"))
        df.set_index(time_col, inplace=True)

    # --- Deduplicate timestamps (important for Binance data) ---
    if not df.index.is_unique:
        df = df.groupby(df.index).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    # --- Sort index (required for resample correctness) ---
    df.sort_index(inplace=True)

    return df



def signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    ma_length: int = 14,
    rsi_length: int = 14
) -> bool:
    """This Function checks if the market is in an up-trend pullback"""
    if "/" in instrument:
        instrument = "".join(instrument.split("/"))
    data = get_data(instrument=instrument, interval=timeframe)
    print(data)
    data[f"RSI"] = RSI(data, rsi_length)
    data[f"MA"] = MA_for_indicators(data, "RSI", ma_length)
    data["ATR"] = ATR(data)
    # based on latest confirmed closed
    latest_close = data["Close"].values[-2]
    latest_rsi_ma = data[f"MA"].values[-2]
    latest_rsi = data[f"RSI"].values[-2]
    if latest_rsi > latest_rsi_ma:
        return {"isTimeEnterLong":True,
                "isTimeEnterShort":False,
                "atr":data["ATR"].values[-2],
                "entry":latest_close
                }
        
    return {"isTimeEnterLong":False,
            "isTimeEnterShort":True,
            "atr":data["ATR"].values[-2],
            "entry":latest_close
            }


def bullish_volume_rsi_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    ma_length: int = 14,
    rsi_length: int = 14
) -> bool:
    """This Function checks if the market is in an up-trend pullback"""
    if "/" in instrument:
        instrument = "".join(instrument.split("/"))
    data = get_data(instrument=instrument, interval=timeframe)
    print(data)
    data[f"RSI"] = RSI(data, rsi_length)
    data["ATR"] = ATR(data)
    # based on latest confirmed closed
    latest_close = data["Close"].values[-2]
    latest_rsi = data[f"RSI"].values[-2]
    if latest_rsi > 60:
        if data["Close"].values[-2] < data["Close"].values[-3] < data["Open"].values[-3]:
                if data["Volume"].values[-2] < data["Volume"].values[-3]:
                    return {"isTimeEnterLong":True,
                            "isTimeEnterShort":False,
                            "atr":data["ATR"].values[-2],
                            "entry":latest_close
                            }
        
    return {"isTimeEnterLong":False,
            "isTimeEnterShort":False,
            "atr":data["ATR"].values[-2],
            "entry":latest_close
            }

def rsi_ma_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    ma_length: int = 100,
    rsi_length: int = 14,
    rsi_ma_length: int = 14
) -> bool:
    """This Function checks if the market is in an up-trend pullback"""
    if "/" in instrument:
        instrument = "".join(instrument.split("/"))
    data = get_data(instrument=instrument, interval=timeframe)
    data["RSI"] = RSI(data, rsi_length)
    data["RSI_MA"] = MA_for_indicators(data, "RSI", rsi_ma_length)
    data["MA"] = MA(data, ma_length)
    data["ATR"] = ATR(data)
    print(data)
    data["ATR"] = ATR(data)
    # based on latest confirmed closed
    latest_close = data["Close"].values[-2]

    if latest_close >= data["MA"].values[-2]:
        if data["RSI"].values[-3] < data["RSI_MA"].values[-3]:
            if data["RSI"].values[-2] > data["RSI_MA"].values[-2]:
                return {"isTimeEnterLong":True,
                                    "isTimeEnterShort":False,
                                    "atr":data["ATR"].values[-2],
                                    "entry":latest_close
                                    }
    else:
        if data["RSI"].values[-3] > data["RSI_MA"].values[-3]:
            if data["RSI"].values[-2] < data["RSI_MA"].values[-2]:
                return {"isTimeEnterLong":False,
                    "isTimeEnterShort":True,
                    "atr":data["ATR"].values[-2],
                    "entry":latest_close
                    }
    
    return {"isTimeEnterLong":False,
            "isTimeEnterShort":False,
            "atr":data["ATR"].values[-2],
            "entry":latest_close
            }

def channel_breakout_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    length: int = 5,
    atr_length: int = 100,
    ma_length: int = 100
) -> bool:
    """This Function checks if the market is in an up-trend pullback"""
    if "/" in instrument:
        instrument = "".join(instrument.split("/"))
    data = get_data(instrument=instrument, interval=timeframe)
    upper_bound = data.High.rolling(length).max()
    lower_bound = data.Low.rolling(length).min()
    print(data)
    data["ATR"] = ATR(data, atr_length)
    data["SMA"] = MA(data, ma_length)
    # based on latest confirmed closed
    latest_close = data["Close"].values[-2]
    latest_sma = data["SMA"].values[-2]

    latest_high = data["High"].values[-1]
    latest_low = data["Low"].values[-1]
    current_up_bound = upper_bound.values[-1]
    current_low_bound = lower_bound.values[-1]
    if latest_high >= current_up_bound:
        if latest_close > latest_sma:
            return {"isTimeEnterLong":True,
                                "isTimeEnterShort":False,
                                "atr":data["ATR"].values[-2],
                                "entry":latest_close
                                }
    
    if latest_low <= current_low_bound:
        if latest_close < latest_sma:
            return {"isTimeEnterLong":False,
                "isTimeEnterShort":True,
                "atr":data["ATR"].values[-2],
                "entry":latest_close
                }
    
    return {"isTimeEnterLong":False,
            "isTimeEnterShort":False,
            "atr":data["ATR"].values[-2],
            "entry":latest_close
            }
 

def engulfing_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    atr_length: int = 100,
) -> bool:
    """This Function checks if the market is in an up-trend pullback"""
    if "/" in instrument:
        instrument = "".join(instrument.split("/"))
    data = get_data(instrument=instrument, interval=timeframe)
    print(data)
    data["ATR"] = ATR(data, atr_length)
    data["ENGULFING"] = ENGULFING(data)
    # based on latest confirmed closed
    latest_close = data["Close"].values[-2]
    latest_engulfing = data["ENGULFING"].values[-2]
    if latest_engulfing == 100:
        return {"isTimeEnterLong":True,
                            "isTimeEnterShort":False,
                            "atr":data["ATR"].values[-2],
                            "entry":latest_close
                            }
    
    if latest_engulfing == -100:
        return {"isTimeEnterLong":False,
            "isTimeEnterShort":True,
            "atr":data["ATR"].values[-2],
            "entry":latest_close
            }
    
    return {"isTimeEnterLong":False,
            "isTimeEnterShort":False,
            "atr":data["ATR"].values[-2],
            "entry":latest_close
            }


def htf_range_ltf_mean_reversion_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "4h",
    rsi_len: int = 14,
    range_len: int = 20,
    atr_length: int = 100
) -> dict:
    """
    HTF range detection + LTF mean reversion entry
    """

    if "/" in instrument:
        instrument = "".join(instrument.split("/"))

    # ===== LTF DATA =====
    data = get_data(instrument=instrument, interval=timeframe)

    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)
    # ATR
    data["ATR"] = ATR(data, atr_length)

    # RSI
    delta = data.Close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(rsi_len).mean() / loss.rolling(rsi_len).mean()
    data["RSI"] = 100 - (100 / (1 + rs))

    # Latest confirmed LTF close
    latest_close = data["Close"].values[-2]

    # ===== HTF DATA =====
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    htf["range"] = (htf.High - htf.Low) / htf.Close
    htf["is_range"] = htf["range"] < htf["range"].rolling(range_len).mean()

    # Last confirmed HTF candle
    is_range = htf["is_range"].values[-2]

    # ===== SIGNAL LOGIC =====
    if is_range:
        # LONG
        if data["RSI"].values[-2] < 30:
            return {
                "isTimeEnterLong": True,
                "isTimeEnterShort": False,
                "atr": data["ATR"].values[-2],
                "entry": latest_close
            }

        # SHORT
        if data["RSI"].values[-2] > 70:
            return {
                "isTimeEnterLong": False,
                "isTimeEnterShort": True,
                "atr": data["ATR"].values[-2],
                "entry": latest_close
            }

    # ===== NO SIGNAL =====
    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": data["ATR"].values[-2],
        "entry": latest_close
    }


def htf_rsi_ltf_bullish_dec_volume_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "4h",
    rsi_len: int = 14,
    sma_len: int = 50,
    atr_length: int = 100
) -> dict:
    """
    HTF RSI bullish regime + LTF bearish pullback with volume contraction
    """

    if "/" in instrument:
        instrument = "".join(instrument.split("/"))

    # ===== LTF DATA =====
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)
    
    data["ATR"] = ATR(data, atr_length)

    latest_close = data["Close"].values[-2]
    data["SMA"] = MA(data, sma_len)
    latest_sma = data["SMA"].values[-2]

    # ===== HTF DATA =====
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    # HTF RSI
    delta = htf.Close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(rsi_len).mean() / loss.rolling(rsi_len).mean()
    htf["RSI"] = 100 - (100 / (1 + rs))

    # Last confirmed HTF candle
    htf_rsi = htf["RSI"].values[-2]

    # ===== SIGNAL LOGIC =====
    if htf_rsi > 60:
        # Uptrend
        if latest_close > latest_sma:

            # Bearish pullback structure
            if data.Close.values[-3] < data.Close.values[-4] < data.Open.values[-4]:

                # Volume contraction
                if data.Volume.values[-3] < data.Volume.values[-4]:
                    return {
                        "isTimeEnterLong": True,
                        "isTimeEnterShort": False,
                        "atr": data["ATR"].values[-2],
                        "entry": latest_close
                    }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": data["ATR"].values[-2],
        "entry": latest_close
    }


def htf_rsi_ltf_bearish_dec_volume_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "4h",
    rsi_len: int = 14,
    sma_len: int = 50,
    lookback_len: int = 15,
    atr_length: int = 100
) -> dict:
    """
    HTF RSI bearish regime + LTF bullish push with volume contraction (short setup)
    """

    if "/" in instrument:
        instrument = "".join(instrument.split("/"))

    # ===== LTF DATA =====
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)
    data["ATR"] = ATR(data, atr_length)
    # SMA
    data["SMA"] = MA(data, sma_len)

    # Resistance (rolling high)
    data["RESISTANCE"] = data.Close.rolling(lookback_len).max()

    latest_close = data["Close"].values[-2]
    latest_high = data["High"].values[-2]

    # ===== HTF DATA =====
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    # HTF RSI
    htf["RSI"] = RSI(htf, rsi_len)

    # Last confirmed HTF candle
    htf_rsi = htf["RSI"].values[-2]

    # ===== SIGNAL LOGIC =====
    if htf_rsi < 40:

         # Below SMA (bearish structure)
        if latest_close < data["SMA"].values[-2]:

            # Wick into resistance
            if latest_high >= data["RESISTANCE"].values[-2]:

                # Bearish continuation on LTF
                if (
                    data.Close.values[-2] > data.Close.values[-3] >
                    data.Close.values[-4] > data.Close.values[-5]
                ):

                    # Volume contraction
                    if (
                        data.Volume.values[-2] <
                        data.Volume.values[-3] <
                        data.Volume.values[-4]
                    ):
                        return {
                            "isTimeEnterLong": False,
                            "isTimeEnterShort": True,
                            "atr": data["ATR"].values[-2],
                            "entry": latest_close
                        }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": data["ATR"].values[-2],
        "entry": latest_close
    }


def htf_rsi_ltf_walk_bb_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "4h",
    rsi_len: int = 14,
    bb_len: int = 20,
    bb_std: float = 2.0,
    atr_length: int = 100
) -> dict:
    """
    HTF RSI regime + LTF Bollinger Band walk (trend continuation)
    """

    if "/" in instrument:
        instrument = "".join(instrument.split("/"))

    # ===== LTF DATA =====
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)
    
    # ATR
    data["ATR"] = ATR(data, atr_length)

    # Bollinger Bands
    upper, middle, lower = BB(data, bb_len, bb_std, True)
    data["BB_UPPER"] = upper
    data["BB_MIDDLE"] = middle
    data["BB_LOWER"] = lower

    # Latest confirmed prices
    price = data.Close.values[-2]
    prev_price = data.Close.values[-3]

    # ===== HTF DATA =====
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    # HTF RSI
    delta = htf.Close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(rsi_len).mean() / loss.rolling(rsi_len).mean()

    htf["RSI"] = 100 - (100 / (1 + rs))

    # Last confirmed HTF candle
    htf_rsi = htf["RSI"].values[-2]

    # ===== SIGNAL LOGIC =====

    # ---- LONG: Bullish HTF + BB walk up ----
    if htf_rsi > 60:
        if (
            price > data["BB_UPPER"].values[-2] and
            prev_price > data["BB_UPPER"].values[-3]
        ):
            return {
                "isTimeEnterLong": True,
                "isTimeEnterShort": False,
                "atr": data["ATR"].values[-2],
                "entry": price
            }

    # ---- SHORT: Bearish HTF + BB walk down ----
    elif htf_rsi < 40:
        if (
            price < data["BB_LOWER"].values[-2] and
            prev_price < data["BB_LOWER"].values[-3]
        ):
            return {
                "isTimeEnterLong": False,
                "isTimeEnterShort": True,
                "atr": data["ATR"].values[-2],
                "entry": price
            }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": data["ATR"].values[-2],
        "entry": price
    }


def htf_ltf_sync_rsi_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "1h",
    rsi_len: int = 14,
    rsi_ma_len: int = 20,
    atr_length: int = 100
) -> dict:
    """
    Sync RSI strategy:
    - HTF RSI crossover
    - LTF RSI confirmation crossover
    """

    if "/" in instrument:
        instrument = "".join(instrument.split("/"))

    # ===== LTF DATA =====
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)

    # LTF RSI + MA
    data["RSI"] = RSI(data, rsi_len, True)
    data["RSI_MA"] = MA_for_indicators(data, "RSI", rsi_ma_len, True)

    # ATR
    data["ATR"] = ATR(data, atr_length)

    # Latest confirmed values
    price = data.Close.values[-2]

    # ===== HTF DATA (1H) =====
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    htf_rsi = RSI(htf, rsi_len, True)
        
    htf_rsi_ma = pd.Series(htf_rsi).rolling(rsi_ma_len).mean().values

    # ===== SIGNAL LOGIC =====

    # LONG
    if (
        crossed_above(htf_rsi, htf_rsi_ma) and
        crossed_above(data["RSI"].values, data["RSI_MA"].values)
    ):
        return {
            "isTimeEnterLong": True,
            "isTimeEnterShort": False,
            "atr": data["ATR"].values[-2],
            "entry": price
        }

    # SHORT
    if (
        crossed_above(htf_rsi, htf_rsi_ma) and
        crossed_below(data["RSI"].values, data["RSI_MA"].values)
    ):
        return {
            "isTimeEnterLong": False,
            "isTimeEnterShort": True,
            "atr": data["ATR"].values[-2],
            "entry": price
        }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": data["ATR"].values[-2],
        "entry": price
    }


def htf_macd_ltf_channel_breakout_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "1h",
    length: int = 15,
    atr_period: int = 100,
    macd_fast: int = 12,
    macd_slow: int = 26,
    macd_signal: int = 9,
):
    if "/" in instrument:
        instrument = instrument.replace("/", "")

    # === LTF data ===
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)

    # === HTF data ===
    htf = get_data(instrument=instrument, interval=htf_timeframe)


    # === Indicators ===
    macd, signal, hist = MACD(
        htf,
        macd_fast,
        macd_slow,
        macd_signal,
        True
    )

    atr = ATR(data, atr_period, True)

    up_bound = data.High.rolling(length).max()
    down_bound = data.Low.rolling(length).min()

    # === Latest prices ===
    latest_close = data.Close.values[-2]   # confirmed close
    latest_high = data.High.values[-1]
    latest_low = data.Low.values[-1]
    latest_up_bound = up_bound.values[-1]
    latest_down_bound = down_bound.values[-1]

    # === Long ===
    if crossed_above(macd, signal):
        if latest_high >= latest_up_bound:
            return {
                "isTimeEnterLong": True,
                "isTimeEnterShort": False,
                "atr": atr[-2],
                "entry": latest_close,
            }

    # === Short ===
    if crossed_below(macd, signal):
        if latest_low <= latest_down_bound:
            return {
                "isTimeEnterLong": False,
                "isTimeEnterShort": True,
                "atr": atr[-2],
                "entry": latest_close,
            }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": atr[-2],
        "entry": latest_close,
    }


def htf_ltf_sync_cci_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "1h",
    cci_period: int = 20,
    htf_cci_period: int = 50,
    atr_period: int = 100,
):
    if "/" in instrument:
        instrument = instrument.replace("/", "")

    # === LTF data ===
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)

    # === HTF data ===
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    # === Indicators ===
    cci = CCI(data, cci_period, True)
    htf_cci = CCI(htf, htf_cci_period, True)
    atr = ATR(data, atr_period, True)

    # === Latest confirmed price ===
    latest_close = data.Close.values[-2]
    latest_htf_cci = htf_cci[-1]

    # === LONG ===
    if latest_htf_cci > 100 and crossed_above(cci, -100):
        return {
            "isTimeEnterLong": True,
            "isTimeEnterShort": False,
            "atr": atr[-2],
            "entry": latest_close,
        }

    # === SHORT ===
    if latest_htf_cci < -100 and crossed_below(cci, 100):
        return {
            "isTimeEnterLong": False,
            "isTimeEnterShort": True,
            "atr": atr[-2],
            "entry": latest_close,
        }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": atr[-2],
        "entry": latest_close,
    }


def htf_rsi_ltf_channel_breakout_signal(
    instrument: str = "ETHUSDT",
    timeframe: str = "5m",
    htf_timeframe: str = "1h",
    rsi_len: int = 14,
    atr_period: int = 100,
    length: int = 15,
):
    if "/" in instrument:
        instrument = instrument.replace("/", "")

    # === LTF data ===
    data = get_data(instrument=instrument, interval=timeframe)
    print("Timeframe: ", timeframe, " for instrument: ", instrument)
    print(data)

    # === HTF data ===
    htf = get_data(instrument=instrument, interval=htf_timeframe)

    # === Indicators ===
    rsi_htf = RSI(htf, rsi_len, True)
    atr = ATR(data, atr_period, True)

    up_bound = data.High.rolling(length).max()
    down_bound = data.Low.rolling(length).min()

    # === Latest prices ===
    latest_close = data.Close.values[-2]   # confirmed close
    latest_rsi = rsi_htf[-1]
    latest_high = data.High.values[-1]
    latest_low = data.Low.values[-1]
    latest_up_bound = up_bound.values[-1]
    latest_down_bound = down_bound.values[-1]

    # === LONG ===
    if latest_rsi > 60:
        if latest_high >= latest_up_bound:
            return {
                "isTimeEnterLong": True,
                "isTimeEnterShort": False,
                "atr": atr[-2],
                "entry": latest_close,
            }

    # === SHORT ===
    if latest_rsi < 40:
        if latest_low <= latest_down_bound:
            return {
                "isTimeEnterLong": False,
                "isTimeEnterShort": True,
                "atr": atr[-2],
                "entry": latest_close,
            }

    return {
        "isTimeEnterLong": False,
        "isTimeEnterShort": False,
        "atr": atr[-2],
        "entry": latest_close,
    }
