import yfinance as yf
# from technical_analysis import TechnicalAnalysis
from hub import tc, ta
# I deliberately changed here!!!

def scan_account():
    # Fetch account data api once and get cash and equity
    account_data = tc.get_account()
    available_cash = float(account_data.cash)
    total_equity = float(account_data.portfolio_value)

    # Fetch holding positions
    open_positions = tc.get_all_positions()
    
    holding_positions = {}
    for position in open_positions:
        holding_price = float(position.avg_entry_price)
        holding_quantity = int(position.qty)     
        symbol = position.symbol
        holding_positions[symbol] = [holding_price, holding_quantity]
    
    # Calculate the number of positions
    num_positions = len(holding_positions)

    # Construct the account object
    account = {
        "holding_positions": holding_positions,
        "num_positions": num_positions, 
        "available_cash": available_cash,
        "total_equity": total_equity
    }

    return account

def run_ta(holding_positions): 
    
    analysis_result = {}  
    
    for ticker in holding_positions:
        df = yf.download(ticker, start='2022-01-01')
        
        print(f'Running technical analysis on {ticker}...')
        # ta = TechnicalAnalysis(df)
        ta.set_df(df)
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

print(scan_account())
# print(run_ta())
                        