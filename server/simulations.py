import numpy as np
import yfinance as yf

# receives a begin stock price , the amount of steps ,volatility and drift
# returns a list  
# steps here is the amount of days
def simulate_daily_stock(x0,steps,drift=0.0005,volatility=0.01):
    stock_data = [x0]
    for _ in range(steps):
        shock = np.random.normal(loc=drift,scale=volatility)
        stock_data.append(stock_data[-1] * (1 + shock))

    return stock_data


def get_historical_data(ticker, start, end):
    """
    Haalt historische data op voor een gegeven ticker tussen start- en einddatum.

    Parameters:
        ticker (str): De ticker van het aandeel (bv. 'AAPL', 'MSFT').
        start (str): Startdatum in 'YYYY-MM-DD'-formaat.
        end (str): Einddatum in 'YYYY-MM-DD'-formaat.

    Returns:
        pandas.DataFrame: DataFrame met Open, High, Low, Close, Adj Close, Volume.
    """
    data = yf.download(ticker, start=start, end=end,auto_adjust=False)
    return data
