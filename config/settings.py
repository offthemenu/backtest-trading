from datetime import datetime

#========== Setup ==========
#----------- Primary Watchlist -----------
WATCHLIST = ['QQQM', 'IAU', 'XLV', 'VOO']
#----------- Secondary Watchlist -----------
WATCHLIST_BACKTEST_SELECTION = [
    "QQQM",  # US Tech - Nasdaq 100
    "VOO",   # US Broad Market - S&P 500
    "IAU",   # Gold / Inflation hedge
    "BOTZ",  # Robotics / Innovation
    "VWO",   # Emerging Markets ETF
    "XLU",   # Utilities - Defensive sector
    "XLP",   # Consumer Staples - Defensive sector
    "XLV",   # Healthcare - Defensive growth
    "VGK",   # Europe ex-UK ETF
    "EWJ",   # Japan ETF
    "IJH",   # US MidCap - S&P MidCap 400
    "IEF",   # 7–10yr Treasury Bonds ETF
]

#----------- Position Sizing -----------
MAX_POSITION_PCT = 1/3

#----------- Mode Selection -----------
LIVE_MODE = True

#----------- Current Timestamp -----------
today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
