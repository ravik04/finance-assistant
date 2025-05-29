import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "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"

def analyze_sentiment(ticker, earnings_summary, news_summary):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f""" You are a financial analyst. Based on the following information, generate a concise investment insight for {ticker}. Indicate if the outlook is bullish, bearish, or neutral and explain why.
    Earnings Summary: {earnings_summary}
    News Summary: {news_summary}
    Give a short analysis under 50 words."""

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API failed: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()
