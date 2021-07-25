#######################
# Author: slurpxbt
#######################
import binance_candle_data as bcd
import datetime
from pathlib import Path
import pickle
import os
import time


def load_and_update_tickers(tickers):

    root = Path(".")    # set root for filepath to current directory

    # start date
    s_day = 21
    s_month = 8
    s_year = 2017

    startDate = datetime.datetime(s_year, s_month, s_day)
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)  # 5----1
    endDate = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 22, 0, 0)   # 14----22


    # TODO: Change only next 2 lines nothing else
    candle_intervals = ["1min", "3min", "5min", "15min", "30min", "1h", "4h", "6h", "12h","1D"]

    # load/update tickers|
    load_update_tickers = True                             

    # if we want to load or update tickers
    if load_update_tickers == True:
        
        # check if directory for data exists -> if not it creates it
        if os.path.isdir(f"{root}/data") == False:
            os.mkdir(f"{root}/data")
        else:
            pass
        
        # load or update every ticker in tickers list
        for ticker in tickers:
            time.sleep(1)
            for candle_interval in candle_intervals:
                start = time.time()
                # data path where we want to have data
                data_path = f"{root}/data/{ticker}_{candle_interval}.p"

                # checks if file with ticker data already exists
                if os.path.exists(data_path) == False:  
                    # get data
                    daily_data = bcd.get_candle_data(time_interval=candle_interval,symbol=ticker, start_date=startDate, end_date=endDate)

                    #  dumps downloaded data into file
                    pickle.dump(daily_data, open(data_path,"wb"))
                    print(f"data load for {ticker} {candle_interval} took", round(time.time() - start, 2), "s")

                else:
                    bcd.update_candle_data(data_path, ticker)
                    print(f"data update for {ticker} {candle_interval} took", round(time.time() - start, 2), "s")

    else:
        pass


tickers = ["BTCUSDT", "ETHUSDT"]

load_and_update_tickers(tickers)