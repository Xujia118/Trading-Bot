from alpaca.trading.client import TradingClient
from technical_analysis import TechnicalAnalysis
import yfinance as yf
import os

# import config
# API_KEY, SECRET_KEY = config.API_KEY, config.SECRET_KEY
# tc = TradingClient(config.API_KEY, config.SECRET_KEY)

API_KEY, SECRET_KEY = os.getenv("API_KEY"), os.getenv("SECRET_KEY")
tc = TradingClient(API_KEY, SECRET_KEY)

def scan_account():
    open_positions = tc.get_all_positions()
 
    holding_positions = {}
    for position in open_positions:
        symbol = position.symbol
        holding_price = float(position.avg_entry_price)
        holding_quantity = int(position.qty)     
        
        holding_positions[symbol] = [holding_price, holding_quantity]
        num_positions = len(holding_positions)
    
    available_cash = float(tc.get_account().cash)
    total_equity = float(tc.get_account().portfolio_value)

    return holding_positions, num_positions, available_cash, total_equity

def run_ta(holding_positions): 
    
    analysis_result = {}  
    
    for ticker in holding_positions:
        df = yf.download(ticker, start='2022-09-01')
        
        print(f'Running technical analysis on {ticker}...')
        ta = TechnicalAnalysis(df)
        ta.good_to_buy()
        ta.good_to_sell()

        close_price = df.iloc[-1]['Close']

        if df.iloc[-1]['good_to_buy'] == True:
            analysis_result[ticker] = ('Buy', close_price)
        elif df.iloc[-1]['good_to_sell'] == True:
            analysis_result[ticker] = ('Sell', close_price)
        else:
            analysis_result[ticker] = (None, close_price)
    
    return analysis_result

# print(scan_account())
                        