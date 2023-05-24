import pandas as pd
from class_analysis_technical import Technical_analysis
from scan_account import scanAccount
import yfinance as yf

frame = pd.read_csv('candidates_Nasdaq.csv')

def scanCandidates(frame):
    positions, _, _ = scanAccount()

    potential_buy = []
    for ticker in frame['symbol']:
        # For ticker in positions, we already did everything in Step 1.
        if ticker in positions:
            continue

        # For other tickers, download historical data and run technical analysis for buy signals
        try:
            df = yf.download(ticker, start='2022-09-01')
            print('Running technical analysis on', ticker)
            ta = Technical_analysis(df)
            ta.good_to_buy()
        except:
            continue

        if df['good_to_buy'][-1] == True:
            potential_buy.append((ticker, df['Close'][-1]))

    return potential_buy
        
