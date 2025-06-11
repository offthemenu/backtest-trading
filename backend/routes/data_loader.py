from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query, HTTPException, FastAPI, APIRouter
from datetime import datetime, timedelta
from typing import List
import random
import investpy

router = APIRouter(prefix="/v01")

# basic in-memory cache
cache: dict[str, dict] = {}

@router.get('/ping')
async def ping():
    return {'message': "pong"}

# Country Stock Retrieval
@router.get('/get_stocks')
def get_stocks(
    country: str = Query(...)
):
    '''
    Get all available stocks for a given country's exchange via investpy and return an object of all available stocks
    '''
    stocks = []
    try:
        df_stocks = investpy.stocks.get_stocks(
            country=country
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to retrieve stocks for {country}.")

    for idx, row in df_stocks.iterrows():
        stock = row["full_name"]
        ticker = row["symbol"]

        stocks.append({
            "ticker": ticker,
            "stock": stock
        })
    
    stocks.sort(key=lambda x: x["stock"].lower())

    result = {
        "country": country,
        "available_stocks": stocks
    }

    return result

# Country Fund Retrieval
@router.get('/get_funds')
def get_funds(
    country: str = Query(...)
):
    '''
    Get all available funds for a given country's exchange via investpy and return an object of all available funds
    '''
    funds = []
    try:
        df_funds = investpy.funds.get_funds(
            country=country
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to retrieve funds for {country}.")

    for idx, row in df_funds.iterrows():
        stock = row["name"]
        ticker = row["symbol"]

        funds.append({
            "ticker": ticker,
            "stock": stock
        })
    
    funds.sort(key=lambda x: x["stock"].lower())
    result = {
        "country": country,
        "available_funds": funds
    }

    return result

# Country ETF Retrieval
@router.get('/get_etfs')
def get_etfs(
    country: str = Query(...)
):
    '''
    Get all available etfs for a given country's exchange via investpy and return an object of all available etfs
    '''
    etfs = []
    try:
        df_etfs = investpy.etfs.get_etfs(
            country=country
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to retrieve etfs for {country}.")

    for idx, row in df_etfs.iterrows():
        stock = row["name"]
        ticker = row["symbol"]

        etfs.append({
            "ticker": ticker,
            "stock": stock
        })

    etfs.sort(key=lambda x: x["stock"].lower())
    result = {
        "country": country,
        "available_etfs": etfs
    }

    return result

# Country Crypto Retrieval
@router.get('/get_cryptos')
def get_cryptos():
    '''
    Get all available coins investpy and return an object of all available coins
    '''
    coins = []
    try:
        df_coins = investpy.crypto.get_cryptos()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to retrieve etfs.")

    for idx, row in df_coins.iterrows():
        stock = row["name"]
        ticker = row["symbol"]

        coins.append({
            "ticker": ticker,
            "stock": stock
        })

    coins.sort(key=lambda x: x["stock"].lower())
    result = {
        "country": None,
        "available_cryptos": coins
    }

    return result

@router.get('/load_data')
def load_data(
    asset_type: str = Query(..., alias= "type"),
    ticker: str = Query(...),
    country: str = Query(...),
    from_date: str = Query(..., alias="from"),
    to_date: str = Query(..., alias="to"),
    interval: str = Query(..., alias="interval")
):  
    '''
    List of available countries using investpy (alphabetical order)
    [
        'argentina', 'australia', 'austria', 
        'bahrain', 'bangladesh', 'belgium', 'bosnia', 'botswana', 'brazil', 'bulgaria', 
        'canada', 'chile', 'china', 'colombia', 'costa rica', 'croatia', 'cyprus', 'czech republic', 
        'denmark', 'dubai', 
        'egypt', 
        'finland', 'france', 
        'germany', 'greece', 
        'hong kong', 'hungary', 
        'iceland', 'india', 'indonesia', 'iraq', 'ireland', 'israel', 'italy', 'ivory coast', 
        'jamaica', 'japan', 'jordan', 
        'kazakhstan', 'kenya', 'kuwait', 
        'lebanon', 'luxembourg', 
        'malawi', 'malaysia', 'malta', 'mauritius', 'mexico', 'mongolia', 'montenegro', 'morocco', 
        'namibia', 'netherlands', 'new zealand', 'nigeria', 'norway', 
        'oman', 
        'pakistan', 'palestine', 'peru', 'philippines', 'poland', 'portugal', 
        'qatar', 
        'romania', 'russia', 'rwanda', 
        'saudi arabia', 'serbia', 'singapore', 'slovakia', 'slovenia', 'south africa', 'south korea', 'spain', 'sri lanka', 'sweden', 'switzerland', 
        'taiwan', 'tanzania', 'thailand', 'tunisia', 'turkey', 
        'uganda', 'ukraine', 'united kingdom', 'united states', 'uruguay', 
        'venezuela', 'vietnam', 
        'zambia', 'zimbabwe'
    ]
    '''
    # Validate date format
    try:
        from_obj = datetime.strptime(from_date, "%Y-%m-%d")
        to_obj = datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if from_obj > to_obj:
        raise HTTPException(status_code=400, detail="`from` date must be earlier than `to` date.")

    # Construct cache key
    cache_key = f"{ticker}_{asset_type}_{country}_{interval}_{from_date}_{to_date}"
    if cache_key in cache:
        return cache[cache_key]
    
    df = None
    try:
        if asset_type == "stocks":
            df = investpy.stocks.get_stock_historical_data(
                stock=ticker,
                country=country.lower(),
                from_date=from_obj.strftime('%d/%m/%Y'),
                to_date=to_obj.strftime('%d/%m/%Y'),
                as_json=False,
                order='ascending',
                interval=interval.lower()
            )
        elif asset_type == "funds":
            # Find Fund name from the ticker using get_funds
            available_funds = get_funds(country=country)["available_funds"]
            fund_name = None

            for fund in available_funds:
                if fund["ticker"] == ticker:
                    fund_name = fund["stock"]
                    break
                if not fund_name:
                    raise HTTPException(status_code=404, detail= f"Fund with ticker {ticker} not found in {country}.")
                
            df = investpy.funds.get_fund_historical_data(
                fund=fund_name,
                country=country.lower(),
                from_date=from_obj.strftime('%d/%m/%Y'),
                to_date=to_obj.strftime('%d/%m/%Y'),
                as_json=False,
                order='ascending'
            )
        elif asset_type == "etfs":
            # Find the ETF name from the ticker using get_etfs
            available_etfs = get_etfs(country=country)["available_etfs"]
            etf_name = None
            for etf in available_etfs:
                if etf["ticker"].lower() == ticker.lower():
                    etf_name = etf["stock"]
                    break
            if not etf_name:
                raise HTTPException(status_code=404, detail=f"ETF with ticker {ticker} not found in {country}.")
            
            df = investpy.etfs.get_etf_historical_data(
                etf=etf_name,
                country=country.lower(),
                from_date=from_obj.strftime('%d/%m/%Y'),
                to_date=to_obj.strftime('%d/%m/%Y'),
                as_json=False,
                order='ascending',
                interval=interval.lower()
            )

        elif asset_type == "cryptocurrency":
            # Find the Crypto name from the ticker using get_crypto
            available_cryptos = get_cryptos()["available_cryptos"]
            crypto_name = None

            for crypto in available_cryptos:
                if crypto["ticker"].lower() == ticker.lower():
                    crypto_name = crypto["stock"]
                    break
            if not crypto_name:
                raise HTTPException(status_code=404, detail=f"Crypto with ticker {ticker} not found in {country}.")

            df = investpy.crypto.get_crypto_historical_data(
                crypto=crypto_name,
                from_date=from_obj.strftime('%d/%m/%Y'),
                to_date=to_obj.strftime('%d/%m/%Y'),
                as_json=False,
                order='ascending',
                interval=interval.lower()
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported asset type: {asset_type}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve stock data for {ticker}: {e}")

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Data not found for {ticker} ({country})."
        )

    df.reset_index(inplace=True)

    candles = []
    for _, row in df.iterrows():
        date_str = row['Date'].strftime('%Y-%m-%d')
        candles.append({
            "date": date_str,
            "open": round(float(row['Open']), 2),
            "high": round(float(row['High']), 2),
            "low": round(float(row['Low']), 2),
            "close": round(float(row['Close']), 2),
            "currency": row.get('Currency', 'USD')  # fallback if missing
        })

    result = {
        "ticker": ticker.upper(),
        "from": from_date,
        "candles": candles
    }

    cache[cache_key] = result  # optional, can disable during dev
    return result


# to run
# uvicorn main:app --reload --port 8000

# Test
samsung = '005930'
samsung_historic = investpy.stocks.get_stock_historical_data(stock=samsung,country='south korea',from_date='01/01/2025',to_date='06/09/2025',as_json=False,order='descending',interval='Daily')
available_countries = investpy.stocks.get_stock_countries()
available_stocks = investpy.stocks.get_stocks(country='united states')
available_funds = get_funds(country='united states')
available_crypto = get_cryptos()
available_etfs = get_etfs(country='united states')
# print(available_etfs["available_etfs"])
# print(available_funds["available_funds"][:10])
print(available_crypto["available_cryptos"][:10])
