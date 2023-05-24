import alpaca_trade_api as tradeapi
import config
import pandas as pd

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url='https://paper-api.alpaca.markets')

def get_latest_order_date():   
    orders = api.list_orders(status='all')

    order_date = {}

    for order in orders:
        if order.filled_at:
            filled_date = pd.Timestamp(order.filled_at).date()
            if order.symbol not in order_date or filled_date > order_date[order.symbol]:
                order_date[order.symbol] = filled_date

    return order_date

