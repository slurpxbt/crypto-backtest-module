#######################
# Author: slurpxbt
#######################
import binance_candle_data as bcd
from pathlib import Path
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import pickle
import numpy as np

# pandas display, pycharm otherwise doesn't display all columns
pd.set_option('display.max_columns', 100)
desired_width = 500
pd.set_option('display.width', desired_width)
# ----------------------------------------------------------

root = Path(".")

def market_daily_H_L_distribution(start_date, end_date, file_path, ticker):

    # data format [open_time, open, high, low, close, volume, close_time, number_of_trades]
    data = bcd.get_data_by_date(start_date, end_date, file_path).values.tolist()
    # calculates how many years of data we have
    year_no = end_date.year - start_date.year


    if year_no != 0:
        # if year difference is one create values for both years,
        years = range(start_date.year, start_date.year + year_no + 1, 1)
    else:
        # if year difference is 0, only value is current year
        years = [end_date.year]



    weekly_data = []

    for year in years:  # for each year and each week compare data
        for i in range(1, 53,1):
            week = []
            for j in range(len(data)):
                # if year and week are the as in for loops append daily data to week list
                if data[j][0].isocalendar()[1] == i and data[j][0].isocalendar()[0] == year:
                    week.append(data[j])

            # append week data to weekly data list
            weekly_data.append(week)

    max_days = []
    min_days = []
    for week in range(len(weekly_data)):
        week_max_prc = 0
        week_min_prc = 10000000
        week_max = []
        week_min = []
        # for each day in weekly data
        for day in weekly_data[week]:
            #print(day)
            if day[2] > week_max_prc:   # if price is higher than previous max price
                week_max = day
                week_max_prc = day[2]   # set new high price to current price

            if day[3] < week_min_prc:   # if price is lower than previous lowest price
                week_min = day
                week_min_prc = day[3]   # set new low price to current price


        max_days.append(week_max)
        min_days.append(week_min)

    days = range(1,8,1)
    days_max = []
    days_min = []
    for day in days:
        day_tmp = []
        for i in max_days:
            if len(i) > 0:
                if i[0].isocalendar()[2] == day:
                    day_tmp.append(i)

        days_max.append(day_tmp)

    for day in days:
        day_tmp = []
        for i in min_days:
            if len(i) > 0:
                if i[0].isocalendar()[2] == day:
                    day_tmp.append(i)
        days_min.append(day_tmp)

    sum_max = 0
    sum_min = 0
    for i in days_max:
        sum_max = sum_max + len(i)

    for i in days_min:
        sum_min = sum_min + len(i)


    day_dict = {0:"mon", 1:"tue", 2:"wed", 3:"thu", 4:"fri", 5:"sat", 6:"sun"}

    print("timespan=", start_date.date(), "=>", end_date.date(), "-> " ,ticker)

    for index in range(len(days_max)):
        day = day_dict[index]
        pct_chance_high = (len(days_max[index])/sum_max)*100
        print(f"chance of high on {day} is {round(pct_chance_high, 2)}%")

    print("-" * 100)
    for index in range(len(days_min)):
        day = day_dict[index]
        pct_chance_high = (len(days_min[index]) / sum_max) * 100
        print(f"chance of low on {day} is {round(pct_chance_high, 2)}%")


