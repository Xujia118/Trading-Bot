import pandas as pd
from _technical_analysis import TechnicalAnalysis
import scan_account
import yfinance as yf

frame = pd.read_csv('candidates_Nasdaq.csv')

def scan_candidates(frame):
    positions, _, _, _ = scan_account.scan_account()

    potential_buy = []
    for ticker in frame['symbol']:
        # For ticker in positions, we already did everything in Step 1.
        if ticker in positions:
            continue

        # For other tickers, download data and run technical analysis for buy signals
        try:
            df = yf.download(ticker, start='2022-09-01')
            print(f'Running technical analysis on {ticker}...')
            ta = TechnicalAnalysis(df)
            ta.good_to_buy()
            
            if df['good_to_buy'][-1] == True:
                potential_buy.append((ticker, df['Close'][-1]))

        except:
            continue

    return potential_buy
        
# print(scan_candidates(frame))