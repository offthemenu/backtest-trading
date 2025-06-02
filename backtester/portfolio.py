class PortfolioState:
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.position = 0
        self.entry_price = 0.0
        self.max_price = 0.0
        self.trade_history = []
        self.daily_nav = []
        self.realized_pnl = 0.0

    def buy(self, date, shares, price, atr, reason):
        fill_price = price
        total_cost = fill_price * shares + 0.005 * shares
        if self.cash < total_cost:
            return False  # insufficient funds

        self.cash -= total_cost
        self.position = shares
        self.entry_price = fill_price
        self.max_price = fill_price

        self.trade_history.append({
            "date": date,
            "type": "BUY",
            "shares": shares,
            "price": fill_price,
            "atr": atr,
            "reason": reason,
            "cash_after": self.cash
        })
        return True

    def sell(self, date, price, atr, reason):
        if self.position == 0:
            return False  # nothing to sell

        fill_price = price
        shares = self.position
        proceeds = fill_price * shares - 0.005 * shares
        pnl = (fill_price - self.entry_price) * shares
        self.cash += proceeds
        self.realized_pnl += pnl

        self.trade_history.append({
            "date": date,
            "type": "SELL",
            "shares": shares,
            "price": fill_price,
            "atr": atr,
            "reason": reason,
            "cash_after": self.cash,
            "pnl": pnl
        })

        self.position = 0
        self.entry_price = 0.0
        self.max_price = 0.0
        return True

    def update_max_price(self, price):
        if self.position > 0 and price > self.max_price:
            self.max_price = price

    def mark_to_market(self, date, close_price):
        nav = self.cash + self.position * close_price
        self.daily_nav.append({"date": date, "nav": nav})
        self.update_max_price(close_price)

    def get_nav_history(self):
        return self.daily_nav

    def get_trade_log(self):
        return self.trade_history

    def get_realized_pnl(self):
        return self.realized_pnl