import sys
import os
from datetime import datetime

# Set today
today = datetime.today().strftime("%Y-%m-%d")
one_year_ago = datetime.today().replace(year=datetime.today().year - 1).strftime("%Y-%m-%d")

# 👇 Add the parent directory of backtester to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backtester.visualize import plot_backtest
from backtester.data_loader import load_data
from backtester.strategy_runner import generate_signals
from backtester.execution_engine import simulate_trades
from config.settings import WATCHLIST_BACKTEST_SELECTION
import pandas as pd
import streamlit as st

st.sidebar.title("Backtest Settings")
ticker = st.sidebar.selectbox("Select Ticker:", WATCHLIST_BACKTEST_SELECTION)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime(one_year_ago))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime(today))

initial_cash = st.sidebar.number_input("Initial Cash:", min_value=0, value=10_000, step=100)

# Load and simulate
df = load_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
signal_df = generate_signals(df)
trade_log = simulate_trades(signal_df, ticker, initial_cash)

# Plot
plot_backtest(signal_df, trade_log)
