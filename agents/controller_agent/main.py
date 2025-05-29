from fastapi import FastAPI, Query
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from utils import summarize_earnings_pipeline
from agents.common.audio_utils import speak_summary
# from agents.common.audio_utils import clean_text_for_speech


import re

def format_summary_readable(ticker: str, summary: str) -> str:
    try:
        lines = summary.split("\n")
        company = f"{ticker.upper()}"

        date = ""
        eps_est = ""
        eps_act = ""
        surprise = ""

        for line in lines:
            if "Earnings Date" in line:   
                date = line.split(":")[-1].strip()
            elif "EPS Estimate" in line:
                eps_est = line.split(":")[-1].strip()
            elif "EPS Actual" in line:
                eps_act = line.split(":")[-1].strip()
            elif "Earnings Surprise" in line:
                surprise = line.split(":")[-1].strip()

        
        return (
            f"{summary}"
        )

    except Exception as e:
        return summary  



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Controller Agent is running!"}

@app.get("/summary/")
def earnings(ticker: str = Query(...,  description="Stock ticker symbol")):
    try:
        scraping_agent_url = f"https://scraping-agent-61gh.onrender.com/scrape/?ticker={ticker}"

        response = requests.get(scraping_agent_url)

        if response.status_code != 200:
            return {"error": f"Scraping agent failed: {response.status_code}"}

        data = response.json()

        summary = summarize_earnings_pipeline(ticker, data)

        cleaned_summary = format_summary_readable(ticker, summary.get("summary", ""))

        speak_summary(cleaned_summary)

        return {"ticker": ticker, "summary": summary["summary"]}

    except Exception as e:
        return {"error": str(e)}
