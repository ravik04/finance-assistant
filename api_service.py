from fastapi import FastAPI, Query
from typing import List
from api_agent import get_tech_stock_data

app = FastAPI()

@app.get("/tech-stocks")
def tech_stocks(tickers: List[str] = Query(...)):
    return get_tech_stock_data(tickers)
