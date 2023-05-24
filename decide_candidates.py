from scan_account import scanAccount
from scan_candidates import scanCandidates
from class_order import Order
import pandas as pd
from parameters import total_equity

def decideCandidates():
    # Get available equity
    positions, num_positions, available_equity = scanAccount()

    frame = pd.read_csv('candidates_Nasdaq.csv')
    potential_buy = scanCandidates(frame)

    buy_plan = []
    for new_ticker, new_ticker_price in potential_buy:
        if available_equity / total_equity > 0.2:    
            new_quantity = total_equity * 0.2 // new_ticker_price
            place = Order()
            place.buy_order(new_ticker, new_quantity)  

            buy_plan.append((new_ticker, new_ticker_price, new_quantity))
             
    return buy_plan