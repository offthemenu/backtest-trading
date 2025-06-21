# dev/test_loader.py

from routes.data_loader import get_funds, get_cryptos, get_etfs, get_stocks

if __name__ == "__main__":
    print("Fetching test data...")
    funds = get_funds(country="united states")
    cryptos = get_cryptos()
    print(f"Sample Funds: {funds['available_funds'][:5]}")
    print(f"Sample Cryptos: {cryptos['available_cryptos'][:5]}")
    # Test
    samsung = '005930'
    available_funds = get_funds(country='united states')
    available_crypto = get_cryptos()
    available_etfs = get_etfs(country='united states')
    # print(available_etfs["available_etfs"])
    # print(available_funds["available_funds"][:10])
    print(available_crypto["available_cryptos"][:10])