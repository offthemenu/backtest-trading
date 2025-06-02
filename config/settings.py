from datetime import datetime

#========== Setup ==========

WATCHLIST_BACKTEST_SELECTION = [
    # Tech giants
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN", "TSLA",

    # Semiconductor / AI
    "AMD", "INTC", "MU", "AVGO", "SMCI",

    # Financials
    "JPM", "BAC", "WFC", "GS", "C",

    # Healthcare
    "PFE", "MRNA", "JNJ", "UNH",

    # Energy
    "XOM", "CVX", "SLB",

    # Consumer Discretionary
    "NKE", "MCD", "SBUX", "HD", "COST", "DIS", "AMZN", "TSLA",

    # ETFs
    "SPY",   # S&P 500 ETF
    "QQQ",   # NASDAQ-100 ETF
    "IWM",   # Russell 2000 ETF
    "DIA",   # Dow Jones ETF
    "UVXY",  # Volatility ETF (VIX Short-Term Futures)

    # Biotech & Speculative
    "BNTX", "RIVN", "LCID", "PLTR", "ROKU", "PYPL",

    # Small-Mid Cap momentum stocks
    "UPST", "SOFI", "AFRM", "AI", "DKNG", "FUBO", "TSM", "FSLR",

    # Meme stocks / Volatile plays
    "GME", "AMC", "BBBY", "CVNA",

    # Industrials
    "BA", "GE"
]

#----------- Position Sizing -----------
MAX_POSITION_PCT = 1/3

#----------- Mode Selection -----------
LIVE_MODE = True

#----------- Current Timestamp -----------
today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
