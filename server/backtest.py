from simulations import get_historical_data,simulate_daily_stock
import pandas as pd
import strategies as strategies
from trader import Trader
from order_book import OrderBook
import logging_config
from portofolio import Portfolio


def run_historical_backtest(
    ticker: str = "TSLA",
    start_date: str = "2024-01-01",
    end_date: str = "2025-01-01",
    window_size: int = 20,
    strategy: str = "Bollinger Bands"
) -> dict:
    df = get_historical_data(ticker, start_date, end_date)
    prices = df[("Close", ticker)].tolist()
    stock_data_series = pd.Series(df[("Close", ticker)])

    mean_reversion_strategies = strategies.MeanReversionStrategies(window_size)

    if strategy.lower() == "bollinger bands":
        signals = mean_reversion_strategies.bollinger_band_reversion(stock_data_series)[window_size:]
    elif strategy.lower() == "moving average crossover":
        signals = mean_reversion_strategies.moving_average_crossover(stock_data_series)[window_size*3:]
        # pas slicing aan door langere window size
        prices = prices[window_size*3:]
    else:
        raise ValueError(f"Onbekende strategie: {strategy}")

    orderbook = OrderBook()
    trader = Trader("trader0")
    trader.trade(prices, signals, orderbook)

    current_price = prices[-1]
    total_equity = trader.cash + trader.holdings * current_price
    return_percent = (total_equity - 10000) / 10000 * 100

    return {
        "total_equity": round(total_equity, 2),
        "return_percent": round(return_percent, 2),
        "prices": prices,
        "trader": {
            "cash": trader.cash,
            "holdings": trader.holdings,
        }
    }

def run_simulation_backtest(
    x0: float = 100,
    steps: int = 365,
    window_size: int = 15,
    strategy: str = "Bollinger Bands"
) -> dict:
    prices = simulate_daily_stock(x0=x0, steps=steps)
    stock_data_series = pd.Series(prices)

    mean_reversion_strategies = strategies.MeanReversionStrategies(window_size)

    if strategy.lower() == "bollinger bands":
        signals = mean_reversion_strategies.bollinger_band_reversion(stock_data_series)[window_size:]
    elif strategy.lower() == "moving average crossover":
        signals = mean_reversion_strategies.moving_average_crossover(stock_data_series)[window_size*3:]
        prices = prices[window_size*3:]
    else:
        raise ValueError(f"Onbekende strategie: {strategy}")

    orderbook = OrderBook()
    trader = Trader("trader0")
    trader.trade(prices, signals, orderbook)

    current_price = prices[-1]
    total_equity = trader.cash + trader.holdings * current_price
    return_percent = (total_equity - 10000) / 10000 * 100

    return {
        "total_equity": round(total_equity, 2),
        "return_percent": round(return_percent, 2),
        "prices": prices,
        "trader": {
            "cash": trader.cash,
            "holdings": trader.holdings,
        }
    }




if __name__ == "__main__":
    result = run_historical_backtest(ticker="AAPL")
    print(f"Totaal vermogen: ${result['total_equity']}")
    print(f"Rendement: {result['return_percent']}%")


    result = run_simulation_backtest()
    print(f"Totaal vermogen: ${result['total_equity']}")
    print(f"Rendement: {result['return_percent']}%")

