import pandas as pd
import numpy as np
from config.settings import WATCHLIST_BACKTEST_SELECTION

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add EMA, RSI, and ATR indicators to df
    === Dataframe Schema: Date,open,high,low,close,volume ===
    """
    df_calc = df.copy()

    # EMA Calculation
    df_calc["ema10"] = df_calc["close"].ewm(span=10, adjust=False).mean()
    df_calc["ema50"] = df_calc["close"].ewm(span=50, adjust=False).mean()

    # RSI Calculation
    delta = df_calc["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi_14 = round(100 - (100 / (1+rs)), 3)
    df_calc["rsi_14"] = rsi_14

    # ATR Calculation (14 days)
    high_low = df_calc["high"] - df_calc["low"]
    high_close = np.abs(df_calc["high"] - df_calc["close"].shift())
    low_close = np.abs(df_calc["low"] - df_calc["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis= 1).max(axis=1)
    df_calc["atr_14"] = tr.rolling(window=14).mean()
    
    # Testing purposes only
    # print(df_calc) 
    
    return df_calc

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies your real-world defensive strategy over historical data.
    Produces BUY/SELL/HOLD signals with reasons and signal prices.
    """
    print(f"Computing indicators...")
    df_signals = compute_indicators(df)
    df_signals["volume_sma"] = df_signals["volume"].rolling(window=20).mean()

    df_signals["signal"] = "HOLD"
    df_signals["signal_price"] = np.nan
    df_signals["signal_reason"] = ""

    for i in range(len(df_signals)):
        row = df_signals.iloc[i]
        
        # retrieve indicators
        try:
            ema10 = row["ema10"]
            ema50 = row["ema50"]
            rsi = row["rsi_14"]
            atr = row["atr_14"]
            close = row["close"]
            volume = row["volume"]
            volume_sma = row["volume_sma"]
        except Exception as e:
            print(f"Error identified: {e}")
            continue
        
        atr_ratio = atr / close if close else 0
        buy_score = 0
        signal = "HOLD"
        reason = ""

        # Buy Scoring:
        if ema10 > ema50: buy_score += 1
        if volume > volume_sma: buy_score += 1
        if 40 < rsi < 65: buy_score += 1
        if atr_ratio < 0.03: buy_score += 1
        if close > ema50 * 1.015: buy_score += 1
        if close < ema10 * 1.02: buy_score += 1
        
        # Final BUY condition
        if buy_score >= 4 or rsi < 25:
            signal = "BUY"
            reason = f"Buy Score = {buy_score}" if rsi >= 25 else "RSI < 25"

        # Sell condition
        elif ema10 < ema50 or rsi < 30 or atr_ratio > .03:
            signal = "SELL"
            reason = "EMA down / RSI drop / ATR spike"
            
        df_signals.at[df.index[i], "signal"] = signal
        df_signals.at[df.index[i], "signal_price"] = close
        df_signals.at[df.index[i], "signal_reason"] = reason
        
    return df_signals

