from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from hub import tc

class Order:
    def __init__(self, ticker, quantity):
        self.ticker = ticker
        self.quantity = quantity
      
    def buy_order(self):
        market_order_data = MarketOrderRequest(
                            symbol = self.ticker,
                            qty = self.quantity,
                            type = 'market',
                            side = OrderSide.BUY,
                            time_in_force = TimeInForce.GTC
                        )

        market_order = tc.submit_order(market_order_data)
   
    # Think about stop loss later
    def sell_order(self):
        market_order_data = MarketOrderRequest(
                            symbol = self.ticker,
                            qty = self.quantity,
                            type = 'market',
                            side = OrderSide.SELL,
                            # stop loss ??
                            time_in_force = TimeInForce.GTC
                        )

        market_order = tc.submit_order(market_order_data)
        