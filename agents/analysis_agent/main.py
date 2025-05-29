from fastapi import FastAPI, Query
from utils import analyze_sentiment

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Analysis Agent is running!"}

@app.get("/analyze/")
def analyze(ticker: str = Query(...), earnings_summary: str = Query(...), news_summary: str = Query(...)):
    try:
        result = analyze_sentiment(ticker, earnings_summary, news_summary)
        return {"ticker": ticker, "analysis": result}
    except Exception as e:
        return {"error": str(e)}
