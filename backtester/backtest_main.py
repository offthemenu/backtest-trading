from datetime import datetime
import pandas as pd
from backtester.data_loader import load_data
from backtester.strategy_runner import generate_signals
from backtester.execution_engine import simulate_trades
from backtester.performance import analyze_performance
from backtester.alpha_scoring import score_alpha_by_ticker
from backtester.visualize import plot_backtest
from pathlib import Path

start_date = (datetime.today().replace(year=datetime.today().year - 2)).strftime("%Y-01-01")
today = datetime.today().strftime("%Y-%m-%d")

ROOT_DIR = Path(__file__).parent.parent

TEST_WATCHLIST = [
    "QQQM",  # US Tech - Nasdaq 100
    "VOO",   # US Broad Market - S&P 500
    "IAU",   # Gold / Inflation hedge
    # "BOTZ",  # Robotics / Innovation
    "XLV",   # Healthcare - Defensive growth
    "VGK",   # Europe ex-UK ETF
    # "IJH",   # US MidCap - S&P MidCap 400
]
net_portfolio_pnl = 0
initial_cash = float(4_700.0)
trade_logs = []

def consolidate_watchlist_data(ticker_list: list, start_date: str, end_date: str): # Improve logic later if you want to backtest on multiple-ticker list
    global TEST_WATCHLIST
    print(f"Creating a consolidated dataframe for all tickers under backtest scope")

    all_data = [] # List will collect each ticker's dataframe

    for ticker in ticker_list:
        # Load historical data
        df = load_data(ticker, start_date, end_date)
        all_data.append(df)

    consolidated_df = pd.concat(all_data)
    # consolidated_df = consolidated_df.sort_index().sort_values(by=["ticker", "date"])

    return consolidated_df


def run_backtest(ticker: str, start_date: str, end_date: str, initial_cash: float = initial_cash):
    global net_portfolio_pnl
    print(f"========Running backtest on {ticker}========")
    # Load historical data
    df = load_data(ticker, start_date, end_date)
    # df = consolidate_watchlist_data(TEST_WATCHLIST, start_date, end_date)

    # Generate buy/sell signals
    print(f"Generating Signals for {ticker}")
    signal_df = generate_signals(df)

    # Simulate trades and get trade log
    print(f"Simulating Trades for {ticker}")
    trade_log = simulate_trades(signal_df, ticker, initial_cash)

    # Performance analysis
    print(f"Analyzing Performance for {ticker}")
    performance_metrics = analyze_performance(trade_log, initial_cash)

    print("\nPerformance Metrics for :")
    for k, v in performance_metrics.items():
        print(f"{k}: {v}")
    ticker_pnl = performance_metrics["Net PnL ($)"]
    net_portfolio_pnl += ticker_pnl

    trade_logs.append(trade_log)

    # Optional: Visualize
    # plot_results(df, signal_df, trade_log)
    print(f"========Completed backtest on {ticker}========\n")

if __name__ == "__main__":
    TEST_TRADE_PATH = ROOT_DIR / "data" / "test" / "backtest_trade_log.csv"
    for ticker in TEST_WATCHLIST:
        run_backtest(ticker=ticker, start_date=start_date, end_date=today)
    print(f"Net Cumulative P&L: ${net_portfolio_pnl:,.2f}. ROI: {net_portfolio_pnl / initial_cash: .2%}")

    # ======= Alpha Scoring ========
    print("=========== Alpha Scoring Across All Tickers ===========")
    all_trades_df = pd.concat(trade_logs, ignore_index=True) # trade_logs is a list of pd dataframes
    all_trades_df.to_csv(TEST_TRADE_PATH, index=False)
    alpha_df = score_alpha_by_ticker(all_trades_df, initial_cash)
    print(alpha_df)
