import sys
import requests
from collections import defaultdict
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
)

class StockCryptoDataFetcher:
    def __init__(self, stock_api_key):
        self.stock_api_key = stock_api_key
        self.stock_cache = {}
        self.crypto_cache = defaultdict(dict)

    def fetch_stock_data(self, symbol):
        if symbol in self.stock_cache:
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
            self.stock_cache[symbol] = data
            return data
        else:
            raise Exception(f"Error fetching stock data: {response.status_code}")

    def fetch_crypto_data(self, crypto_id):
        if crypto_id in self.crypto_cache:
            return self.crypto_cache[crypto_id]

        base_url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': crypto_id,
            'vs_currencies': 'usd'
        }

        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            self.crypto_cache[crypto_id] = data
            return data
        else:
            raise Exception(f"Error fetching cryptocurrency data: {response.status_code}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fetcher = StockCryptoDataFetcher('YOUR_API_KEY_HERE')

    def initUI(self):
        self.setWindowTitle('Stock and Crypto Data Fetcher')
        layout = QVBoxLayout()

        # Stock input
        self.stock_input = QLineEdit(self)
        self.stock_input.setPlaceholderText('Enter stock symbol (e.g. AAPL)')
        layout.addWidget(self.stock_input)

        self.stock_button = QPushButton('Fetch Stock Data', self)
        self.stock_button.clicked.connect(self.fetch_stock)
        layout.addWidget(self.stock_button)

        self.stock_output = QTextEdit(self)
        self.stock_output.setReadOnly(True)
        layout.addWidget(self.stock_output)

        # Crypto input
        self.crypto_input = QLineEdit(self)
        self.crypto_input.setPlaceholderText('Enter crypto ID (e.g. bitcoin)')
        layout.addWidget(self.crypto_input)

        self.crypto_button = QPushButton('Fetch Crypto Data', self)
        self.crypto_button.clicked.connect(self.fetch_crypto)
        layout.addWidget(self.crypto_button)

        self.crypto_output = QTextEdit(self)
        self.crypto_output.setReadOnly(True)
        layout.addWidget(self.crypto_output)

        self.setLayout(layout)
        
        # Apply midnight blue theme
        self.setStyleSheet("""
            QWidget {
                background-color: #001f3f;
                color: #ffffff;
            }
            QLineEdit, QTextEdit {
                background-color: #003366;
                color: #ffffff;
                border: 1px solid #00509E;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #00509E;
                color: #ffffff;
                border: none;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0066CC;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

    def fetch_stock(self):
        symbol = self.stock_input.text()
        try:
            stock_data = self.fetcher.fetch_stock_data(symbol)
            if 'Time Series (Daily)' in stock_data:
                stock_series = stock_data['Time Series (Daily)']
                df = pd.DataFrame.from_dict(stock_series, orient='index')
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df.index.name = 'Date'
                self.stock_output.setText(str(df))
            else:
                self.stock_output.setText("No data available for this stock.")
        except Exception as e:
            self.stock_output.setText(str(e))

    def fetch_crypto(self):
        crypto_id = self.crypto_input.text()
        try:
            crypto_data = self.fetcher.fetch_crypto_data(crypto_id)
            self.crypto_output.setText(str(crypto_data))
        except Exception as e:
            self.crypto_output.setText(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(600, 400)
    ex.show()
    sys.exit(app.exec_())
