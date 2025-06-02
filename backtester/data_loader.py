import pandas as pd
import os
from datetime import datetime
from pandas_datareader import data as pdr
from pathlib import Path
from config.settings import WATCHLIST

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"

def fetch_from_api(ticker: str, start_date: str, end_date: str, cache_path: str):
    print(f"[{ticker}] Fetching from Stooq...")
    stooq_ticker = f"{ticker}.US" if not ticker.endswith(".US") else ticker
    df = pdr.DataReader(stooq_ticker, 'stooq', start=start_date, end=end_date)
    if df.empty:
        raise ValueError(f"No data returned for {ticker} from Stooq.")
    df["Ticker"] = ticker
    df = df[['Ticker','Open', 'High', 'Low', 'Close', 'Volume']]
    df.columns = [col.lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df.to_csv(cache_path)
    print(f"[{ticker}] Cached to {cache_path}")
    return df

def load_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Load historical OHLCV data for a ticker.
    - First checks local cache: data/cache/{ticker}.csv
    - Falls back to Stooq API via pandas_datareader
    - Saves successful pulls to cache
    """
    print(f"Loading Data for {ticker}")
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{ticker}.csv")
    
    try:
        # Try loading from local cache
        if os.path.exists(cache_path):
            df_cached = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            if df_cached.index.min() <= pd.to_datetime(start_date) and df_cached.index.max() >= pd.to_datetime(end_date):
                print(f"[{ticker}] Using cached data")
                return df_cached.loc[start_date:end_date]
            else:
                print(f"[{ticker}] Cache incomplete → refetching full range")
                return fetch_from_api(ticker, start_date, end_date, cache_path)
        else:
            return fetch_from_api(ticker, start_date, end_date, cache_path)
    except Exception as e:
        print(f"[{ticker}] Load failed: {e}")
        return pd.DataFrame()

#======Test========
# for ticker in WATCHLIST:
#     df = load_data(ticker, "2022-01-01", "2025-05-28")
#     print(df)