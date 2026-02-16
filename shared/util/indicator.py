import talib
import pandas as pd


def ATR(DataFrame, N=14, isBacktesting:bool = False):
    res = talib.ATR(
        DataFrame.High.values.astype(float),
        DataFrame.Low.values.astype(float),
        DataFrame.Close.values.astype(float),
        N,
    )
    if isBacktesting:
        return res
    return pd.DataFrame({"ATR": res}, index=DataFrame.index)


def MA(DataFrame, N=20, isBacktesting:bool = False):
    res = talib.MA(DataFrame.Close.values.astype(float), N)
    if isBacktesting:
        return res
    return pd.DataFrame({f"MA{N}": res}, index=DataFrame.index)


def CCI(DataFrame, N=20, isBacktesting:bool = False):
    res = talib.CCI(
        DataFrame.High.values.astype(float),
        DataFrame.Low.values.astype(float),
        DataFrame.Close.values.astype(float),
        N,
    )
    if isBacktesting:
        return res
    return pd.DataFrame({"CCI": res}, index=DataFrame.index)

def RSI(DataFrame, N=14, isBacktesting:bool=False):
    res = talib.RSI(DataFrame.Close.values.astype(float), N)
    if isBacktesting:
        return res
    return pd.DataFrame({"RSI": res}, index=DataFrame.index)

def MA_for_indicators(DataFrame, Indicator, N=20, isBacktesting: bool = False):
    res = talib.MA(DataFrame[Indicator].values.astype(float), N)
    if isBacktesting:
        return res
    return pd.DataFrame({f"{Indicator}_MA": res}, index=DataFrame.index)

def ENGULFING(DataFrame, isBacktesting: bool = False):
    res = talib.CDLENGULFING(
        DataFrame.Open.values.astype(float),
        DataFrame.High.values.astype(float),
        DataFrame.Low.values.astype(float),
        DataFrame.Close.values.astype(float),
    )
    if isBacktesting:
        return res
    return pd.DataFrame({"ENGULFING": res}, index=DataFrame.index)

def BB(DataFrame, N=10, std=2, isBacktesting: bool = False):
    upper, middle, lower = talib.BBANDS(
        DataFrame.Close.values.astype(float), N, std, std
    )
    if isBacktesting:
        return upper, middle, lower
    return (
        pd.DataFrame({"BB": upper}, index=DataFrame.index),
        pd.DataFrame({"BB": middle}, index=DataFrame.index),
        pd.DataFrame({"BB": lower}, index=DataFrame.index),
    )

def MACD(DataFrame, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9, isBacktesting: bool = False):
    macd, signal, hist = talib.MACD(
        DataFrame.Close.values.astype(float),
        fastperiod=fastperiod,
        slowperiod=slowperiod,
        signalperiod=signalperiod,
    )
    if isBacktesting:
        return macd, signal, hist
    return pd.DataFrame({"MACD": hist}, index=DataFrame.index)