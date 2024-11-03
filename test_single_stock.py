import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import parameters
from hub import ta

start_date = '2022-01-01'
start_date = pd.to_datetime(start_date)
# df = yf.download('FANG', start_date)
df = yf.download('GILD', start='2022-05-25')

def trade(df, equity, invest_ratio, rebuy_tolerance, profit_threshold):
    ta.good_to_buy()
    ta.good_to_sell()

    Buy_dates = [] 
    Sell_dates = []
    trade_profit = 0
    total_profit = 0
    open_pos = [] # [('price1', 'quantity1', 'date1')]
    attempt = 0
    sells_left = 2

    for i in range(len(df) - 1):    
        cur_price = df['Close'].iloc[i]
        cur_date = df.index[i]

        if df['good_to_buy'].iloc[i] == True:           
            buy_price = df['Open'].iloc[i + 1]       
            buy_quantity = equity * invest_ratio // buy_price
            buy_date = df.iloc[i + 1].name

            if not open_pos:
                Buy_dates.append(buy_date)
                open_pos.append((buy_price, buy_quantity, buy_date))
                attempt += 1
                print('开仓', open_pos)
                continue
            
            holding_price, holding_quantity, last_trade_date = open_pos[0]           
            if cur_price <= holding_price * rebuy_tolerance and attempt < 2:           
                new_quantity = holding_quantity * 3   
                new_price = (holding_quantity * holding_price + buy_price * holding_quantity * 2) / new_quantity       
                Buy_dates.append(buy_date)
                open_pos[0] = (new_price, new_quantity, buy_date)              
                print('加仓', open_pos)
                attempt += 1

        if df['good_to_sell'].iloc[i] == True:  
            if not open_pos:
                continue
            
            sell_price = df['Open'].iloc[i + 1]
            sell_date = df.iloc[i + 1].name
            holding_price, holding_quantity, last_trade_date = open_pos[0]

            # Check if price hits the stop loss (50% of holding price)
            if cur_price <= holding_price * 0.5:
                Sell_dates.append(sell_date)
                open_pos.pop()
                loss = holding_quantity * (sell_price - holding_price)
                trade_profit -= loss
            
            # Check selling conditions: ten days or 10% gain
            days_gone = (cur_date.date() - last_trade_date.date()).days
            if days_gone < 3 or cur_price < holding_price * (1 + profit_threshold): 
                continue
            
            Sell_dates.append(sell_date)               
            sell_quantity = holding_quantity // sells_left           
            remainder = holding_quantity - sell_quantity             
            
            gain = (sell_price - holding_price) * sell_quantity
            trade_profit += gain
            print('Sold price/quantity', sell_price, sell_quantity)

            # Update
            holding_quantity = remainder
            sells_left -= 1

            if holding_quantity == 0:
                attempt = 0
                open_pos = []
                total_profit += trade_profit
                print('This trade made', trade_profit)
                equity += trade_profit 
                print('Now the account has', equity)           
                trade_profit = 0
                gain = 0
                loss = 0
                sells_left = 2
                continue
            else:          
                last_trade_date = df.index[i + 1]
                open_pos[0] = holding_price, holding_quantity, last_trade_date
                
    return Buy_dates, Sell_dates, total_profit, equity

Buy_dates, Sell_dates, total_profit, equity = trade(df, 
                                                    parameters.total_equity, 
                                                    parameters.invest_ratio, 
                                                    parameters.rebuy_tolerance, 
                                                    parameters.profit_target)

plt.scatter(df.loc[Buy_dates].index, df.loc[Buy_dates]['Close'], marker='^', c='g')
plt.scatter(df.loc[Sell_dates].index, df.loc[Sell_dates]['Open'], marker='v', c='r')
plt.plot(df['Close'], alpha=0.5)
plt.show()

print(int(total_profit), int(equity))