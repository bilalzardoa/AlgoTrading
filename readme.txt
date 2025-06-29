# 📊 FinTech Backtesting Platform

Een modulair en uitbreidbaar backtesting-platform geschreven in Python voor financiële strategieën, inclusief ondersteuning voor historische en gesimuleerde data.

---

## 🗂️ Projectstructuur

```
fintech/
├── client/              # Streamlit frontend (optioneel)
├── server/
│   ├── api/             # FastAPI server
│   │   └── server.py
│   ├── backtest.py      # Kernlogica voor backtests
│   ├── simulations.py   # Genereert gesimuleerde stockprijzen
│   ├── strategies.py    # Strategieën zoals Bollinger Bands
│   ├── trader.py        # Trader logica: voert trades uit
│   ├── order_book.py    # Slaat uitgevoerde orders op
│   ├── portofolio.py    # Portfolio tracking (optioneel)
│   └── logging_config.py# Loggingconfiguratie
└── requirements.txt     # Benodigde Python packages
```

---

## 🚀 Functionaliteiten

- ✅ Backtests met **historische data** (via `yfinance`)
- ✅ Backtests met **gesimuleerde data**
- ✅ Ondersteuning voor meerdere strategieën:
  - Bollinger Bands
  - Moving Average Crossover
- 🛠️ Ondersteuning voor **custom strategieën** (zie hieronder)
- 💼 Portfolio en order tracking

---

## ⚙️ Custom Strategieën

Je kunt eenvoudig eigen strategieën toevoegen via `server/strategies.py`.

### ➕ Voorbeeldstrategie toevoegen

```python
class MeanReversionStrategies:
    def __init__(self, window_size: int):
        self.window_size = window_size

    def custom_strategy(self, prices: pd.Series) -> list:
        signals = []
        ma = prices.rolling(window=self.window_size).mean()
        for i in range(len(prices)):
            if i < self.window_size:
                signals.append(0)
                continue
            price = prices[i]
            if price < 0.95 * ma[i]:
                signals.append(1)  # Koop
            elif price > 1.05 * ma[i]:
                signals.append(-1)  # Verkoop
            else:
                signals.append(0)  # Houd
        return signals
```

En in `backtest.py`:

```python
elif strategy.lower() == "custom strategy":
    signals = mean_reversion_strategies.custom_strategy(stock_data_series)[window_size:]
```

---

## 🧪 Voorbeeld Uitvoeren

```bash
cd server
python backtest.py
```

Output:
```
Totaal vermogen: $10,843.55
Rendement: 8.44%
```

---

## 📦 Dependencies installeren

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Auteur

Dit project is ontwikkeld door Bilal Zardoa AI & Data Engineer als een backtesting-tool voor eigen strategieën en simulaties.