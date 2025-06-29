import pandas as pd

class MeanReversionStrategies:
    def __init__(self, window_size):
        self.window_size = window_size

    def bollinger_band_reversion(self, prices: pd.Series):
        signals = [0] * len(prices)
        mean = prices.rolling(self.window_size).mean()
        std = prices.rolling(self.window_size).std()
        for i in range(self.window_size, len(prices)):
            lower_band = mean.iloc[i] - 2 * std.iloc[i]
            upper_band = mean.iloc[i] + 2 * std.iloc[i]
            if prices.iloc[i] < lower_band:
                signals[i] = 1
            elif prices.iloc[i] > upper_band:
                signals[i] = -1
            else:
                signals[i] = 0
        return signals

    def moving_average_crossover(self, prices: pd.Series):
        signals = [0] * len(prices)
        short_ma = prices.rolling(window=self.window_size).mean()
        long_ma = prices.rolling(window=self.window_size * 3).mean()
        for i in range(self.window_size * 3, len(prices)):
            if short_ma.iloc[i] > long_ma.iloc[i] and short_ma.iloc[i-1] <= long_ma.iloc[i-1]:
                signals[i] = 1
            elif short_ma.iloc[i] < long_ma.iloc[i] and short_ma.iloc[i-1] >= long_ma.iloc[i-1]:
                signals[i] = -1
            else:
                signals[i] = 0
        return signals

    def rsi_reversion(self, prices: pd.Series, lower_threshold=30, upper_threshold=70):
        signals = [0] * len(prices)
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(self.window_size).mean()
        avg_loss = loss.rolling(self.window_size).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))

        for i in range(self.window_size, len(prices)):
            if rsi.iloc[i] < lower_threshold:
                signals[i] = 1
            elif rsi.iloc[i] > upper_threshold:
                signals[i] = -1
            else:
                signals[i] = 0
        return signals
