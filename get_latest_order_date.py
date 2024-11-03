from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
import pandas as pd
from client import tc

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

def get_pending_orders():
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

# print(get_pending_orders())
# get_latest_order_date()