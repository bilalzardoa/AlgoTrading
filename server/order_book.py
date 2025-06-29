import heapq
import logging
import os


logger = logging.getLogger('trading')


class Order:
    def __init__(self, order_id, side, price, quantity):
        self.id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity

class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.order_id = 0

    
    def place_limit_order(self, side, price, quantity):
        self.order_id += 1
        order = Order(self.order_id, side, price, quantity)
        
        if side == "buy":
            heapq.heappush(self.bids, (-price, self.order_id, order))
        else:
            heapq.heappush(self.asks, (price, self.order_id, order))
        
        self.match_orders()

    def match_orders(self):
        while self.bids and self.asks:
            best_bid_price, _, buy_order = self.bids[0]
            best_ask_price, _, sell_order = self.asks[0]

            if -best_bid_price >= best_ask_price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                trade_price = best_ask_price

                logger.info(
                    f"TRADE: {trade_quantity} units @ {trade_price} between Buy#{buy_order.id} and Sell#{sell_order.id}"
                )

                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity

                if buy_order.quantity == 0:
                    heapq.heappop(self.bids)
                if sell_order.quantity == 0:
                    heapq.heappop(self.asks)
            else:
                break

# === Testrun ===
if __name__ == "__main__":
    ob = OrderBook()
    ob.place_limit_order("buy", 100, 10)
    ob.place_limit_order("sell", 102, 5)
    ob.place_limit_order("sell", 99, 7)  # Triggert trade
