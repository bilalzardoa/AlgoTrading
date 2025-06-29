from order_book import OrderBook
import logging


logger = logging.getLogger('trading')

class Trader:
    def __init__(self, name, initial_cash=10000):
        self.name = name
        self.cash = initial_cash
        self.holdings = 0

    def trade(self, prices, signals, orderbook: OrderBook):
        for i in range(len(signals)):
            price = prices[i]
            signal = signals[i]

            if signal == 1:
                # Max 5% van cash gebruiken voor koop
                budget = self.cash * 0.05
                quantity = int(budget // price)
                if quantity > 0:
                    orderbook.place_limit_order('buy', price, quantity)
                    self.cash -= quantity * price
                    self.holdings += quantity
                    logger.info(f"[BUY] {quantity} @ {price:.2f} | Cash: {self.cash:.2f} | Holdings: {self.holdings}")

            elif signal == -1:
                if self.holdings > 0:
                    quantity = self.holdings
                    orderbook.place_limit_order('sell', price, quantity)
                    self.cash += quantity * price
                    self.holdings = 0
                    logger.info(f"[SELL] {quantity} @ {price:.2f} | Cash: {self.cash:.2f} | Holdings: {self.holdings}")
