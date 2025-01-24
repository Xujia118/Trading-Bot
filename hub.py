from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from technical_analysis import TechnicalAnalysis
import pandas as pd
import os
# from dotenv import load_dotenv

# load_dotenv()

API_KEY, SECRET_KEY = os.getenv("API_KEY"), os.getenv("SECRET_KEY")

# Instances
tc = TradingClient(API_KEY, SECRET_KEY, paper=True)
ta = TechnicalAnalysis(None)
client = StockHistoricalDataClient(API_KEY, SECRET_KEY)