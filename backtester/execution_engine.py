import pandas as pd
from backtester.portfolio import PortfolioState

FEE_PER_SHARE = 0.005
SLIPPAGE_PCT = 0.001 # 0.1% price slippage
RISK_PER_TRADE = 0.005  # 0.5% of current NAV per trade


def simulate_trades(df: pd.DataFrame, ticker: str, initial_cash: float) -> pd.DataFrame:
    """
    Simulates trades based on signal columns from df.
    Returns a trade log with executed trades.
    """

    trade_log = []
    portfolio = PortfolioState(initial_cash)
    
    for index, row in df.iterrows():
        signal = row["signal"]
        price = row["signal_price"]
        atr = row.get("atr_14", 2.0)
        
        if pd.isna(price) or signal == "HOLD":
            continue
        
        price = float(price)
        
        # Buy Logic
        if signal == "BUY" and portfolio.position == 0:
            dollar_risk_per_share = atr
            risk_budget = RISK_PER_TRADE * portfolio.cash
            shares = int(risk_budget / dollar_risk_per_share)
            max_affordable = int(portfolio.cash // price)
            shares = min(shares, max_affordable)

            if shares > 0:
                fill_price = price * (1 + SLIPPAGE_PCT)
                cost = fill_price * shares + FEE_PER_SHARE * shares
                portfolio.cash -= cost
                portfolio.position += shares
                portfolio.entry_price = fill_price
                portfolio.max_price = fill_price

                nav = portfolio.cash + portfolio.position * fill_price

                trade_log.append({
                    "date": index,
                    "ticker": ticker,
                    "type": "BUY",
                    "shares": shares,
                    "price": fill_price,
                    "atr": atr,
                    "reason": row["signal_reason"],
                    "cash_after": portfolio.cash,
                    "shares_owned": portfolio.position,
                    "net_asset_value": nav
                })

        # Sell Logic
        elif signal == "SELL" and portfolio.position > 0:
            fill_price = price * (1 - SLIPPAGE_PCT)
            proceeds = fill_price * portfolio.position - FEE_PER_SHARE * portfolio.position
            pnl = (fill_price - portfolio.entry_price) * portfolio.position
            portfolio.cash += proceeds
            portfolio.realized_pnl += pnl
            nav = portfolio.cash

            trade_log.append({
                "date": index,
                "ticker": ticker,
                "type": "SELL",
                "shares": portfolio.position,
                "price": fill_price,
                "atr": atr,
                "reason": row["signal_reason"],
                "cash_after": portfolio.cash,
                "pnl": pnl,
                "shares_owned": 0,
                "net_asset_value": nav
            })

            portfolio.position = 0
            portfolio.entry_price = 0.0
            portfolio.max_price = 0.0
    
    # For testing purposes only
    # print(trade_log)            
    
    return pd.DataFrame(trade_log)