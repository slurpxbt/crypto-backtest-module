#######################
# Author: slurpxbt
#######################
import binance_candle_data as bcd
import pnl_display_func as pnl
from pathlib import Path
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

# pandas display, pycharm otherwise doesn't display all columns
pd.set_option('display.max_columns', 100)
desired_width = 500
pd.set_option('display.width', desired_width)
# ----------------------------------------------------------

root = Path("..")

def strategy():
    """
    TODO: YOU NEED TO DOWNLOAD DATA FIRST
    """
    # --------------------------------------------------------------------
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2020, 10, 1)
    # --------------------------------------------------------------------

    ticker = "ETHUSDT"  # binance spot pair
    time_frame = "1h"   # available time frames ["1min", "3min", "5min", "15min", "30min", "1h", "4h", "6h", "12h","1D"]
    filepath = f"data/{ticker}_{time_frame}.p"
    data = bcd.get_data_by_date(start_date, end_date, filepath)

    # format =  [open_time, open, high, low, close, volume, close_time, number_of_trades]
    candle_data_list = data.values.tolist()     # convert df to list

    pct_returns = []    # returns in %: [1, 2.2, 3.1, -2.1]
    coin_amount = []    # amount of coins after each trade
    usd_amount = []     # amount of usd after reach trade
    coin_prices = []    # price when trade was close
    strategy_type = "long-only"

    # STRATEGY GOES HERE
    # --------------------------------------------------------------------
    for candle in candle_data_list:
        print(candle)

    # --------------------------------------------------------------------

    return pct_returns, coin_amount, usd_amount, coin_prices, strategy_type, ticker, start_date, end_date


pct_returns, coin_amount, usd_amount, coin_prices, strategy_type, ticker, start_date, end_date = strategy()
pnl.display_pnl(pct_returns, coin_amount, usd_amount, coin_prices, strategy_type, ticker, start_date, end_date)