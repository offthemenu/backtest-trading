from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from datetime import datetime, timedelta
from typing import List
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during development only; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/v01/ping')
async def ping():
    return {'message': "pong"}

@app.get('/v01/load_data')
def load_data(
    ticker: str = Query(...),
    from_date: str = Query(..., alias="from")
):
    # Mock data generation
    num_days = 50
    data = []
    base_price = 100 + random.uniform(-10, 10)
    current_date = datetime.strptime(from_date, "%Y-%m-%d")

    for _ in range(num_days):
        open_price = base_price + random.uniform(-5, 5)
        close_price = open_price + random.uniform(-5, 5)
        high_price = max(open_price, close_price) + random.uniform(0, 3)
        low_price = min(open_price, close_price) - random.uniform(0, 3)
        date_str = current_date.strftime("%Y-%m-%d")

        data.append({
            "date": date_str,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
        })
        current_date += timedelta(days=1)

    return {
        "ticker": ticker,
        "from": from_date,
        "candles": data
    }


# to run
# uvicorn main:app --reload --port 8000