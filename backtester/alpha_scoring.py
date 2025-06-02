import pandas as pd
import numpy as np
from pandas import Timestamp
from numpy import sqrt

test_log = [{'date': Timestamp('2022-07-21 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 17, 'price': 126.31018399999998, 'atr': 2.872071428571426, 'reason': 'RSI < 25', 'cash_after': 7852.641872}, {'date': Timestamp('2022-09-01 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 17, 'price': 122.788089, 'atr': 2.546785714285712, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 9939.954385000001, 'pnl': -59.87561499999964}, {'date': Timestamp('2022-11-17 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 15, 'price': 117.28716999999999, 'atr': 3.120521428571429, 'reason': 'RSI < 25', 'cash_after': 8180.571835000001}, {'date': Timestamp('2022-12-16 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 15, 'price': 112.74714, 'atr': 2.748214285714284, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 9871.703935000001, 'pnl': -68.10044999999981}, {'date': Timestamp('2023-01-27 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 21, 'price': 121.99186999999999, 'atr': 2.277635714285713, 'reason': 'RSI < 25', 'cash_after': 7309.769665000002}, {'date': Timestamp('2023-08-24 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 21, 'price': 148.43142, 'atr': 2.384921428571429, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10426.724485000002, 'pnl': 555.2305500000002}, {'date': Timestamp('2023-08-30 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 21, 'price': 155.23507999999998, 'atr': 2.39902142857143, 'reason': 'RSI < 25', 'cash_after': 7166.682805000002}, {'date': Timestamp('2023-09-22 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 21, 'price': 147.10275, 'atr': 1.9735928571428576, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10255.735555000003, 'pnl': -170.77892999999992}, {'date': Timestamp('2023-10-18 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 20, 'price': 149.63949, 'atr': 2.5019999999999993, 'reason': 'RSI < 25', 'cash_after': 7262.845755000003}, {'date': Timestamp('2023-10-19 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 20, 'price': 147.92193, 'atr': 2.5297428571428577, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10221.184355000003, 'pnl': -34.351199999999835}, {'date': Timestamp('2023-11-09 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 21, 'price': 152.44228999999999, 'atr': 2.325185714285717, 'reason': 'RSI < 25', 'cash_after': 7019.7912650000035}, {'date': Timestamp('2024-04-18 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 21, 'price': 174.08574, 'atr': 2.8580428571428507, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10675.486805000004, 'pnl': 454.51245000000006}, {'date': Timestamp('2024-05-07 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 18, 'price': 181.37118999999998, 'atr': 2.8585785714285743, 'reason': 'RSI < 25', 'cash_after': 7410.715385000004}, {'date': Timestamp('2024-07-30 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 18, 'price': 188.10171, 'atr': 3.9034571428571416, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10796.456165000003, 'pnl': 121.14936000000023}, {'date': Timestamp('2024-08-22 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 12, 'price': 195.62543, 'atr': 4.175314285714287, 'reason': 'RSI < 25', 'cash_after': 8448.891005000003}, {'date': Timestamp('2024-09-06 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 12, 'price': 184.5153, 'atr': 3.4520142857142884, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10663.014605000004, 'pnl': -133.32155999999998}, {'date': Timestamp('2024-09-13 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 14, 'price': 195.82562999999996, 'atr': 3.630092857142862, 'reason': 'RSI < 25', 'cash_after': 7921.385785000004}, {'date': Timestamp('2025-02-27 00:00:00'), 'ticker': 'QQQM', 'type': 'SELL', 'shares': 14, 'price': 205.84395, 'atr': 3.3447357142857124, 'reason': 'EMA down / RSI drop / ATR spike', 'cash_after': 10803.131085000005, 'pnl': 140.25648000000064}, {'date': Timestamp('2025-05-07 00:00:00'), 'ticker': 'QQQM', 'type': 'BUY', 'shares': 12, 'price': 199.21902, 'atr': 4.392578571428572, 'reason': 'RSI < 25', 'cash_after': 8412.442845000005}]
df_test_log = pd.DataFrame(test_log)

def score_alpha_by_ticker(trade_log: pd.DataFrame, initial_cash: float) -> pd.DataFrame:
    """
    Scores each ticker based on trade performance metrics.
    Returns a DataFrame with per-ticker alpha scores.
    """
    if trade_log.empty or "type" not in trade_log.columns:
        return pd.DataFrame()

    trades = trade_log.copy()
    trades["date"] = pd.to_datetime(trades["date"])
    trades.sort_values(by=["date"], inplace=True)

    if "ticker" not in trades.columns:
        trades["ticker"] = "UNKNOWN"

    ticker_stats = []

    for ticker, group in trades.groupby(by=["ticker"]):
        closed_trades = group[group["type"] == "SELL"]
        if closed_trades.empty:
            continue
    
        total_return = closed_trades["pnl"].sum()
        win_rate = (closed_trades["pnl"] > 0).mean()
        avg_return = closed_trades["pnl"].mean()

        # NAV simulation
        nav = initial_cash
        nav_list = []

        for _, row in closed_trades.iterrows():
            nav += row["pnl"]
            nav_list.append(nav)

        nav_series = pd.Series(nav_list, index=closed_trades["date"])

        rolling_max = nav_series.cummax()
        drawdown = rolling_max - nav_series
        max_drawdown = drawdown.max() if not drawdown.empty else 0.0

        daily_returns = closed_trades['pnl'] / initial_cash
        sharpe = np.mean(daily_returns) / np.std(daily_returns) * sqrt(252) if np.std(daily_returns) > 0 else 0

        ticker_stats.append({
            "Ticker": ticker,
            "Total Return ($)": round(total_return, 2),
            "Win Rate": round(win_rate, 3),
            "Avg Return per Trade ($)": round(avg_return, 2),
            "Sharpe Ratio": sharpe,
            "Max Drawdown ($)": round(max_drawdown, 2) # Refine later
        })

    return pd.DataFrame(ticker_stats)

# print(df_test_log)