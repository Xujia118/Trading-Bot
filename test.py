import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
# from _get_ticker_data import get_tickcer_data
from hub import ta

start_date = '2022-01-01'
start_date = pd.to_datetime(start_date)
df = yf.download('FTNT', start='2024-01-01')
print(df.head())
