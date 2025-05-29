import requests
from bs4 import BeautifulSoup

ALPHA_VANTAGE_API_KEY = "E4PBTRLJNZDTBU6H"

def get_earnings_alpha_vantage(ticker: str):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "Alpha Vantage API request failed"}

        data = response.json()

        if "quarterlyEarnings" not in data or not data["quarterlyEarnings"]:
            return {"error": "No earnings data found for the ticker."}

        latest = data["quarterlyEarnings"][0]
        actual = float(latest.get("reportedEPS", 0))
        estimate = float(latest.get("estimatedEPS", 0))
        date = latest.get("fiscalDateEnding", "Unknown")

        if actual > estimate:
            sentiment = f"Beat estimates by {round(actual - estimate, 2)} EPS"
        elif actual < estimate:
            sentiment = f"Missed estimates by {round(estimate - actual, 2)} EPS"
        else:
            sentiment = "Met estimates"

        return {
            "earnings": [{
                "symbol": ticker,
                "epsEstimate": estimate,
                "epsActual": actual,
                "sentiment": sentiment,
                "date": date
            }]
        }

    except Exception as e:
        return {"error": str(e)}


def scrape_yahoo_earnings_headlines(ticker: str):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Failed to retrieve Yahoo Finance page. Code: {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []

        for tag in soup.find_all("h3"):
            text = tag.get_text(strip=True)
            if "earnings" in text.lower():
                headlines.append(text)

        if not headlines:
            return {"info": "No earnings-related headlines found"}

        return {"earnings_headlines": headlines[:5]}  # Limit to 5 headlines

    except Exception as e:
        return {"error": str(e)}


def get_earnings_or_headlines(ticker: str):
    # Try Alpha Vantage first
    api_result = get_earnings_alpha_vantage(ticker)
    if "earnings" in api_result and api_result["earnings"]:
        return api_result

    # Fallback to Yahoo headlines
    return scrape_yahoo_earnings_headlines(ticker)







#before vesion- correct

# import requests
# from bs4 import BeautifulSoup

# # OPTIONAL: Add your Finnhub API key
# API_KEY = "d0r1hu1r01qn4tjfsuegd0r1hu1r01qn4tjfsuf0"  # Replace with your actual key or leave empty

# def get_earnings_finnhub(ticker: str):
#     if not API_KEY:
#         return {"info": "No API key provided. Skipping Finnhub."}

#     url = f"https://finnhub.io/api/v1/calendar/earnings?symbol={ticker}&token={API_KEY}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return {"error": "Finnhub API request failed"}

#     data = response.json()
#     earnings = data.get("earningsCalendar", [])

#     if not earnings:
#         return {"info": "No earnings data from API"}

#     result = []
#     for item in earnings[:3]:  # Limit to 3 results
#         estimate = item.get("epsEstimate")
#         actual = item.get("epsActual")
#         surprise = item.get("surprise")
#         surprise_percent = item.get("surprisePercent")

#         # Determine sentiment
#         if actual is not None and estimate is not None:
#             if actual > estimate:
#                 sentiment = f"Beat estimates by {round(actual - estimate, 2)} EPS ({round(surprise_percent or 0, 2)}%)"
#             elif actual < estimate:
#                 sentiment = f"Missed estimates by {round(estimate - actual, 2)} EPS ({round(surprise_percent or 0, 2)}%)"
#             else:
#                 sentiment = "Met estimates"
#         else:
#             sentiment = "Sentiment not available"

#         result.append({
#             "symbol": item.get("symbol"),
#             "epsEstimate": estimate,
#             "epsActual": actual,
#             "surprise": surprise,
#             "surprisePercent": surprise_percent,
#             "sentiment": sentiment,
#             "date": item.get("date")
#         })

#     return {"earnings": result}


# def scrape_yahoo_earnings_headlines(ticker: str):
#     url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#         "Accept-Language": "en-US,en;q=0.9",
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             return {"error": f"Failed to retrieve Yahoo Finance page. Code: {response.status_code}"}

#         soup = BeautifulSoup(response.text, "html.parser")
#         headlines = []

#         for tag in soup.find_all("h3"):
#             text = tag.get_text(strip=True)
#             if "earnings" in text.lower():
#                 headlines.append(text)

#         if not headlines:
#             return {"info": "No earnings-related headlines found"}

#         return {"earnings_headlines": headlines[:5]}  # limit to 5

#     except Exception as e:
#         return {"error": str(e)}


# def get_earnings_or_headlines(ticker: str):
#     # Try Finnhub API for U.S. tickers
#     api_result = get_earnings_finnhub(ticker)
#     if "earnings" in api_result and api_result["earnings"]:
#         return api_result

#     # Fallback to Yahoo News headlines
#     return scrape_yahoo_earnings_headlines(ticker)





# import requests
# from bs4 import BeautifulSoup

# # OPTIONAL: Add your Finnhub API key if you want U.S. earnings data
# API_KEY = "d0r1hu1r01qn4tjfsuegd0r1hu1r01qn4tjfsuf0"  # Replace with your actual key or leave empty

# def get_earnings_finnhub(ticker: str):
#     if not API_KEY:
#         return {"info": "No API key provided. Skipping Finnhub."}

#     url = f"https://finnhub.io/api/v1/calendar/earnings?symbol={ticker}&token={API_KEY}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return {"error": "Finnhub API request failed"}

#     data = response.json()
#     earnings = data.get("earningsCalendar", [])

#     if not earnings:
#         return {"info": "No earnings data from API"}

#     result = []
#     for item in earnings[:3]:  # Limit to 3 results
#         result.append({
#             "symbol": item.get("symbol"),
#             "epsEstimate": item.get("epsEstimate"),
#             "epsActual": item.get("epsActual"),
#             "surprise": item.get("surprise"),
#             "surprisePercent": item.get("surprisePercent"),
#             "date": item.get("date")
#         })

#     return {"earnings": result}


# import xml.etree.ElementTree as ET

# def scrape_yahoo_earnings_headlines(ticker: str):
#     rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

#     try:
#         headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#     "Accept-Language": "en-US,en;q=0.9",}

#         response = requests.get(rss_url, headers=headers)

#         if response.status_code != 200:
#             return {"error": f"Failed to load RSS feed. Status: {response.status_code}"}

#         root = ET.fromstring(response.content)
#         items = root.findall(".//item")
#         earnings_headlines = []

#         for item in items:
#             title = item.find("title").text
#             if "earnings" in title.lower():
#                 earnings_headlines.append(title)

#         if not earnings_headlines:
#             return {"info": "No earnings-related headlines found in RSS feed"}

#         return {"earnings_headlines": earnings_headlines[:5]}

#     except Exception as e:
#         return {"error": str(e)}




# def get_earnings_or_headlines(ticker: str):
#     # Try Finnhub API for U.S. tickers
#     api_result = get_earnings_finnhub(ticker)
#     if "earnings" in api_result and api_result["earnings"]:
#         return api_result

#     # Fallback to Yahoo News headlines
#     return scrape_yahoo_earnings_headlines(ticker)

# import requests
# from bs4 import BeautifulSoup

# def scrape_yahoo_earnings_headlines(ticker: str):
#     feed_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
#     try:
#         response = requests.get(feed_url, headers={"User-Agent": "Mozilla/5.0"})
#         if response.status_code != 200:
#             return {"error": f"Failed to load RSS feed. Status: {response.status_code}"}
#     except Exception as e:
#         return {"error": str(e)}

#     soup = BeautifulSoup(response.content, "xml")
#     items = soup.find_all("item")

#     earnings_news = []
#     for item in items:
#         title_tag = item.find("title")
#         if title_tag and "earnings" in title_tag.text.lower():
#             earnings_news.append(title_tag.text.strip())

#     if not earnings_news:
#         return {"info": "No earnings-related headlines found"}

#     return {"earnings_headlines": earnings_news}
