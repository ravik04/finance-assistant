from fastapi import FastAPI, Query
from typing import List
from utils import summarize_headlines

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Language Agent is running!"}

@app.get("/summarize/")
def summarize_news(ticker: str = Query(...), headlines: List[str] = Query(...)):
    summary = summarize_headlines(ticker, headlines)
    return {"ticker": ticker, "news_summary": summary}
