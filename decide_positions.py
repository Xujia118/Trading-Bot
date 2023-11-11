import scan_account
import get_latest_order_date
from _order import Order
import pandas as pd
from datetime import date
import parameters
import json
import os

def get_positions_summary():
    # Get positions information
    positions, num_positions, available_cash, total_equity = scan_account.scan_account()

    # Run technical analysis on all holding tickers
    analysis_result = scan_account.run_ta(positions)

    # Get latest order date (used in sell)
    latest_order = get_latest_order_date.get_latest_order_date()
    
    # Combine info into a new data frame.
    df1 = pd.DataFrame.from_dict(positions, orient='index', columns=['Holding price', 'Quantity'])
    df2 = pd.DataFrame.from_dict(analysis_result, orient='index', columns=['Action', 'Last price'])
    df3 = pd.DataFrame.from_dict(latest_order, orient='index', columns=['Last order date'])

    position_df = pd.merge(df1, df2, left_index=True, right_index=True)
    position_df = pd.merge(position_df, df3, left_index=True, right_index=True)
        
    # Holding price Quantity Action  Last price Last order date
    # AAPL       173.105        2   None  175.160004      2023-05-15
    # AMZN        118.35        3   None  116.250000      2023-05-18
    
    return position_df, available_cash, num_positions

def decide_positions_actions():
    position_df, available_cash, num_positions = get_positions_summary()

    positions_sell, positions_buy = [], []

    for i in range(len(position_df)):
        ticker = position_df.index[i]
        holding_price = float(position_df['Holding price'].iloc[i])
        holding_quantity = int(position_df['Quantity'].iloc[i])
        cur_price = float(position_df['Last price'].iloc[i])
        last_trade_date = position_df['Last order date'].iloc[i]

        if position_df['Action'].iloc[i] == "Sell":             
            sell = sell_positions_stocks(ticker, 
                                 holding_price,
                                 holding_quantity,
                                 cur_price,
                                 last_trade_date)
            if sell:
                positions_sell.append(sell)
        
        if position_df['Action'].iloc[i] == "Buy":          
            buy = buy_positions_stocks(ticker,
                                 holding_price,
                                 holding_quantity,
                                 cur_price, 
                                 available_cash,
                                 num_positions)           
            if buy:
                positions_buy.append(buy)

    return positions_sell, positions_buy
    

pending_orders = get_latest_order_date.get_pending_orders()

def sell_positions_stocks(ticker, holding_price, holding_quantity, cur_price, last_trade_date):
    # Check selling conditions: ten days or 10% gain
    days_gone = (date.today() - last_trade_date).days
    if days_gone < 5 or cur_price < holding_price * (1 + parameters.profit_threshold): 
        return
    # 暂时改成5天，10天有点太长了，还是落袋为安比较好。
    
    # Sell if quantity is too small
    if holding_quantity <= 3:
        place = Order(ticker, holding_quantity)

        # Avoid repeating filing the same order as yesterday.
        if ticker not in pending_orders:
            place.sell_order()    
            sell_result = (ticker, holding_quantity)
            return sell_result
    
    # Sell in three operations
    json_file = f'selling_{ticker}.json'
    try:
        with open(json_file, 'r') as file:
            selling = json.load(file)
    except FileNotFoundError:
        selling = {}

    if ticker not in selling:
        # Sell a third of holding quantity
        sell_quantity = holding_quantity // 3

        # Update 'selling'. The remaining shares of this ticker will be sold in two operations.
        selling[ticker] = 2
    else:      
        if selling[ticker] == 2:
            sell_quantity = holding_quantity // 2
            selling[ticker] -= 1
        else:
            sell_quantity = holding_quantity
            del selling[ticker]
            os.remove(json_file)

    place = Order(ticker, sell_quantity)

    # Avoid repeating filing the same order as yesterday.
    if ticker not in pending_orders:
        place.sell_order()  
        sell_result = (ticker, sell_quantity)
        
    if selling:
        with open(json_file, 'w') as file:
            json.dump(selling, file)
 
    return sell_result

def buy_positions_stocks(ticker, holding_price, holding_quantity, cur_price, available_cash, num_positions):
    # Check if we are allowed to buy
    if available_cash / parameters.total_equity < parameters.invest_ratio or \
        cur_price > holding_price * parameters.rebuy_tolerance:
        # num_positions >= 3: not to use it for more frequent testing
        return

    buy_quantity = holding_quantity * 2
    place = Order(ticker, buy_quantity)

    # Avoid repeating filing the same order as yesterday.
    if ticker not in pending_orders:
        place.buy_order()

    buy_result = (ticker, buy_quantity)
    return buy_result

# print(decide_positions_actions())
