from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from services.backtest_engine import calculate_indicators, generate_trades
from routes.data_loader import load_data  # reuse your existing logic
import pandas as pd

router = APIRouter(prefix="/v01")

@router.post("/v01/backtest")
def backtest(
    ticker: str = Query(...),
    country: str = Query(...),
    from_date: str = Query(...),
    to_date: str = Query(...),
    asset_type: str = Query(...),
    interval: str = Query(...),
    ema_short: int = Query(...),
    ema_long: int = Query(...),
    rsi_window: int = Query(...)
):
    return {}