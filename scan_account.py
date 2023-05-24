from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
import config

from class_analysis_technical import Technical_analysis
import yfinance as yf

tc = TradingClient(config.API_KEY, config.SECRET_KEY)

def scanAccount():
    open_positions = tc.get_all_positions()
 
    holding_positions = {}
    for position in open_positions:
        symbol = position.symbol
        holding_price = position.avg_entry_price
        holding_quantity = position.qty
        available_equity = tc.get_account().cash
        
        holding_positions[symbol] = [holding_price, holding_quantity]
        num_positions = len(holding_positions)

    return holding_positions, num_positions, available_equity

def run_ta(holding_positions): 
    
    analysis_result = {}  
    
    for ticker in holding_positions:
        df = yf.download(ticker, start='2021-09-01')
        ta = Technical_analysis(df)
        ta.good_to_buy()
        ta.good_to_sell()

        close_price = df['Close'][-1]

        if df['good_to_buy'][-1] == True:
            analysis_result[ticker] = ('Buy', close_price)
        elif df['good_to_sell'][-1] == True:
            analysis_result[ticker] = ('Sell', close_price)
        else:
            analysis_result[ticker] = (None, close_price)
    
    return analysis_result
                                      
