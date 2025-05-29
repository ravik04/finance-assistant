import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

def summarize_headlines(ticker, headlines):
    prompt = f"""Summarize(in short 50 words) the following recent news headlines for {ticker} into a single clear and concise paragraph:\n\n """
    for headline in headlines:
        prompt += f"- {headline}\n"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        data = response.json()

        if response.status_code != 200:
            return f"Groq API error: {data.get('error', {}).get('message', 'Unknown error')}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error summarizing: {str(e)}"
