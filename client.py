from alpaca.trading.client import TradingClient

import os
# API_KEY, SECRET_KEY = os.getenv("API_KEY"), os.getenv("SECRET_KEY")

import config
API_KEY, SECRET_KEY = config.API_KEY, config.SECRET_KEY

# Other files can import this
tc = TradingClient(API_KEY, SECRET_KEY, paper=True)
