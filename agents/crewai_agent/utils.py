from crewai import Agent, Task, Crew
from litellm import completion
import litellm

# ✅ Set up LLM configuration
litellm.set_verbose = True

from litellm import completion, Router

# Explicit LLM config using Groq
litellm.api_key = "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"

# ✅ Define wrapper function CrewAI can use
class GroqLLM:
    def chat(self, messages, **kwargs):
        response = completion(
            model="llama3-70b-8192",
            messages=messages,
            provider="groq",
            api_key=litellm.api_key
        )
        return response["choices"][0]["message"]["content"]

llm = GroqLLM()

# ✅ Core logic
def run_market_crew(ticker: str, headlines: list, earnings_summary: str):
    news_text = "\n".join(headlines)

    summarizer = Agent(
        role="News Summarizer",
        goal="Summarize financial headlines clearly",
        backstory="You write daily news summaries for hedge fund managers.",
        llm=llm,
        verbose=True
    )

    analyst = Agent(
        role="Market Sentiment Analyst",
        goal="Determine sentiment from news and earnings",
        backstory="You help investment analysts form market views.",
        llm=llm,
        verbose=True
    )

    summarize_task = Task(
        description=f"Summarize the following headlines about {ticker}:\n{news_text}",
        expected_output="A short paragraph summary.",
        agent=summarizer
    )

    analyze_task = Task(
        description=f"Analyze sentiment for {ticker} using earnings summary: {earnings_summary} and news: {{summarize_task.output}}. Give a bullish/bearish/neutral signal with a reason.",
        expected_output="Sentiment and rationale.",
        agent=analyst,
        depends_on=[summarize_task]
    )

    crew = Crew(
        agents=[summarizer, analyst],
        tasks=[summarize_task, analyze_task],
        verbose=True
    )

    crew.kickoff()

    return {
        "ticker": ticker.upper(),
        "news_summary": summarize_task.output,
        "analysis": analyze_task.output
    }
