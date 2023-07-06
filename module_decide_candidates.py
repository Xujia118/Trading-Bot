from alpaca.trading.client import TradingClient
import config
import module_scan_account
import module_scan_candidates
from module_order import Order
import pandas as pd

def decide_candidates():
    tc = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

    # The bot would fire the same orders if yesterday was a holiday. 
    # So if there are pending orders, do nothing. 
    open_orders = tc.get_orders()
    if len(open_orders) > 0:
        return

    # Get available equity
    positions, num_positions, available_cash, total_equity = module_scan_account.scan_account()

    frame = pd.read_csv('candidates_Nasdaq.csv')
    potential_buy = module_scan_candidates.scan_candidates(frame)
    buy_plan = []

    for new_ticker, new_ticker_price in potential_buy:
        if available_cash / total_equity > 0.2:    
            new_quantity = total_equity * 0.2 // new_ticker_price
            if new_quantity > 0:
                place = Order(new_ticker, new_quantity)
                place.buy_order()  

            buy_plan.append((new_ticker, new_ticker_price, new_quantity))
             
    return buy_plan

# print(decide_candidates())