from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
import pandas as pd
import config

tc = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)

def get_latest_order_date():   
    all_orders = GetOrdersRequest(status=QueryOrderStatus.ALL)
    orders = tc.get_orders(filter=all_orders)

    order_date = {}
    for order in orders:
        if order.filled_at:
            filled_date = pd.Timestamp(order.filled_at).date()
            if order.symbol not in order_date or filled_date > order_date[order.symbol]:
                order_date[order.symbol] = filled_date

    return order_date
