import scan_account
import scan_candidates
import get_latest_order_date
from _order import Order
import pandas as pd

def decide_candidates():
    # Get pending orders if there are any
    # It's a dictionary: {'FTNT': '411', 'FANG': '132', 'CSCO': '397'}
    pending_orders = get_latest_order_date.get_pending_orders()

    # Get available equity
    positions, num_positions, available_cash, total_equity = scan_account.scan_account()

    frame = pd.read_csv('candidates_Nasdaq.csv')
    potential_buy = scan_candidates.scan_candidates(frame)
    buy_plan = []

    for new_ticker, new_ticker_price in potential_buy:
        if new_ticker in pending_orders:
            continue
        
        if available_cash / total_equity > 0.4:    
            new_quantity = total_equity * 0.2 // new_ticker_price
            if new_quantity > 0:
                place = Order(new_ticker, new_quantity)
                place.buy_order()  
                buy_plan.append((new_ticker, new_ticker_price, new_quantity))
             
    return buy_plan

print(decide_candidates())