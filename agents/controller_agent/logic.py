# import requests

# SCRAPING_AGENT_URL = "http://localhost:8001/scrape/"

# def get_summary(ticker: str):
#     try:
#         response = requests.get(SCRAPING_AGENT_URL, params={"ticker": ticker})
#         data = response.json()
#     except Exception as e:
#         return {"error": f"Failed to get data: {str(e)}"}

#     if "earnings" in data:
#         item = data["earnings"][0]
#         actual = item.get("epsActual")
#         estimate = item.get("epsEstimate")
#         date = item.get("date")

#         if actual is not None and estimate is not None:
#             diff = actual - estimate
#             pct = (diff / estimate) * 100 if estimate != 0 else 0
#             sentiment = "beat" if diff > 0 else "missed" if diff < 0 else "met"

#             return {
#                 "ticker": ticker.upper(),
#                 "summary": f"On {date}, {ticker.upper()} reported earnings and {sentiment} expectations by {abs(pct):.2f}%."
#             }

#     elif "earnings_headlines" in data:
#         headline = data["earnings_headlines"][0]
#         return {
#             "ticker": ticker.upper(),
#             "summary": f"{ticker.upper()} recent earnings news: \"{headline}\""
#         }

#     return {"ticker": ticker.upper(), "summary": "No earnings data found."}




