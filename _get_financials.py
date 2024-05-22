import yfinance as yf
import pandas as pd

df2 = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[4]
tickers = df2['Ticker'].to_list()
infos = [yf.Ticker(i).info for i in tickers] 
df2 = pd.DataFrame(infos)
df2 = df2.set_index('symbol')

fundamentals = ['trailingPE',
                'trailingEps',
                'returnOnEquity',
                'profitMargins',
                'dividendYield'
                ]

df2 = df2[fundamentals]
df2.to_csv('Fundamentals_Nasdaq.csv')
print('Fundamentals updated successfully.')