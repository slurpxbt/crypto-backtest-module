import binance_candle_data as bcd
import datetime
from pathlib import Path
import pickle
import os


def main():

    root = Path(".")    # set root for filepath to current directory

    # start date
    s_day = 1
    s_month = 1
    s_year = 2020
    # binance script date format is american that's why date and month are on reverse place
    startDate = datetime.datetime(s_year,s_day, s_month)

    candle_interval = "1D"                          # [15min, 30min, 1h, 4h, 6h, 1D]
    tickers = ["BTCUSDT", "ETHUSDT"]

    
    load_update_tickers = True                             # load/update tickers
    ticker_update_date = datetime.datetime.today()  # update data until this date

    if load_update_tickers == True:
        
        # check if directory for data exists -> if not it creates it
        if os.path.isdir(f"{root}/data") == False:
            os.mkdir(f"{root}/data")
        else:
            pass

        for ticker in tickers:

            # data path where we want to have data
            data_path = f"{root}/data/{ticker}_{candle_interval}.p"     
            # ----------------------------------------------------------------------------------------------------------------------

            # checks if file with ticker data already exists
            if os.path.exists(data_path) == False:  
                # get data
                daily_data = bcd.get_candle_data(time_interval=candle_interval,symbol=ticker, start_date=startDate)

                #  dumps downloaded data into file
                pickle.dump(daily_data, open(data_path,"wb"))

            else:
                # if ticker file exists this just updates data
                bcd.update_candle_data(data_path, ticker, ticker_update_date)
    else:
        pass



if __name__ == "__main__":
    main()