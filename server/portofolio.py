from trader import Trader

class Portfolio:
    def __init__(self, trader: Trader):
        self.trader = trader
        self.starting_cash = trader.cash
        self.history = []  # to track portfolio value over time

    def update(self, current_price):
        total_value = self.trader.cash + self.trader.holdings * current_price
        self.history.append(total_value)
        return total_value

    def current_value(self, current_price):
        return self.trader.cash + self.trader.holdings * current_price

    def return_percent(self, current_price):
        total_value = self.current_value(current_price)
        return (total_value - self.starting_cash) / self.starting_cash * 100

    def print_summary(self, current_price):
        total_value = self.current_value(current_price)
        ret = self.return_percent(current_price)
        print(f"Portfolio Value: {total_value:.2f}, Return: {ret:.2f}%")
