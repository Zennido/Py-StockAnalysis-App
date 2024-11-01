import requests
from collections import defaultdict
import pandas as pd

class StockCryptoDataFetcher:
    def __init__(self, stock_api_key):
        self.stock_api_key = stock_api_key
        self.stock_cache = {}
        self.crypto_cache = defaultdict(dict)

    def fetch_stock_data(self, symbol):
        if symbol in self.stock_cache:
            print("Fetching stock data from cache.")
            return self.stock_cache[symbol]
        
        base_url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.stock_api_key,
            'outputsize': 'compact'
        }

        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            self.stock_cache[symbol] = data  # Cache the fetched data
            return data
        else:
            raise Exception(f"Error fetching stock data: {response.status_code}")

    def fetch_crypto_data(self, crypto_id):
        if crypto_id in self.crypto_cache:
            print("Fetching cryptocurrency data from cache.")
            return self.crypto_cache[crypto_id]

        base_url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': crypto_id,
            'vs_currencies': 'usd'
        }

        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            self.crypto_cache[crypto_id] = data  # Cache the fetched data
            return data
        else:
            raise Exception(f"Error fetching cryptocurrency data: {response.status_code}")

    def display_stock_data(self, data):
        """Displays stock data in a tabular format using pandas."""
        if 'Time Series (Daily)' in data:
            stock_data = data['Time Series (Daily)']
            df = pd.DataFrame.from_dict(stock_data, orient='index')
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df.index.name = 'Date'
            df = df.astype({'Open': 'float', 'High': 'float', 'Low': 'float', 'Close': 'float', 'Volume': 'int'})
            print(df)

if __name__ == "__main__":
    api_key = '72358fkpa1d660hr'  # Make sure to use your own API key
    fetcher = StockCryptoDataFetcher(api_key)
    
    # Top 5 stock symbols
    stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    # Top 5 cryptocurrency IDs
    crypto_ids = ['bitcoin', 'ethereum', 'ripple', 'cardano', 'solana']

    # Fetch and display stock data
    for symbol in stock_symbols:
        try:
            stock_data = fetcher.fetch_stock_data(symbol)
            print(f"Stock Data for {symbol}:")
            fetcher.display_stock_data(stock_data)  # Display stock data in tabular form
        except Exception as e:
            print(e)

    # Fetch and display cryptocurrency data
    for crypto_id in crypto_ids:
        try:
            crypto_data = fetcher.fetch_crypto_data(crypto_id)
            print(f"Cryptocurrency Data for {crypto_id}:")
            print(crypto_data)
        except Exception as e:
            print(e)
