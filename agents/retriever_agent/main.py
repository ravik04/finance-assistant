from fastapi import FastAPI, Query
from utils import fetch_relevant_news

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Retriever Agent is running!"}

@app.get("/news/")
def get_news(ticker: str = Query(..., description="Ticker symbol")):
    return fetch_relevant_news(ticker)
