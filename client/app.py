import streamlit as st
import requests

st.title("📈 Trading Bot Backtester")

mode = st.selectbox("Kies backtest type:", ["Historisch", "Simulatie"])

# Checkbox of bot automatisch strategie kiest
auto_strategy = st.checkbox("Bot kiest strategie automatisch", value=False)

strategies = ["Bollinger Bands", "Moving Average Crossover", "RSI"]
if not auto_strategy:
    strategy = st.selectbox("Kies strategie:", strategies)
else:
    strategy = None  # Geen keuze nodig, bot kiest

if mode == "Historisch":
    st.subheader("Historische Backtest")
    ticker = st.text_input("Ticker", "TSLA")
    start = st.date_input("Startdatum")
    end = st.date_input("Einddatum")
    window = st.slider("Window size", 5, 50, 20)

    if st.button("Run Backtest"):
        payload = {
            "ticker": ticker,
            "start_date": str(start),
            "end_date": str(end),
            "window_size": window,
            "auto_strategy": auto_strategy,
        }
        if not auto_strategy:
            payload["strategy"] = strategy

        response = requests.post("http://localhost:8000/historical_backtest", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Totaal vermogen: ${result['total_equity']}")
            st.info(f"Rendement: {result['return_percent']}%")
            st.line_chart(result["prices"])
        else:
            st.error(f"Fout bij backtest: {response.text}")

elif mode == "Simulatie":
    st.subheader("Simulatie Backtest")
    x0 = st.number_input("Startprijs", 50.0, 500.0, 100.0)
    steps = st.slider("Aantal stappen", 30, 1000, 365)
    window = st.slider("Window size", 5, 50, 15)

    if st.button("Run Simulatie"):
        payload = {
            "x0": x0,
            "steps": steps,
            "window_size": window,
            "auto_strategy": auto_strategy,
        }
        if not auto_strategy:
            payload["strategy"] = strategy

        response = requests.post("http://localhost:8000/simulation_backtest", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Totaal vermogen: ${result['total_equity']}")
            st.info(f"Rendement: {result['return_percent']}%")
            st.line_chart(result["prices"])
        else:
            st.error(f"Fout bij simulatie: {response.text}")
