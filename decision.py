import pandas as pd
import yfinance as yf
from datetime import date
import json
import os

from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus

from hub import tc, ta
from order import Order
import parameters

# from technical_analysis import TechnicalAnalysis

class Decision:
    def __init__(self):
        # self.ta = TechnicalAnalysis(None)
        self.portfolio = {}
        self.portfolio_df = None

    def update_portfolio(self):
        self._generate_portfolio_df()
        available_cash = self.portfolio["available_cash"]
        num_positions = self.portfolio["num_positions"]

        positions_sell, positions_buy = [], []

        for i in range(len(self.portfolio_df)):
            position = {
                "ticker": self.portfolio_df.index[i],
                "holding_price": float(self.portfolio_df['Holding price'].iloc[i]),
                "holding_quantity": int(self.portfolio_df['Quantity'].iloc[i]),
                "current_price": float(self.portfolio_df['Last price'].iloc[i]),
                "action": self.portfolio_df['Action'].iloc[i],
            }

            if position['Action'].iloc[i] == "Sell":
                sell = self._sell_portfolio_stocks(position)
                if sell:
                    positions_sell.append(sell)

            if position['Action'].iloc[i] == "Buy":
                buy = self._buy_portfolio_stocks(position, available_cash, num_positions)
                if buy:
                    positions_buy.append(buy)

        return positions_sell, positions_buy # For the report

    def screen_new_candidates(self):
        # Get positions information
        self._scan_account()
        holding_positions = self.portfolio["holding_positions"]

        frame = pd.read_csv('candidates_Nasdaq.csv')

        potential_buy = []
        for ticker in frame['symbol']:
            # For ticker in positions, we already did everything in scan_portfolio.
            if ticker in holding_positions:
                continue

            # For other tickers, download data and run technical analysis for buy signals
            try:
                df = yf.download(ticker, start='2022-09-01')
                print(f'Running technical analysis on {ticker}...')
                ta.good_to_buy()

                if df.iloc[-1]['good_to_buy'] == True:
                    potential_buy.append((ticker, df.iloc[-1]['Close']))

            except:
                continue

        return potential_buy

    def _generate_portfolio_df(self):
        '''
        Generate a concise portfolio dataframe:
              Holding price  Quantity Action  Last price
        BIIB     277.386282        78   None  256.540009
        CSCO      52.500000       398   None   49.439999
        EBAY      44.389204       490   None   42.650002
        '''
        # Get positions information
        self._scan_account()
        holding_positions = self.portfolio["holding_positions"]

        # Run technical analysis on all holding tickers
        analysis_result = self._run_techincal_analysis(holding_positions)

        # Combine info into a new data frame
        df1 = pd.DataFrame.from_dict(holding_positions, orient='index', columns=[
                                    'Holding price', 'Quantity'])
        df2 = pd.DataFrame.from_dict(analysis_result, orient='index', columns=[
                                    'Action', 'Last price'])

        self.portfolio_df = pd.merge(df1, df2, left_index=True, right_index=True)

    def _sell_portfolio_stocks(self, position):
        current_price = position["current_price"]
        holding_price = position["holding_price"]
        holding_quantity = position["holding_quantity"]
        ticker = position["ticker"]

        '''
        Exit sell if profit target is not met or an order was fired yesterday 
        to avoid early exit during consolidation
        '''
        pending_orders = self._get_pending_orders()

        if (
            current_price < holding_price * (1 + parameters.profit_target) or \
            ticker in pending_orders
        ):
            return
        
        order = Order(ticker, holding_quantity)

        # Sell all if quantity is too small
        if holding_quantity <= 3:
            order.sell_order()
            return ticker, holding_quantity

        # File to track selling state
        json_file = f'selling_{ticker}.json'
        selling_state = {}

        # Load existing selling state if it exists
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as file:
                    selling_state = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                pass

        # Determine sell quantity based on selling state
        if ticker not in selling_state:
            # First: sell half
            sell_quantity = holding_quantity // 2
            selling_state[ticker] = 1
            with open(json_file, 'w') as file:
                json.dump(selling_state, file)
        else:
            # Finaly: sell the rest
            sell_quantity = holding_quantity
            if os.path.exists(json_file):
                os.remove(json_file)

        order.sell_order()

        return ticker, sell_quantity

    def _buy_portfolio_stocks(self, position):
        current_price = position["current_price"]
        holding_price = position["holding_price"]
        holding_quantity = position["holding_quantity"]
        ticker = position["ticker"]
        available_cash = position["available_cash"]

        # Check if we are allowed to buy
        if (
            available_cash / parameters.total_equity < parameters.invest_ratio or \
            current_price > holding_price * parameters.rebuy_tolerance # num_positions >= 3: not to use it for more frequent testing
        ):
            return

        buy_quantity = holding_quantity * 2
        order = Order(ticker, buy_quantity)

        # Avoid repeating filing the same order as yesterday.
        pending_orders = self._get_pending_orders()

        if ticker not in pending_orders:
            order.buy_order()

        return ticker, buy_quantity
    
    def _get_pending_orders(self):
        # Get pending orders
        open_orders = GetOrdersRequest(status=QueryOrderStatus.OPEN)

        # Pending_orders is a list. A class object is at index 0 in this list.
        pending_orders = tc.get_orders(filter=open_orders)

        if not pending_orders:
            return {}

        result = {}
        for order in pending_orders:
            ticker = order.symbol
            quantity = order.qty
            if ticker not in result:
                result[ticker] = 0
            result[ticker] = quantity

        return result

    def _get_latest_order_date(self):
        all_orders = GetOrdersRequest(status=QueryOrderStatus.ALL)
        orders = tc.get_orders(filter=all_orders)

        order_date = {}
        for order in orders:
            if order.filled_at:
                filled_date = pd.Timestamp(order.filled_at).date()
                if order.symbol not in order_date or filled_date > order_date[order.symbol]:
                    order_date[order.symbol] = filled_date

        return order_date

    def _run_techincal_analysis(self):
        holding_positions = self.account["holding_positions"]
        analysis_result = {}

        for ticker in holding_positions:
            df = yf.download(ticker, start='2022-01-01')
            print(f'Running technical analysis on {ticker}...')
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

    def _scan_account(self):
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

        # Construct the portfolio object
        self.portfolio = {
            "holding_positions": holding_positions,
            "num_positions": num_positions,
            "available_cash": available_cash,
            "total_equity": total_equity
        }
