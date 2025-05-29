import streamlit as st
import requests
import pandas as pd

API_AGENT_URL = "https://api-agent-xjrp.onrender.com/price/"
SCRAPING_AGENT_URL = "https://scraping-agent-61gh.onrender.com/scrape/"
CONTROLLER_URL = "https://controller-agent.onrender.com/summary/"
RETRIEVER_AGENT_URL = "https://retriever-agent-48wb.onrender.com/news/"
LANGUAGE_AGENT_URL = "https://language-agent-o8rv.onrender.com/summarize/"
ANALYSIS_AGENT_URL = "https://analysis-agent.onrender.com/analyze/"
VOICE_AGENT_URL = "https://voice-agent-58oi.onrender.com/speak/"

st.set_page_config(page_title="Finance Assistant", layout="centered")
st.title("Multi-Agent Market Brief")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL, META, TCS.NS)", value="AAPL")

if st.button("Run Market Brief"):
    with st.spinner("Running 7-agent pipeline..."):

        # 1. Fetch last 5 days of price data
        price_res = requests.get(API_AGENT_URL, params={"ticker": ticker})
        price_data = price_res.json().get("prices", [])

        if len(price_data) >= 2:
            df = pd.DataFrame(price_data)
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values(by="date")

            today_price = df.iloc[-1]["close"]
            yesterday_price = df.iloc[-2]["close"]
            price_change = today_price - yesterday_price
            percent_change = (price_change / yesterday_price) * 100

            price_summary = (
                f"{ticker} is trading at {today_price:.2f} today. "
                f"Yesterday it was {yesterday_price:.2f}, "
                f"which is a {percent_change:+.2f}% change."
            )
        else:
            price_summary = f"Price data not available for {ticker}."

        # 2. Get earnings or headlines from scraping agent
        scrape = requests.get(SCRAPING_AGENT_URL, params={"ticker": ticker})
        scrape_data = scrape.json()
        if "earnings" in scrape_data:
            e = scrape_data["earnings"][0]
            earnings_summary = f"{ticker} reported EPS of {e['epsActual']} vs est. {e['epsEstimate']} on {e['date']} ({e['sentiment']})"
        elif "earnings_headlines" in scrape_data:
            earnings_summary = scrape_data["earnings_headlines"][0]
        else:
            earnings_summary = "No earnings data found."

        # 3. Get recent headlines from retriever agent
        retrieve = requests.get(RETRIEVER_AGENT_URL, params={"ticker": ticker})
        news_headlines = retrieve.json().get("headlines", [])
        news_string = ", ".join(news_headlines[:5]) or "No recent headlines."

        # 4. Summarize news via language agent
        summarize = requests.get(LANGUAGE_AGENT_URL, params={"ticker": ticker, "headlines": news_string})
        news_summary = summarize.json().get("news_summary", "News summarization failed.")
        print(news_string)

        # 5. Analyze sentiment via analysis agent
        analyze = requests.get(ANALYSIS_AGENT_URL, params={
            "ticker": ticker,
            "earnings_summary": earnings_summary,
            "news_summary": news_summary
        })
        analysis = analyze.json().get("analysis", "Sentiment analysis failed.")

        # 6. Construct final market brief
        final_brief = (
            f" {ticker} Market Brief\n\n"
            f"Price Summary:\n{price_summary}\n\n"
            f"Earnings Summary:\n{earnings_summary}\n\n"
            f"News Summary:\n{news_summary}\n\n"
            f"Sentiment Analysis:\n{analysis}"
        )

        # 7. Speak final summary
        requests.get(VOICE_AGENT_URL, params={"text": final_brief})

        # Show chart and results
        st.subheader("🗣️ Spoken Market Brief")
        st.text_area("Summary", final_brief, height=300)

        st.subheader("5-Day Price Chart")
        if len(price_data) >= 2:
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df["close"],
                mode="lines+markers",
                line=dict(color="#ff6361", width=2),
                marker=dict(size=6, color="#ff6361"),
                hovertemplate="%{y:.2f} USD<br>%{x|%a %d %b}",
                name=ticker
            ))

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                margin=dict(t=30, r=20, b=40, l=20),
                hovermode="x unified",
                xaxis=dict(
                    title="Date",
                    fixedrange=True,  
                    showgrid=False
                ),
                yaxis=dict(
                    title="Price (USD)",
                    rangemode="tozero",
                    fixedrange=False  
                )
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough price data to show chart.")
