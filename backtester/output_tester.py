from pathlib import Path
from datetime import datetime
import pandas as pd
from backtester.data_loader import load_data
from backtester.strategy_runner import generate_signals
from backtester.execution_engine import simulate_trades
from backtester.performance import analyze_performance
from backtester.alpha_scoring import score_alpha_by_ticker
from backtester.visualize import plot_backtest

ROOT_DIR = Path(__file__).parent.parent

start_date = (datetime.today().replace(year=datetime.today().year - 3)).strftime("%Y-%m-%d")
today = datetime.today().strftime("%Y-%m-%d")

TEST_WATCHLIST = ['QQQM', 'IAU', 'XLV', 'VOO']
net_portfolio_pnl = 0
initial_cash = float(10_000.0)
trade_logs = []

# Sig Generation Test
for ticker in TEST_WATCHLIST:
    TEST_DATA_DIR = ROOT_DIR / "data" / "test" / f"{ticker}.csv"
    df = load_data(ticker, start_date, today)
    # df = consolidate_watchlist_data(TEST_WATCHLIST, start_date, end_date)

    # Generate buy/sell signals
    print(f"Generating Signals for {ticker}")
    signal_df = generate_signals(df)
    signal_df.to_csv(TEST_DATA_DIR)