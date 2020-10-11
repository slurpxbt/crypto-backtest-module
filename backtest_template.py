#######################
# Author: slurpxbt
#######################
import binance_candle_data as bcd
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

# USER INPUTS --------------------------------------------------------
# --------------------------------------------------------------------
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020, 10, 1)
# --------------------------------------------------------------------
time_frame = "1h"
ticker = "ETHUSDT"
# --------------------------------------------------------------------
start_size = 5000  # contracts
size = start_size
# --------------------------------------------------------------------
market_order_fee = 0.075    # unit [%]
slippage = 0.1              # unit [%]
# --------------------------------------------------------------------
tp_pct = 0.01               # unit => 1 - 100%, 0.1 - 10%, 0.01 - 1%
# --------------------------------------------------------------------
compounding = True
# END OF USER INPUTS -------------------------------------------------


filepath = f"data/{ticker}_{time_frame}.p"
data = bcd.get_data_by_date(start_date, end_date, filepath)

# ----------------------------------------------------------------
# Add MA and EMAs here
data["EMA5"] = round(data["close"].ewm(span=5).mean(), 2)
data["EMA10"] = round(data["close"].ewm(span=10).mean(), 2)
# ----------------------------------------------------------------

# format =  [open_time, open, high, low, close, volume, close_time, number_of_trades, EMA5,  EMA10]
candle_data_list = data.values.tolist()     # convert df to list


short_long = ""
trade_opened = False

pnl = []
tps = []
sls = []
cum_size = []

for candle in candle_data_list:
    close = candle[4]           # candle open prc
    low = candle[3]             # candle low prc
    high = candle[2]            # candle high prc
    ema5 = candle[8]            # 5 ema
    ema10 = candle[9]           # 10 ema

    # YOUR STRATEGY GOES HERE
    if not trade_opened:
        trade_entry = 0
        tp = 0
        if close < ema10 and close < ema5:
            short_long = "short"
            trade_opened = True
            trade_entry = close
            tp = round(trade_entry - (trade_entry * tp_pct), 2)
            print(f"short entry @ {trade_entry} with tp @ {tp} -> size {size}")

        elif close > ema5 and close > ema10:
            short_long = "long"
            trade_opened = True
            trade_entry = close
            tp = round(trade_entry + (trade_entry * tp_pct), 2)
            print(f"long entry @ {trade_entry} with tp @ {tp} -> size {size}")


    if trade_opened:

        if short_long == "short":   # short

            if close <= tp or low <= tp:
                gain = round((tp / trade_entry - 1) * 100 * (-1) - market_order_fee - slippage, 2)
                trade_profit = gain * size / 100

                cum_size.append(size + trade_profit)
                if compounding:
                    size = size + trade_profit
                pnl.append(trade_profit)
                tps.append(trade_profit)

                print(f"tp executed @ {tp} -> gain {gain}% -> profit {trade_profit} $")
                trade_opened = False
                print("-"*100)

            elif close > ema10 and close > ema5:
                gain = round((close / trade_entry - 1) * 100 * (-1) - market_order_fee - slippage, 2)
                trade_profit = gain * size / 100

                cum_size.append(size + trade_profit)
                if compounding:
                    size = size + trade_profit
                pnl.append(trade_profit)
                sls.append(trade_profit)

                print(f"sl executed @ {close} -> gain {gain}% -> profit {trade_profit} $")
                trade_opened = False
                print("-" * 100)

        elif short_long == "long":  # long

            if close >= tp or high >= tp:
                gain = round((tp / trade_entry - 1) * 100 - market_order_fee - slippage,2)
                trade_profit = gain * size / 100

                cum_size.append(size + trade_profit)
                if compounding:
                    size = size + trade_profit
                pnl.append(trade_profit)
                tps.append(trade_profit)
                print(f"tp executed @ {tp} -> gain {gain}% -> profit {trade_profit} $")
                trade_opened = False
                print("-" * 100)

            elif close < ema10 and close < ema5:
                gain = round((close / trade_entry - 1) * 100 - market_order_fee - slippage, 2)
                trade_profit = gain * size / 100

                cum_size.append(size + trade_profit)
                if compounding:
                    size = size + trade_profit
                pnl.append(trade_profit)
                sls.append(trade_profit)
                print(f"sl executed @ {close} -> gain {gain}% -> profit {trade_profit} $")
                trade_opened = False
                print("-" * 100)


print("-" * 100)
print("-" * 100)
print(f"strategy on {ticker} on {time_frame} timespan => {start_date} -> {end_date}")
print(f"strategy $ pnl is {round(sum(pnl), 2)}")
if compounding:
    print(f"strategy % pnl is {round((cum_size[-1] / start_size - 1) * 100, 2)}")
    print(f"W/L ratio: {round((len(tps)/(len(sls)+len(tps)))*100, 2)}%")
    print(f"average profit {round(np.average(tps), 2)}")
    print(f"average loss {round(np.average(sls), 2)}")
else:
    print(f"strategy % pnl is {round((sum(pnl) / start_size - 1) * 100, 2)}")
    print(f"W/L ratio: {len(tps) / len(sls)}")
    print(f"average profit {round(np.average(tps), 2)}")
    print(f"average loss {round(np.average(sls), 2)}")


cum_sum = []
cum = 0
for profit in pnl:
    cum += profit
    cum_sum.append(cum)


plt.plot(cum_sum)
plt.title(f"strategy $ return {start_date} -> {end_date}")
plt.grid(alpha=0.3)
plt.show()

plt.plot(cum_size)
plt.title(f"strategy cum size")
plt.grid(alpha=0.3)
plt.show()

x = [i for i in range(len(pnl))]
plt.title("pnl histogram")
plt.bar(x, pnl, width=0.3)
plt.show()