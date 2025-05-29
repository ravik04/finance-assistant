from fastapi import FastAPI, Query
from typing import List
from utils import run_market_crew

app = FastAPI()

@app.get("/")
def root():
    return {"message": "CrewAI Agent is running!"}

@app.get("/run/")
def run_crew(
    ticker: str = Query(...),
    earnings_summary: str = Query(...),
    headlines: List[str] = Query(...)
):
    try:
        return run_market_crew(ticker, headlines, earnings_summary)
    except Exception as e:
        return {"error": str(e)}
