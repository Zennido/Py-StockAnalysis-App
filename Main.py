import requests
from collections import defaultdict
import time
import csv

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

    def export_to_csv(self, data, filename):
        """Exports the provided data to a CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            if isinstance(data, dict):
                # Handle stock data (which is typically a nested dictionary)
                # Write the header
                writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
                for date, values in data.get('Time Series (Daily)', {}).items():
                    writer.writerow([date, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. volume']])
            elif isinstance(data, list):
                # Handle cryptocurrency data (which is usually simpler)
                writer.writerow(['Crypto ID', 'Price (USD)'])
                for crypto_id, values in data.items():
                    writer.writerow([crypto_id, values['usd']])

if __name__ == "__main__":
    api_key = '72358fkpa1d660hr'
    fetcher = StockCryptoDataFetcher(api_key)
    
    stock_symbol = 'AAPL'  # Example: Apple Inc.
    crypto_id = 'bitcoin'   # Example: Bitcoin

    try:
        stock_data = fetcher.fetch_stock_data(stock_symbol)
        print("Stock Data:")
        print(stock_data)
        fetcher.export_to_csv(stock_data, 'stock_data.csv')  # Export stock data to CSV
    except Exception as e:
        print(e)

    try:
        crypto_data = fetcher.fetch_crypto_data(crypto_id)
        print("Cryptocurrency Data:")
        print(crypto_data)
        fetcher.export_to_csv(crypto_data, 'crypto_data.csv')  # Export crypto data to CSV
    except Exception as e:
        print(e)
