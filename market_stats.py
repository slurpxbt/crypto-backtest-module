#######################
# Author: slurpxbt
#######################
import binance_candle_data as bcd
from pathlib import Path
import pandas as pd
import datetime
import pickle

# pandas display, pycharm otherwise doesn't display all columns
pd.set_option('display.max_columns', 100)
desired_width = 500
pd.set_option('display.width', desired_width)
# ----------------------------------------------------------

root = Path(".")




def market_weekly_H_L_stats(start_date, end_date, filepath, ticker):

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

        # if len(week_max) > 0 and len(week_min) > 0:
        #     print("year", week_max[0].isocalendar()[0])
        #     print("week", week_max[0].isocalendar()[1])
        #     print("high price", week_max[2],"day", week_max[0].isocalendar()[2])
        #     print("low price", week_min[3], "day", week_min[0].isocalendar()[2])
        #     print("-"*100)

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

    #print(sum_max)
    #print(sum_min)

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


ticker = "BTCUSDT"
time_frame = "1D"
file_path = f"{root}/data/{ticker}_{time_frame}.p"
start_date = datetime.datetime(2020, 5, 1)
end_date = datetime.datetime(2020, 9, 1)

market_weekly_H_L_stats(start_date, end_date, file_path, ticker)

print("-"*100)

ticker = "ETHUSDT"
file_path = f"{root}/data/{ticker}_{time_frame}.p"
market_weekly_H_L_stats(start_date, end_date, file_path, ticker)