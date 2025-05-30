import requests

FINNHUB_API_KEY = "d0sm7t9r01qg1sj9beogd0sm7t9r01qg1sj9bep0"  # ← Replace with your key

def fetch_relevant_news(ticker: str):
    try:
        # Remove exchange suffix (Finnhub uses base ticker)
        base_ticker = ticker.split(".")[0]  # "TCS.NS" → "TCS"
        
        url = f"https://finnhub.io/api/v1/company-news?symbol={base_ticker}&from=2025-05-25&to=2025-05-30&token={FINNHUB_API_KEY}"
        
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"Finnhub API error: {response.status_code}"}

        news_items = response.json()
        if not news_items:
            return {"ticker": ticker, "headlines": ["No recent news found."]}

        headlines = [item["headline"] for item in news_items[:5] if item.get("headline")]
        return {"ticker": ticker, "headlines": headlines}

    except Exception as e:
        return {"error": str(e)}














# import requests
# from bs4 import BeautifulSoup

# def fetch_relevant_news(ticker: str):
#     url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
#     headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Connection": "keep-alive",
#     }


#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code != 200:
#             return {"error": f"Failed to fetch news: {response.status_code}"}

#         soup = BeautifulSoup(response.text, "html.parser")

#         headlines = []
#         for h3 in soup.find_all("h3"):
#             text = h3.get_text(strip=True)
#             if text and "..." not in text and len(text) > 30:
#                 headlines.append(text)

#         if not headlines:
#             return {"ticker": ticker, "headlines": ["No relevant headlines found."]}

#         return {"ticker": ticker, "headlines": headlines[:10]}  # return top 5

#     except Exception as e:
#         return {"error": str(e)}
