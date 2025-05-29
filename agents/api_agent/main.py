from fastapi import FastAPI, Query
from utils import fetch_earnings_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Agent is running!"}

@app.get("/earnings/")
def get_earnings(ticker: str = Query(..., description="Stock ticker symbol")):
    return fetch_earnings_data(ticker)


from utils import fetch_last_5_days_prices

@app.get("/price/")
def get_price(ticker: str = Query(..., description="Stock ticker symbol")):
    return fetch_last_5_days_prices(ticker)
