import pandas as pd

def calculate_indicators(df: pd.DataFrame, ema_short: int, ema_long: int, rsi_period: int):
    '''
    Input: Dataframe with schema of:
    {
      "date": "2024-06-16",
      "open": 79200,
      "high": 82500,
      "low": 78000,
      "close": 80000,
      "currency": "KRW"
    }
    '''
    
    df["ema_short"] = df["close"].ewm(span=ema_short, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=ema_long, adjust=False).mean()
    return df

def generate_trades(df: pd.DataFrame):
    trades = []

    return trades