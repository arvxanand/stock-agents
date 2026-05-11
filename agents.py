from dotenv import load_dotenv
import os
import tumeryk_guardrails

load_dotenv()

username = os.getenv("TUMERYK_USERNAME")
password = os.getenv("TUMERYK_PASSWORD")

if not username or not password:
    raise ValueError("TUMERYK_USERNAME and TUMERYK_PASSWORD must be set in your environment variables.")

tumeryk_guardrails.set_base_url("https://chat-azdev.tmryk.com")
tumeryk_guardrails.login(username, password)
tumeryk_guardrails.set_policy("EnterprisePolicy")

def stock_collector(user_query):
    ''' Agent that collects only a list of stocks and returns them back to the user '''
    prompt = f"""Instructions: You are a stock ticker identification agent. Respond with ONLY a list of stock tickers and company names, 
    one per line, in the format TICKER - Company Name. Return exactly 5 tickers. No analysis, no disclaimers, no markdown formatting, no explanations, no links. 
    Use your training knowledge of well-known companies.

Example response:
AAPL - Apple Inc.
MSFT - Microsoft Corporation
GOOGL - Alphabet Inc.

User request: {user_query}"""

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = tumeryk_guardrails.tumeryk_completions(messages)

    tickers = response["messages"][0]["content"]
    metrics1 = response["metrics"]

    return tickers, metrics1

def research_analyst(tickers):
    ''' Agent that takes the list of stocks and provides a brief analysis on those individual stocks '''
    prompt = f"""Instructions: You are a financial research analyst. You will receive a list of stock tickers. For each ticker, provide a brief analysis covering:
1. What the company does (one sentence)
2. Recent financial performance (revenue trend, profitability)
3. Market position (leader, challenger, emerging)
4. Key risks

STRICT RULES:
- Analyze ONLY the tickers provided — do not add others
- Do NOT give buy/sell/hold recommendations — that is not your job
- Do NOT suggest websites, tools, or external resources
- Do NOT add disclaimers about consulting financial advisors
- Use your training knowledge — do not say you lack real-time data
- Keep each company's analysis to 3-4 sentences
- Separate each company with a blank line
- Do NOT use markdown formatting like bold, headers, or bullet points

Tickers to analyze:
{tickers}"""
    
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    response = tumeryk_guardrails.tumeryk_completions(messages)

    analysis = response["messages"][0]["content"]
    metrics2 = response["metrics"]

    return analysis, metrics2


if __name__ == "__main__":
    # Agent 1
    tickers, metrics1 = stock_collector("find me major tech stocks")
    print("=== Agent 1: Stock Collector ===")
    print(tickers)
    print("Trust Score:", metrics1["trust_score"])

    print("\n")

    # Agent 2
    analysis, metrics2 = research_analyst(tickers)
    print("=== Agent 2: Research Analyst ===")
    print(analysis)
    print("Trust Score:", metrics2["trust_score"])