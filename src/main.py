import os
import alpaca_trade_api as tradeapi

from ticker import Ticker
from strategy import MovingAverageCrossover, MeanReversion
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version="v2")

# YFinance Data
apple = Ticker(ticker="AAPL", start_date="2020-01-01", end_date="2023-01-01")

# -- Perform Backtrading -- #
mac = MovingAverageCrossover(data=apple.data, short_window=40, long_window=100)
mac.run_backtrader()

mrs = MeanReversion(data=apple.data, window=30, num_std=2)
mrs.run_backtrader()
