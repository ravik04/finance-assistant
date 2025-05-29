from fastapi import FastAPI, Query
from utils import get_earnings_or_headlines

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Scraping Agent is running!"}

@app.get("/scrape/")
def earnings(ticker: str = Query(..., description="Stock ticker symbol (e.g., TSM, AAPL, 005930.KQ)")):
    return get_earnings_or_headlines(ticker)