def hourly_H_L_distribution(start_date, end_date, file_path, ticker):

    # data format [open_time, open, high, low, close, volume, close_time, number_of_trades]
    data = bcd.get_data_by_date(start_date, end_date, file_path).values.tolist()
    # calculates how many years of data we have
    year_no = end_date.year - start_date.year


    if year_no != 0:
        # if year difference is one create values for both years,
        years = range(start_date.year, start_date.year + year_no + 1, 1)
    else:
        # if year difference is 0, only value is current year
        years = [end_date.year]



    weekly_data = []

    for year in years:  # for each year and each week and each day of the week compare data
        for i in range(1, 53,1):
            week = []
            for day in range(1,8,1):
                tmp_day = []
                for j in range(len(data)):
                    # if year and week are the as in for loops append daily data to week list
                    if data[j][0].isocalendar()[1] == i and data[j][0].isocalendar()[0] == year and data[j][0].isocalendar()[2] == day:
                        tmp_day.append(data[j])     # appends data to current day list

                week.append(tmp_day)    # appends day to the week

            # append week data to weekly data list
            weekly_data.append(week)

    weekday_highs = [[], [], [], [], [], [], []]
    weekday_lows = [[], [], [], [], [], [], []]
    for week in weekly_data:
        for day in week:
            daily_high = 0
            daily_low = 1000000

            daily_high_tmp = []
            daily_low_tmp = []

            for trade in day:
                if daily_high < trade[2]:   # finds the daily high  trade[2]=high
                    daily_high = trade[2]
                    daily_high_tmp = trade

                if daily_low > trade[3]:    # finds the daily low  trade[3]=low
                    daily_low = trade[3]
                    daily_low_tmp = trade

            if len(daily_high_tmp) > 0 and len(daily_low_tmp) > 0:  # if list is not empty

                weekday_highs[daily_high_tmp[0].isocalendar()[2] - 1].append(daily_high_tmp)    # appends trades that contains high for specific day at it's day index
                weekday_lows[daily_low_tmp[0].isocalendar()[2]-1].append(daily_low_tmp)         # appends trades that contains low for specific day at it's day index

    # empty list for data that will be used for stats
    weekday_high_stats = [[], [], [], [], [], [], []]
    weekday_low_stats = [[], [], [], [], [], [], []]


    counter = 1
    for day in weekday_highs:
        # for each day create list of 24h for trades
        daily_highs = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for high in day:
            daily_highs[high[0].hour].append(high)  # appends trade that contains high to it's corresponding hour in daily_highs list

        weekday_high_stats[counter-1].append(daily_highs)   # appends day to the week
        counter += 1


    counter = 1
    for day in weekday_lows:
        daily_lows = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for low in day:
            daily_lows[low[0].hour].append(low)  # appends trade that contains low to it's corresponding hour in daily_lows list

        weekday_low_stats[counter-1].append(daily_lows) # appends day to the week
        counter += 1



    day_dict = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}

    #HIGHS
    for day in range(len(weekday_high_stats)):
        daily_sum = 0
        for hour in weekday_high_stats[day]:
            for trades in hour:
                daily_sum += len(trades)    # calculates sum for easier % calculation

        print("-" * 100)
        print("timespan=", start_date.date(), "->", end_date.date(), "ticker=", ticker)
        h_count = 0
        for hour in range(len(weekday_high_stats[day])):
            for trades in weekday_high_stats[day][hour]:
                len_trd = len(trades)

                current_day = day_dict[day]
                chance_of_high = round((len_trd/daily_sum)*100, 2)

                print(f"chance of high on {current_day} at hour {h_count} is:", chance_of_high, "%")
                h_count += 1

                # visualization
                text_str = f"{chance_of_high}%"
                plt.bar(h_count-1, chance_of_high, width=0.5)
                plt.text(h_count - 1.25, chance_of_high + 0.25,text_str)

            plt.title(f"chance of high on {current_day} for {ticker} in timespan {start_date.date()} -> {end_date.date()}")
            plt.xlabel("hour")
            plt.ylabel("%")
            plt.xticks(range(0,24,1))
            plt.grid(alpha=0.3)
            figMan = plt.get_current_fig_manager()
            figMan.window.showMaximized()
            plt.show()

            print("-"*100)


    # LOWS
    for day in range(len(weekday_low_stats)):
        daily_sum = 0
        for hour in weekday_low_stats[day]:
            for trades in hour:
                daily_sum += len(trades)     # calculates sum for easier % calculation

        print("-" * 100)
        print("timespan=", start_date.date(), "->", end_date.date(), "ticker=", ticker)
        h_count = 0
        for hour in range(len(weekday_low_stats[day])):
            for trades in weekday_low_stats[day][hour]:
                len_trd = len(trades)

                current_day = day_dict[day]
                chance_of_low = round((len_trd / daily_sum) * 100, 2)

                print(f"chance of low on {current_day} at hour {h_count} is:", chance_of_low, "%")
                h_count += 1
                # visualization
                text_str = f"{chance_of_low}%"
                plt.bar(h_count-1, chance_of_low, width=0.5)
                plt.text(h_count - 1.25, chance_of_low + 0.25, text_str)

            plt.title(f"chance of low on {current_day} for {ticker} in timespan {start_date.date()} -> {end_date.date()}")
            plt.xlabel("hour")
            plt.ylabel("%")
            plt.xticks(range(0, 24, 1))
            plt.grid(alpha=0.3)
            figMan = plt.get_current_fig_manager()
            figMan.window.showMaximized()
            plt.show()

    print("-" * 100)


