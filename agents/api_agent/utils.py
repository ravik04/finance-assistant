import requests
import os

ALPHAVANTAGE_API_KEY = "5C54WGKVH11Y1AQK"
BASE_URL = "https://www.alphavantage.co/query"

def fetch_earnings_data(ticker):
    try:
        params = {
            "function": "EARNINGS",
            "symbol": ticker,
            "apikey": ALPHAVANTAGE_API_KEY
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "quarterlyEarnings" not in data:
            return {"error": "Earnings data not found."}

        latest = data["quarterlyEarnings"][0]
        return {
            "ticker": ticker,
            "fiscalDateEnding": latest["fiscalDateEnding"],
            "reportedEPS": latest["reportedEPS"],
            "estimatedEPS": latest.get("estimatedEPS", "N/A"),
            "surprise": latest.get("surprise", "N/A"),
            "surprisePercentage": latest.get("surprisePercentage", "N/A")
        }

    except Exception as e:
        return {"error": str(e)}
    

def fetch_last_5_days_prices(ticker: str):
    try:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": ALPHAVANTAGE_API_KEY
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return {"error": f"API call failed with status {response.status_code}"}

        data = response.json()
        print("RAW RESPONSE:", data)
        
        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            return {"error": "No price data found.", "raw": data}


        sorted_dates = sorted(time_series.keys(), reverse=True)[:5]
        prices = []
        for date in sorted_dates:
            close = float(time_series[date]["4. close"])
            prices.append({"date": date, "close": close})

        return {"prices": prices}

    except Exception as e:
        return {"error": f"Failed to fetch price data: {str(e)}"}



import yfinance as yf  # pip install yfinance

def fetch_last_5_days_prices(ticker: str):
    try:
        # Fetch data for NSE-listed TCS
        stock = yf.Ticker(ticker)
        data = stock.history(period="5d")
        
        if data.empty:
            return {"error": "No price data found."}
        
        # Format the response
        prices = [
            {"date": str(date.date()), "close": close} 
            for date, close in zip(data.index, data["Close"])
        ]
        return {"prices": prices}
    
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}

