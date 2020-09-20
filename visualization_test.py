#######################
# Author: slurpxbt
#######################
from pathlib import Path
import pandas as pd
import pickle
import datetime
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpdates

import binance_candle_data as bcd

# pandas display, pycharm otherwise doesn't display all columns
pd.set_option('display.max_columns', 40)
desired_width = 500
pd.set_option('display.width', desired_width)
# ------------------------------------------------------------
# root for file directory
root = Path(".")
# ------------------------------------------------------------


# DATA VARIABLES ----------------------------------------------
ticker = "BTCUSDT"
time_frame = "1D"

# file path
file_path = f"{root}/data/{ticker}_{time_frame}.p"

# start date of backtest
startDate = datetime.datetime(2020, 6, 1)
# end date of backtest
endDate = datetime.datetime(2020, 9, 1)
# -------------------------------------------------------------

backtest_data = bcd.get_data_by_date(startDate, endDate, file_path)
backtest_data["candle pct gain"] = round((backtest_data["close"]/backtest_data["open"]-1)*100, 3)


def plt_candle_pct_chg(pct_changes, candle_data, close_times):
    labels = []
    for date in close_times:
        date_format = f"{date.date()}/{date.hour}:{date.minute}"
        labels.append(date_format)
        print(date_format)
    closes_x_labels = labels

    plt.subplots_adjust(top=0.95, bottom=0.05, hspace=15)

    close_graph = plt.subplot2grid((6, 1), (0, 0), rowspan=3)
    pct_graph = plt.subplot2grid((6, 1), (3, 0), rowspan=2)

    closes_x = [i for i in range(len(candle_data))]   # some dates are missing that's why i create x tick(xticks have equal spacing)
    close_graph.plot(closes_x, candle_data)
    close_graph.set_xticks(closes_x)
    close_graph.set_xticklabels(labels=closes_x_labels, rotation=90)
    close_graph.grid(alpha=0.1)
    close_graph.margins(x=0.01)

    pct_x = [i for i in range(len(pct_changes))]
    pct_graph.bar(pct_x, pct_changes, width=0.8)
    pct_graph.set_xticks(pct_x)
    pct_graph.set_xticklabels(labels=closes_x_labels, rotation=90)
    pct_graph.margins(x=0.01)
    pct_graph.grid(alpha=0.1)

    figMan = plt.get_current_fig_manager()
    figMan.window.showMaximized()

    plt.show()



def plt_candle_pct_chgV2(pct_changes, candle_data, close_times):

    ohlc = candle_data[candle_data.columns[0:5]]
    ohlc['open_time'] = pd.to_datetime(ohlc['open_time'])
    ohlc['open_time'] = ohlc['open_time'].map(mpdates.date2num)

    labels = []
    for date in close_times:
        date_format = f"{date.date()}"
        labels.append(date_format)
        print(date_format)
    closes_x_labels = labels


    plt.style.use('ggplot')
    candle_graph = plt.subplot2grid((8, 1), (0, 0), rowspan=5)
    pct_graph = plt.subplot2grid((8, 1), (5, 0), rowspan=2)
    plt.subplots_adjust(top=0.95, bottom=0.05, hspace=10)

    candlestick_ohlc(candle_graph, ohlc.values, width=0.6, colorup="green", colordown="red", alpha=0.8)
    candle_graph.set_xticklabels(labels=closes_x_labels, rotation=90)
    candle_graph.margins(x=0.01)

    pct_x = [i for i in range(len(pct_changes))]
    pct_graph.bar(pct_x, pct_changes, width=0.8, color="purple")
    pct_graph.set_xticks(pct_x)
    pct_graph.set_xticklabels(labels=closes_x_labels, rotation=90)
    pct_graph.set_yticks(range(-10,12,2))
    pct_graph.margins(x=0.01)
    pct_graph.grid(alpha=0.5)

    figMan = plt.get_current_fig_manager()
    figMan.window.showMaximized()

    plt.show()



plt_candle_pct_chg(backtest_data['candle pct gain'], backtest_data['close'], backtest_data['open_time'])
plt_candle_pct_chgV2(backtest_data['candle pct gain'], backtest_data, backtest_data['open_time'])

# data format [open_time, open, high, low, close, volume, close_time, number_of_trades]
backtest_data_list = backtest_data.values.tolist()

closes = []
opens = []
highs = []
lows = []
for i in backtest_data_list:
    try:
        volume_per_trade = round(i[5] / i[-1], 4)
        print(i)
        i.append(volume_per_trade)
    except:
        i.append(0)

    opens.append(i[1])
    closes.append(i[4])
    highs.append(i[2])
    lows.append(i[3])

plt.plot(opens, label="open")
plt.plot(lows, label="low")
plt.plot(highs, label="high")
plt.legend()
plt.show()