def candle_interval_stats(file_path, candle_range, ticker, time_frame):
    # format = [open_time, open, high, low, close, volume, close_time, number_of_trades]
    ticker_data = bcd.get_data_by_date(start_date, end_date, file_path)
    candle_data = ticker_data.values.tolist()

    # print(ticker_data)
    #
    # print(len(candle_data))
    # print("-"* 100)

    avg = []            # list for storing candle close values
    candle_gain = []    # list for storing candle gain values
    pct_change = []     # list for storing candle pct gains
    ranges = []         # list for storing candle ranges
    for i in candle_data:

        if len(avg) < candle_range:
            avg.append(i[4])            # appends candle closes

            if len(avg) >= 2:   # if there are atleast 2 values in list

                #print(f"avg len={len(avg)} ||| avg price of last {len(avg)} candles is {round(sum(avg) / len(avg), 2)} -> current price={avg[-1]} ||| % change [max/min] of last {len(avg)} candles=>{round((max(avg) / min(avg) - 1) * 100, 2)} ||| max={max(avg)} - min={min(avg)} ||| last candle gain/loss {round((avg[-1] / avg[-2] - 1) * 100, 2)}")
                candle_gain.append(round((avg[-1] / avg[-2] - 1) * 100, 3))     # append last candle gain

            else:
                #print(f"avg len={len(avg)} ||| avg price of last {len(avg)} candles is {round(sum(avg) / len(avg), 2)} -> current price={avg[-1]}  ||| % change [max/min] of last {len(avg)} candles=>{round((max(avg) / min(avg) - 1) * 100, 2)} ||| max={max(avg)} - min={min(avg)}")
                pass

        if len(avg) == candle_range:        # if candle range list is full
            pct_change.append(round((max(avg) / min(avg) - 1) * 100, 2))    # append this candle range pct range(max/min)
            ranges.append(max(avg) - min(avg))                              # append this candle range max-min
            candle_gain = []                                                # prepare list for next candle range gains
            avg = []                                                        # prepare list for next candle closes

    print("-" * 100)
    print(f"{ticker} stats")
    print(f"avg % change of {candle_range} {time_frame} candles in timespan {start_date.date()} -> {end_date.date()} =>{round(np.average(pct_change), 3)} %")
    print(f"avg range of {candle_range} {time_frame} candles in timespan {start_date.date()} -> {end_date.date()} =>{round(np.average(ranges), 2)} $")
    print("-" * 100)


