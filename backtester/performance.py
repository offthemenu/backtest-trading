import pandas as pd
import numpy as np
from math import sqrt
from backtester.portfolio import PortfolioState

def analyze_performance(trade_log: pd.DataFrame, initial_cash: float) -> dict:
    """
    Computes backtest performance metrics from a trade log DataFrame.
    Returns a dictionary of KPIs:
        Win rate: The percentage of trades that closed with a profit.

        Average gain/loss: The mean profit from winning trades and mean loss from losing trades, measured in dollars.

        Average holding period: The average number of days a position is held before being sold.

        Expected Return: The average expected return per trade, accounting for both win probability and payoff.

        Sharpe ratio: A risk-adjusted performance metric measuring return per unit of volatility.

        Max drawdown: The largest peak-to-trough equity decline during the backtest period.

        CAGR (Compound Annual Growth Rate): The annualized return your strategy would achieve assuming consistent compounding.
    """

    # When trade_log is empty:
    if trade_log.empty or "type" not in trade_log.columns:
        return {"error": "Trade log empty or invalid"}
    
    trades = trade_log.copy()
    trades["date"] = pd.to_datetime(trades["date"])
    trades.sort_values(by=["date"], inplace=True)

    # bypass non-closed trades
    if "pnl" not in trades.columns:
        return {"error": "No completed trades found"}
    
    completed_trades = trades[trades["type"] == "SELL"].copy()

    if completed_trades.empty:
        return {"error": "No completed SELL trades"}
    
    total_trades = len(completed_trades)
    winning_trades = completed_trades[completed_trades["pnl"] > 0]
    losing_trades = completed_trades[completed_trades["pnl"] <= 0]

    total_pnl = completed_trades["pnl"].sum()
    win_rate = len(winning_trades) / total_trades
    avg_win = winning_trades["pnl"].mean() if not winning_trades.empty else 0
    avg_loss = losing_trades["pnl"].mean() if not losing_trades.empty else 0
    expected_return = (win_rate * avg_win) + ((1-win_rate) * avg_loss)
    
    # Calculate holding days
    holding_periods = []
    for i in range(0, len(trades)-1):
        if trades.iloc[i]["type"] == "BUY" and trades.iloc[i+1]["type"] == "SELL":
            delta = trades.iloc[i+1]["date"] - trades.iloc[i]["date"]
            holding_periods.append(delta.days)

    avg_hold = np.mean(holding_periods) if holding_periods else None

    # Calculate CAGR and Sharpe Ratio
    first_date = trades["date"].iloc[0]
    last_date = trades["date"].iloc[-1] 
    days = (last_date - first_date).days
    cagr = ((1 + total_pnl / initial_cash) ** (365 / days) - 1)

    daily_returns = completed_trades["pnl"] / initial_cash
    sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * sqrt(252) if np.std(daily_returns) > 0 else 0

    # Calculate Max Drawdown 
    portfolio = PortfolioState(initial_cash=initial_cash)

    for i, trade in trades.iterrows():
        # Apply trades back into a shadow portfolio to simulate net asset value
        if trade["type"] == "BUY":
            portfolio.buy(
                date=trade["date"],
                shares=trade["shares"],
                price=trade["price"],
                atr=trade.get("atr", 2.0),
                reason=trade.get("reason", "")
            )
        elif trade["type"] == "SELL":
            portfolio.sell(
                date=trade["date"],
                price=trade["price"],
                atr=trade.get("atr", 2.0),
                reason=trade.get("reason", "")
            )
        
        # Recalculate NAV on every trade date
        current_price = trade["price"]
        portfolio.mark_to_market(trade["date"], current_price)

    nav_df = pd.DataFrame(portfolio.get_nav_history())
    nav_df.set_index("date", inplace=True)
    nav_df["rolling_max"] = nav_df['nav'].cummax()
    nav_df["drawdown"] = nav_df['rolling_max'] - nav_df['nav']
    max_drawdown = nav_df["drawdown"].max() if not nav_df.empty else 0.0

    return {
        "Total Trades": total_trades,
        "Win Rate": round(win_rate, 3),
        "Average Gain": round(avg_win, 2),
        "Average Loss": round(avg_loss, 2),
        "Expectancy": round(expected_return, 2),
        "Average Hold (days)": round(avg_hold, 1) if avg_hold is not None else "N/A",
        "CAGR": round(cagr * 100, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Max Drawdown ($)": round(max_drawdown, 2),
        "Net PnL ($)": round(total_pnl, 2)
    }