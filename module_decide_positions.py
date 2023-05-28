import module_scan_account
import module_get_last_trade_date
from module_order import Order
import pandas as pd
from datetime import date
import parameters

def decide_positions():
    # Get positions information
    positions, num_positions, available_equity = module_scan_account.scan_account()

    # Run technical analysis on all holding tickers
    analysis_result = module_scan_account.run_ta(positions)

    # Get latest order date (used in sell)
    latest_order = module_get_last_trade_date.get_latest_order_date()

    # Combine info into a new data frame.
    df1 = pd.DataFrame.from_dict(positions, orient='index', columns=['Holding price', 'Quantity'])
    df2 = pd.DataFrame.from_dict(analysis_result, orient='index', columns=['Action', 'Last price'])
    df3 = pd.DataFrame.from_dict(latest_order, orient='index', columns=['Last order date'])

    position_df = pd.merge(df1, df2, left_index=True, right_index=True)
    position_df = pd.merge(position_df, df3, left_index=True, right_index=True)
        
    # Holding price Quantity Action  Last price Last order date
    # AAPL       173.105        2   None  175.160004      2023-05-15
    # AMZN        118.35        3   None  116.250000      2023-05-18

    # Decide actions for positions.
    position_sell, position_buy = [], []
    sells_left = 3
    for i in range(len(position_df)):
        # Get commmon variables
        ticker = position_df.index[i]
        holding_price = float(position_df['Holding price'].iloc[i])
        holding_quantity = int(position_df['Quantity'].iloc[i])
        cur_price = float(position_df['Last price'].iloc[i])
        last_trade_date = position_df['Last order date'].iloc[i]
        
        # If we have a sell signal
        if position_df['Action'].iloc[i] == "Sell":             
            # Check selling conditions: ten days or 10% gain
            days_gone = (date.today() - last_trade_date).days
            if days_gone < 10 or cur_price < holding_price * (1 + parameters.profit_threshold): 
                continue

            # calculate sell_quantity
            sell_quantity = holding_quantity // sells_left
            remainder = holding_quantity - sell_quantity

            # Place the order
            place = Order()
            place.sell_order(ticker, sell_quantity)

            # Update quantity and sells left
            holding_quantity = remainder
            sells_left -= 1
            if holding_quantity == 0:
                sells_left = 3

            position_sell.append((ticker, sell_quantity))
        
        # if we have a buy signal 
        if position_df['Action'].iloc[i] == "Buy": 
            # Check if we are allowed to buy
            if available_equity / parameters.total_equity > parameters.invest_ratio and \
                cur_price <= holding_price * parameters.rebuy_tolerance:
                buy_quantity = holding_quantity * 2
                place = Order()
                place.buy_order(ticker, buy_quantity)

                position_buy.append((ticker, buy_quantity))

    return position_sell, position_buy

# decidePositions()