def std2_prob_movingWindow(file_path, candle_range, time_frame):

    # format = [open_time, open, high, low, close, volume, close_time, number_of_trades]
    ticker_data = bcd.get_data_by_date(start_date, end_date, file_path)
    candle_data = ticker_data.values.tolist()

    candle_gain = []
    avg = []
    std2 = []
    double_std2 = []
    same_dir_std2 = []

    for index in range(len(candle_data)):
        candle = candle_data[index]         # store current candle data

        if len(avg) < candle_range:
            # index 4 is candle close
            avg.append(candle[4])       # append candle close

            if len(avg) >= 2:
                candle_gain.append(round((avg[-1] / avg[-2] - 1) * 100, 3))

        if len(avg) == candle_range:
            std = round(np.std(candle_gain), 4)     # calculates std for candles gains

            # print("candle gains=>", candle_gain)
            # print("candle gain 1std=", std, "candle gain 2std=", 2*std)
            # print("candle gain -1std=", std * (-1), "candle gain -2std=", (2 * std) * (-1))
            # print("-"*50, "current price", candle[4])

            if index+1 < len(candle_data) and index+2 < len(candle_data):                   # check for the last candle in dataset
                if abs(round((candle_data[index+1][4]/candle[4]-1)*100, 2)) >= (std * 2):    # if candle gain is bigger thant 2std

                    # print("-"*200)
                    # print(f"current price -> {candle[4]}, next candle -> {candle_data[index+1][4]}")
                    # print(f"move with 2std or more -> % change {round((candle_data[index+1][4]/candle[4]-1)*100, 3)} %")
                    # print("-" * 200)
                    std2.append(1)      # this list is mostly used just for length that's why I append 1

                    if abs(round((candle_data[index+2][4]/candle_data[index+1][4]-1)*100, 2)) >= (std * 2):  # if 2nd candle i a row has gain of more than 2std
                        double_std2.append(1)   # this list is mostly used just for length that's why I append 1

                        # print("2nd 2std MOVE IN A ROW" ,"*" * 200)
                        # print(f"move with 2std or more -> % change {round((candle_data[index + 1][4] / candle[4] - 1) * 100, 3)} %")
                        # print(f"current price -> {candle[4]}, next candle -> {candle_data[index + 1][4]} -> next candle -> {candle_data[index + 2][4]}")
                        # print("*" * 200)

                        if round((candle_data[index+2][4]/candle[4]-1)*100, 2) >= 0 and round((candle_data[index+1][4]/candle[4]-1)*100, 2) >= 0:   # if candle gain is positive checks if next candle is also positive
                            same_dir_std2.append(1)     # this list is mostly used just for length that's why I append 1

                        elif round((candle_data[index+2][4]/candle[4]-1)*100, 2) < 0 and round((candle_data[index+1][4]/candle[4]-1)*100, 2) < 0:   # if candle gain is negative checks if next candle is also negative
                            same_dir_std2.append(1)     # this list is mostly used just for length that's why I append 1

            # removes first element since this is moving window
            candle_gain.pop(0)
            avg.pop(0)

    # results
    print("-" * 100)
    print(f"timespan {start_date.date()} -> {end_date.date()}")
    print(f"chance of 2nd 2std move when first 2std happens for {time_frame} and candle range {candle_range} is {round((len(double_std2)/len(std2))*100, 2)} %")
    print(f"chance of 2nd 2std move being in the same direction as first one is {round(len(same_dir_std2)/len(double_std2)*100, 2)} %")
    print("-" * 100)


