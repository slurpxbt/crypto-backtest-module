from binance.client import Client
import pandas as pd
import pickle
import datetime
import time
from pathlib import Path

def get_candle_data(symbol="BTCUSDT", time_interval="1D", start_date=datetime.datetime(2020,1,1) , end_date=None):
    """
        this function cannot get binance futures data\n
        it should be used only the first time, then you should use update_candle_data() function instead\n
        params:
            symbol       : string -> coin ticker
            time_interval: string -> ["1min", "3min", "5min", "15min", "30min", "1h", "4h", "6h", "1D"]
            start_date   : datetime.datetime -> from when to collect data
            end_date     : datetime.datetime -> until when we want to collect data
    """
    # 
    
    # checks if end date is before start date
    if end_date != None:
        if start_date > end_date and end_date:
            end_date = None
        else:
            pass
    else:
        pass
    
    # client initialization
    client = Client()
    
    # checks the selected time interval
    if time_interval == "1min":
        kline_interval = Client.KLINE_INTERVAL_1MINUTE
    elif time_interval == "3min":
        kline_interval = Client.KLINE_INTERVAL_3MINUTE
    elif time_interval == "5min":
        kline_interval = Client.KLINE_INTERVAL_5MINUTE
    elif time_interval == "15min":
        kline_interval = Client.KLINE_INTERVAL_15MINUTE
    elif time_interval == "30min":
        kline_interval = Client.KLINE_INTERVAL_30MINUTE
    elif time_interval == "1h":
        kline_interval = Client.KLINE_INTERVAL_1HOUR
    elif time_interval == "4h":
        kline_interval = Client.KLINE_INTERVAL_4HOUR
    elif time_interval == "6h":
        kline_interval = Client.KLINE_INTERVAL_6HOUR
    elif time_interval == "1D":
        kline_interval = Client.KLINE_INTERVAL_1DAY


    # returns = [open_time, open, high, low, close, volumem, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume]
    candle_data  = client.get_historical_klines(symbol=symbol, interval=kline_interval, start_str=start_date.strftime("%Y/%d/%m"))
    
    # creates dataframe from list of lists
    candle_data_df = pd.DataFrame(candle_data, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])

    # converting datatypes
    candle_data_df["open_time"] = pd.to_datetime(candle_data_df["open_time"], unit='ms')    # time conversion from timestamp to datetime
    candle_data_df["open"] = pd.to_numeric(candle_data_df["open"])                          # string to numeric
    candle_data_df["high"] = pd.to_numeric(candle_data_df["high"])                          # string to numeric
    candle_data_df["low"] = pd.to_numeric(candle_data_df["low"])                            # string to numeric
    candle_data_df["close"] = pd.to_numeric(candle_data_df["close"])                        # string to numeric
    candle_data_df["volume"] = pd.to_numeric(candle_data_df["volume"]).round(2) 	        # rounds the float
    candle_data_df["close_time"] = pd.to_datetime(candle_data_df["close_time"], unit='ms') + datetime.timedelta(milliseconds=1) # time conversion from timestamp to datetime ==> adds 1 milisecond so close is at 24:00:00.000 -> data gives you 23:59:59.999
    
    # column drops
    candle_data_df.drop("quote_asset_volume", 1, inplace=True)                              
    candle_data_df.drop("taker_buy_base_asset_volume", 1, inplace=True)
    candle_data_df.drop("taker_buy_quote_asset_volume", 1, inplace=True)
    candle_data_df.drop("ignore", 1, inplace=True)

    # row drops
    if end_date != None:
        candle_data_df.drop(candle_data_df[candle_data_df["open_time"] > end_date].index, inplace=True) # drops rows which are after the specified end date
    else:
        pass

    return candle_data_df


def update_candle_data(filepath, ticker,update_date=datetime.datetime.today(), info=True):
    """
        params:
            filepath   : string - path to the file 
            ticker     : string - ticker name 
            update_date: datetime.datetime - date to where we want to update our data
    """
    # pickle data streams are self contained
    # you need to load as long as there are data streams and get an error
    # this script assumes in the pickle file data is ordered and without duplicates

    root = Path(".")                                            # set root for filepath to current directory
    intervals = ["1min", "3min", "5min", "15min", "30min", "1h", "4h", "6h", "1D"]      # possible time intervals


    # checks the file name and finds the data time_frame
    for i in intervals:
        if i in filepath:
            time_frame = i
    
    # loads data from file
    data = pickle.load(open(filepath, "rb"))

 
    last_data_point_date = data.loc[data.index[-1]]["open_time"].date()                 # checks date of last data point
    missing_data = update_date.date() - last_data_point_date                            # check many days of data is missing
    new_date = data.loc[data.index[-1]]["open_time"].date() + datetime.timedelta(1)     # set the date from when we update data => 1 day + our last data entry
    
    # sets date into right format 
    startDate = datetime.datetime(new_date.year, new_date.month, new_date.day)


    # updates data if there is atleast 1 day of missing data
    if missing_data.days != 0:
        print(f"updating missing days of data {missing_data.days}")    
        update = get_candle_data(ticker, time_frame, startDate, update_date) # gets missing data
        data = data.append(update, ignore_index=True)           # appends new data to previously loaded 
        data.reset_index(drop=True)                             # reindexes dataframe because missing data indexes start with 1 again

        pickle.dump(data, open(filepath, "wb")) 
                             # check if this works
    else:
        print(f"no mising data for {ticker}")




###########################################################################################################
# mainj function is meant just for testing purposes when developing new functions and testing current ones
###########################################################################################################

def main():

    root = Path(".")    # set root for filepath to current directory

    # start date
    s_day = 21
    s_month = 12
    s_year = 2018
    startDate = datetime.datetime(s_year, s_month , s_day)

    candle_interval = "1D"                          # [15min, 30min, 1h, 4h, 6h, 1D]
    ticker = "BTCUSDT"

    # end date
    e_day = 21
    e_month = 1
    e_year = 2019
    endDate = datetime.datetime(e_year, e_month, e_day)
    
    # ----------------------------------------------------------------------------------------------------------------------
    # data path where we want to have data
    data_path = f"{root}/data_test/{ticker}_{candle_interval}.p"     

    # get data
    daily_data = get_candle_data(time_interval=candle_interval,symbol=ticker, start_date=startDate, end_date=endDate)

    #  dumps downloaded data into file
    pickle.dump(daily_data, open(data_path,"wb"))     # "ab" -> appends to the end of the file if it exists, if not it creates a new file

    print("data loaded------------------------------")
    
    up_date = datetime.datetime(2020,7,31)                      # date to where we want to update data
    update_candle_data(data_path, ticker, update_date=up_date)  # update data function call

    updated_data = pickle.load(open(data_path, "rb") )
    
    # ------------------------------------------------------------------------------------------------------------------------


    for index in range(len(updated_data)):

        row = updated_data.loc[index].tolist()
        open_date = row[0]
        close_date = row[6]
        open_ = round(float(row[1]), 2)
        high = round(float(row[2]), 2)
        low = round(float(row[3]), 2)
        close = round(float(row[4]), 2)
        volume = round(float(row[5]), 2) # BTC volume
        no_trades = row[7]

        print("open_date:", open_date, "|open:", open_, "|high:", high, "|low:", low, "|close:", close, "|close_date:", close_date, "number of trades", no_trades)

if __name__ == "__main__":
    main()
























