from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from technical_analysis import TechnicalAnalysis
import pandas as pd
import config
import os

# Cloud Environment
# API_KEY, SECRET_KEY = os.getenv("API_KEY"), os.getenv("SECRET_KEY")

# Dev Environment
API_KEY, SECRET_KEY = config.API_KEY, config.SECRET_KEY

# Instances
tc = TradingClient(API_KEY, SECRET_KEY, paper=True)
ta = TechnicalAnalysis(pd.DataFrame())
client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