def triple_sdt1_prob_movingWindow(file_path, candle_range, time_frame):

    # format = [open_time, open, high, low, close, volume, close_time, number_of_trades]
    ticker_data = bcd.get_data_by_date(start_date, end_date, file_path)
    candle_data = ticker_data.values.tolist()

    candle_gain = []
    avg = []

    std1 = []
    double_std1 = []
    same_dir_std1 = []
    triple_std1 = []
    double_same_dir_std1 = []

    for index in range(len(candle_data)):

        candle = candle_data[index]

        if len(avg) < candle_range:
            # index 4 is candle close
            avg.append(candle[4])

            if len(avg) >= 2:
                candle_gain.append(round((avg[-1] / avg[-2] - 1) * 100, 3))

        if len(avg) == candle_range:

            std = round(np.std(candle_gain), 4)     # calculates std of candle gains

            # print("candle gains=>", candle_gain)
            # print("candle gain 1std=", std, "candle gain 2std=", 2*std)
            # print("candle gain -1std=", std * (-1), "candle gain -2std=", (2 * std) * (-1))
            # print("-"*50, "current price", candle[4])

            if index+1 < len(candle_data) and index+2 < len(candle_data) and index+3 < len(candle_data):    # check for last candles in dataset
                # triple std1 move
                if abs(round((candle_data[index + 1][4] / candle[4] - 1) * 100, 2)) >= std:     # if candle gain is bigger than 1std

                    # print("-" * 200)
                    # print(f"current price -> {candle[4]}, next candle -> {candle_data[index + 1][4]}")
                    # print(f"move with 1std or more -> % change {round((candle_data[index + 1][4] / candle[4] - 1) * 100, 3)} %")
                    # print("-" * 200)

                    std1.append(1)  # this list is mostly used just for length that's why I append 1

                    if abs(round((candle_data[index + 2][4] / candle_data[index + 1][4] - 1) * 100, 2)) >= std:     # if 2nd candle also has bigger gain than 1std
                        double_std1.append(1)   # this list is mostly used just for length that's why I append 1

                        # print("2nd 1std MOVE IN A ROW", "*" * 200)
                        # print(f"move with 1std or more -> % change {round((candle_data[index + 1][4] / candle[4] - 1) * 100, 3)} %")
                        # print(f"current price -> {candle[4]}, next candle -> {candle_data[index + 1][4]} -> next candle -> {candle_data[index + 2][4]}")
                        # print("*" * 200)

                        # check if 1std moves are in the same direction
                        if round((candle_data[index + 2][4] / candle[4] - 1) * 100, 2) >= 0 and round((candle_data[index + 1][4] / candle[4] - 1) * 100, 2) >= 0:
                            same_dir_std1.append(1)     # this list is mostly used just for length that's why I append 1
                        elif round((candle_data[index + 2][4] / candle[4] - 1) * 100, 2) < 0 and round((candle_data[index + 1][4] / candle[4] - 1) * 100, 2) < 0:
                            same_dir_std1.append(1)     # this list is mostly used just for length that's why I append 1

                        if abs(round((candle_data[index + 3][4] / candle_data[index + 2][4] - 1) * 100, 2)) >= std:     # check if third candle is 1std move
                            triple_std1.append(1)
                            # print("3rd 1std MOVE IN A ROW", "*_*" * 100)
                            # print(f"move with 1std or more -> % change {round((candle_data[index + 1][4] / candle[4] - 1) * 100, 3)} %")
                            # print(f"current price -> {candle[4]}, next candle -> {candle_data[index + 1][4]} -> next candle -> {candle_data[index + 2][4]}")
                            # print("*_*" * 100)

                            # check if 1std moves are in the same direction
                            if round((candle_data[index + 3][4] / candle[4] - 1) * 100, 2) >= 0 and round((candle_data[index + 2][4] / candle[4] - 1) * 100, 2) >= 0:
                                double_same_dir_std1.append(1)      # this list is mostly used just for length that's why I append 1
                            elif round((candle_data[index + 3][4] / candle[4] - 1) * 100, 2) < 0 and round((candle_data[index + 2][4] / candle[4] - 1) * 100, 2) < 0:
                                double_same_dir_std1.append(1)      # this list is mostly used just for length that's why I append 1

            # removes first element since this is moving window
            candle_gain.pop(0)
            avg.pop(0)



    print("-" * 100)
    print(f"timespan {start_date.date()} -> {end_date.date()}")
    print(f"chance of 2nd 1std move when first 1std happens for {time_frame} and candle range {candle_range} is {round((len(double_std1)/len(std1))*100, 2)} %")
    print(f"chance of 2nd 1std move being in the same direction as first one is {round(len(same_dir_std1)/len(double_std1)*100, 2)} %")
    print(f"chance of 3rd 1std move when 2nd 1std happens for {time_frame} and candle range {candle_range} is {round((len(triple_std1) / len(double_std1)) * 100, 2)} %")
    print(f"chance of 3nd 1std move being in the same direction as 2nd one is {round(len(double_same_dir_std1) / len(triple_std1) * 100, 2)} %")
    print("-" * 100)





start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020, 9, 20)

tickers = ["BTCUSDT", "ETHUSDT"]
time_frames = ["1h"]
for ticker in tickers:
    for time_frame in time_frames:
        candle_range = 30
        file_path = f"{root}/data/{ticker}_{time_frame}.p"

        market_daily_H_L_distribution(start_date, end_date, file_path, ticker)
        hourly_H_L_distribution(start_date, end_date, file_path, ticker)
        candle_interval_stats(file_path, candle_range, ticker, time_frame)
        std2_prob_movingWindow(file_path, candle_range, time_frame)
        triple_sdt1_prob_movingWindow(file_path, candle_range, time_frame)


