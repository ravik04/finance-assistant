import yfinance as yf
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

def get_tech_stock_data(tickers):
    stock_data = {}
    for ticker in tickers:
        logging.info(f"Fetching {ticker}")
        for i in range(10):  # 5 retries
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d", interval= "1m")
                if hist.empty:
                    raise Exception("No data returned")
                today = hist["Close"].iloc[-1]
                # yesterday = hist["Close"].iloc[-2]
                # change = today - yesterday
                # pct_change = (change / yesterday) * 100
                stock_data[ticker] = {
                    "today": round(today,2),
                    # "yesterday": round(yesterday,2),
                    # "change": round(change,2),
                    # "percent_change": round(pct_change,2)
                }
                break
            except Exception as e:
                logging.warning(f"Error on {ticker}, retry {i+1}: {e}")
                time.sleep(random.uniform(2,5))
        else:
            stock_data[ticker] = {"error": "Failed after retries"}
    return stock_data

# if __name__ == "__main__":
#     tickers = ['TCS.NS', 'INFY.NS', 'RELIANCE.NS']
#     print(get_tech_stock_data(tickers))
