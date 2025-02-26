from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from technical_analysis import TechnicalAnalysis
import pandas as pd
import os


API_KEY, SECRET_KEY = os.getenv("API_KEY"), os.getenv("SECRET_KEY")

# Instances
tc = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Because I instantiate without a df, I will need to call set_df() method later.
# Preferably, instantiation should be in a same place with df creation
ta = TechnicalAnalysis(None)

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)