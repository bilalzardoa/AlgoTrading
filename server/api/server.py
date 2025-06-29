import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging_config
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from backtest import run_historical_backtest, run_simulation_backtest

app = FastAPI()

class HistoricalRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    window_size: int = 20
    auto_strategy: Optional[bool] = False
    strategy: Optional[str] = None

class SimulationRequest(BaseModel):
    x0: float = 100
    steps: int = 365
    window_size: int = 15
    auto_strategy: Optional[bool] = False
    strategy: Optional[str] = None

@app.post("/historical_backtest")
def historical_backtest(request: HistoricalRequest):
    # Kies strategie als auto_strategy True is
    if request.auto_strategy:
        chosen_strategy = auto_choose_strategy_historical()
    else:
        chosen_strategy = request.strategy or "Bollinger Bands"

    result = run_historical_backtest(
        ticker=request.ticker,
        start_date=request.start_date,
        end_date=request.end_date,
        window_size=request.window_size,
        strategy=chosen_strategy
    )
    return result

@app.post("/simulation_backtest")
def simulation_backtest(request: SimulationRequest):
    if request.auto_strategy:
        chosen_strategy = auto_choose_strategy_simulation()
    else:
        chosen_strategy = request.strategy or "Bollinger Bands"

    result = run_simulation_backtest(
        x0=request.x0,
        steps=request.steps,
        window_size=request.window_size,
        strategy=chosen_strategy
    )
    return result

def auto_choose_strategy_historical() -> str:
    # Dummy logica voor automatische keuze historische data
    # Je kan hier bv. statistieken of andere parameters gebruiken
    return "Bollinger Bands"

def auto_choose_strategy_simulation() -> str:
    # Dummy logica voor automatische keuze simulatie
    return "Moving Average Crossover"
