from alpaca.trading.client import TradingClient
from module_technical_analysis import TechnicalAnalysis
import yfinance as yf
import config

tc = TradingClient(config.API_KEY, config.SECRET_KEY)

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

        close_price = df['Close'][-1]

        if df['good_to_buy'][-1] == True:
            analysis_result[ticker] = ('Buy', close_price)
        elif df['good_to_sell'][-1] == True:
            analysis_result[ticker] = ('Sell', close_price)
        else:
            analysis_result[ticker] = (None, close_price)
    
    return analysis_result

# print(scan_account())
                        