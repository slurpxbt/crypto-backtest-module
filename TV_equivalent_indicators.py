import pandas as pd
import numpy as np


def rsi_tradingview(ohlc: pd.DataFrame, period):
    delta = ohlc["close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm(up, alpha=1/period).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha=1/period).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))
    ohlc["RSI"] = rsi

    return ohlc


def WMA(s, period):
    return s.rolling(period).apply(lambda x: ((np.arange(period) + 1) * x).sum() / (np.arange(period) + 1).sum(), raw=True)

def HMA(s, period):
    return WMA(WMA(s, period // 2).multiply(2).sub(WMA(s, period)), int(np.sqrt(period)))