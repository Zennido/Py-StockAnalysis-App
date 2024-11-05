import sys
import requests
from collections import defaultdict
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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

    def fetch_top_cryptos(self, crypto_ids):
        prices = {}
        for crypto_id in crypto_ids:
            try:
                data = self.fetch_crypto_data(crypto_id)
                prices[crypto_id] = data[crypto_id]['usd']
            except Exception as e:
                print(f"Error fetching data for {crypto_id}: {e}")
        return prices

class DonutChart(QWidget):
    def __init__(self, prices):
        super().__init__()
        self.initUI(prices)

    def initUI(self, prices):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a figure for the donut chart
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a donut chart
        self.plot_donut_chart(prices)

    def plot_donut_chart(self, prices):
        labels = prices.keys()
        sizes = prices.values()

        # Create a pie chart
        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        # Draw a circle at the center to make it a donut chart
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')
        plt.title('Top 5 Cryptocurrencies by Price')
        self.canvas.draw()

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

        # Show Donut Chart
        self.chart_button = QPushButton('Show Top 5 Crypto Donut Chart', self)
        self.chart_button.clicked.connect(self.show_donut_chart)
        layout.addWidget(self.chart_button)

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

    def show_donut_chart(self):
        top_cryptos = ['bitcoin', 'ethereum', 'ripple', 'cardano', 'solana']
        prices = self.fetcher.fetch_top_cryptos(top_cryptos)
        if prices:
            self.donut_chart = DonutChart(prices)
            self.donut_chart.resize(400, 300)
            self.donut_chart.setWindowTitle('Top 5 Cryptocurrencies')
            self.donut_chart.show()
        else:
            self.crypto_output.setText("Failed to fetch cryptocurrency data.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(600, 600)
    ex.show()
    sys.exit(app.exec_())
