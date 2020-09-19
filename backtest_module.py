#######################
# Author: slurpxbt
#######################
from pathlib import Path
import pandas as pd
import pickle

# pandas display, pycharm otherwise doesn't display all columns
pd.set_option('display.max_columns', 40)
desired_width = 500
pd.set_option('display.width', desired_width)
# ------------------------------------------------------------

root = Path(".")
ticker = "BTCUSDT"
time_frame = "1D"


def get_data_by_date(ticker, time_frame, start_date, end_date):

    file_path = f"{root}/data/{ticker}_{time_frame}.p"
    data = pickle.load(open(file_path, "rb"))
    data_df = pd.DataFrame(data)
    print(data_df)




get_data_by_date(ticker, time_frame, 0, 0)