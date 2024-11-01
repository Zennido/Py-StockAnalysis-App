import requests

def fetch_stock_data(symbol, api_key):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'compact'
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching stock data: {response.status_code}")
        return None

def fetch_crypto_data(crypto_id):
    base_url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': crypto_id,
        'vs_currencies': 'usd'
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching cryptocurrency data: {response.status_code}")
        return None

if __name__ == "__main__":
    api_key = '72358fkpa1d660hr'
    stock_symbol = 'AAPL'  # Example: Apple Inc.
    crypto_id = 'bitcoin'   # Example: Bitcoin

    stock_data = fetch_stock_data(stock_symbol, api_key)
    crypto_data = fetch_crypto_data(crypto_id)

    if stock_data:
        print("Stock Data:")
        print(stock_data)

    if crypto_data:
        print("Cryptocurrency Data:")
        print(crypto_data)
