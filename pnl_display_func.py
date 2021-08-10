import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


def drawdown_calc(cum_sizes):
    """cum_sizes = list of portfolio cumulative size over time"""
    max_acc_val = cum_sizes[0]
    drawdown_timer = 0  # number of trades
    drawdowns = []  # stored length of drawdowns
    drawdown_pcts = []

    drawdown = 0  # %
    for i in range(len(cum_sizes)):
        size = cum_sizes[i]

        if size > max_acc_val:
            max_acc_val = size
            drawdowns.append(drawdown_timer)
            drawdown_timer = 0
        else:

            drawdown = (1 - (size / max_acc_val)) * 100  # %
            drawdown_pcts.append(round(drawdown, 2))

            drawdown_timer += 1
            # print(size, drawdown_timer)

    drawdowns.append(drawdown_timer)

    print(f"max drawdown: {max(drawdown_pcts)} %")
    if len(drawdowns) > 0:
        print(f"max drawdown lenght: {max(drawdowns)} trades")
    else:
        print(f"drawdown from the start to end of backtest")


def display_pnl(pct_returns:list,coin_amount:list, usd_amount:list, coin_prices:list, strategy_type:str, ticker:str, start_date:dt, end_date:dt):
    """
    Function that display PNL stats of the strategy
    """

    usd_pct_gain = round(((usd_amount[-1]) / (usd_amount[0]) - 1) * 100, 2)
    coin_pct_gain = round((coin_amount[-1]/coin_amount[0]-1)*100,2)

    start_size =usd_amount[0]
    size = start_size
    for ret in pct_returns:
        size = size + (size * (ret/100))
    usd_margin_equivalent_pct_gain = round((size / start_size - 1) * 100, 2)
    buy_hold = round((coin_prices[-1]/coin_prices[0]-1)*100,2)

    wins = []
    losses = []
    for ret in pct_returns:
        if ret >= 0:
            wins.append(ret)
        else:
            losses.append(ret)

    w_l_ratio = round(len(wins) / len(pct_returns) * 100, 2)

    avg_pct_gain = round(np.average(pct_returns), 2)
    profit_factor = round(sum(wins)/sum(losses), 2)

    print("*" * 100)
    print("*" * 100)
    print(f"COIN: {ticker}")
    print(f"strat type: {strategy_type}")
    print("-" * 100)
    print(f"start: {start_date.date()} || end: {end_date.date()}")
    print("-" * 100)
    print(f"pure % return on usd collat: {usd_margin_equivalent_pct_gain} %")
    print(f"coin return: {coin_pct_gain} % || start: {coin_amount[0]} {ticker[:-4]} {round(coin_amount[0] * coin_prices[0])} $ || end: {coin_amount[-1]} {ticker[-4:]} {round(coin_amount[-1] * coin_prices[-1])} $ || usd % gain: {usd_pct_gain} %")
    print(f"w/l ratio: {w_l_ratio} %")
    print("-" * 100)
    print(f"buy and hold ret: {buy_hold} %")
    print(f"performance against buy & hold: {round(coin_pct_gain/buy_hold, 2)}")
    print(f"avg. pct. gain: {avg_pct_gain} %")
    print(f"profit factor: {profit_factor}")
    print("-" * 100)
    # coin DD
    print("COIN-m DD stats")
    drawdown_calc(coin_amount)
    print("-" * 100)
    # usd DD
    print("USD-m DD stats")
    drawdown_calc(usd_amount)
    print("*" * 100)
    print("*" * 100)

    fig, ax1 = plt.subplots()
    plt.title(f"{ticker[:-4]} || start: {start_date.date()} -> end: {end_date.date()} || type: {strategy_type} || usd_ret: {usd_pct_gain} % || coin_ret: {coin_pct_gain} %")
    x = range(len(usd_amount))

    color = 'tab:blue'
    ax1.set_xlabel('trade no.')
    ax1.set_ylabel('usd balance', color=color)
    ax1.plot(x, usd_amount, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:orange'
    ax2.set_ylabel('coin balance', color=color)
    ax2.plot(x, coin_amount, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.show()




