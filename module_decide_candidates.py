import module_scan_account
import module_scan_candidates
import module_get_trade_history
from module_order import Order
import pandas as pd

pending_ticker, pending_qty = module_get_trade_history.get_pending_orders()

def decide_candidates():

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

                # Avoid repeating filing the same order as yesterday.
                if new_quantity != pending_qty and new_ticker != pending_ticker:
                    place.buy_order()  

            buy_plan.append((new_ticker, new_ticker_price, new_quantity))
             
    return buy_plan

# print(decide_candidates())