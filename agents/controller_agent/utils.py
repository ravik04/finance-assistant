import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# from agents.common.audio_utils import speak_summary


import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

def summarize_earnings_pipeline(ticker: str, earnings_data: dict) -> dict:
    if not earnings_data:
        return {"ticker": ticker, "summary": "No data available."}

    prompt = f""" You are a financial analyst. Given the following earnings data for {ticker}, provide a clear, concise, and insightful summary(in 50 words):
    {earnings_data} give me brief, not too much long story."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            return {
                "error": f"Groq API failed: {response.status_code}",
                "details": response.text
            }

        result = response.json()
        message = result['choices'][0]['message']['content']
        return {"ticker": ticker, "summary": message.strip()}

    except Exception as e:
        return {"error": "Unexpected error occurred", "details": str(e)}
