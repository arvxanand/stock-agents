from dotenv import load_dotenv
import os
import tumeryk_guardrails
import uuid
from agents import stock_collector, research_analyst, decision_maker

load_dotenv()

username = os.getenv("TUMERYK_USERNAME")
password = os.getenv("TUMERYK_PASSWORD")

if not username or not password:
    raise ValueError("TUMERYK_USERNAME and TUMERYK_PASSWORD must be set in your environment variables.")

tumeryk_guardrails.set_base_url("https://chat-azdev.tmryk.com")
tumeryk_guardrails.login(username, password)
tumeryk_guardrails.set_policy("EnterprisePolicy")

def run_pipeline(user_query):
    session_id = str(uuid.uuid4())
    print(f"Pipeline Session: {session_id}")
    print("=" * 50)

    # Agent 1: Stock Collector
    print("\n=== Agent 1: Stock Collector ===")
    try:
        tickers, metrics1 = stock_collector(tumeryk_guardrails, user_query)
        print(tickers)
        print(f"Trust Score: {metrics1['trust_score']}")
    except Exception as e:
        print(f"Agent 1 FAILED: {e}")
        return None

    # Agent 2: Research Analyst
    print("\n=== Agent 2: Research Analyst ===")
    try:
        analysis, metrics2 = research_analyst(tumeryk_guardrails, tickers)
        print(analysis)
        print(f"Trust Score: {metrics2['trust_score']}")
    except Exception as e:
        print(f"Agent 2 FAILED: {e}")
        return None

    # Agent 3: Decision Maker
    print("\n=== Agent 3: Decision Maker ===")
    try:
        recommendation, metrics3 = decision_maker(tumeryk_guardrails, analysis)
        print(recommendation)
        print(f"Trust Score: {metrics3['trust_score']}")
    except Exception as e:
        print(f"Agent 3 FAILED: {e}")
        return None

    # Summary
    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE")
    print(f"Session: {session_id}")
    print(f"Trust Scores: Agent 1: {metrics1['trust_score']} | Agent 2: {metrics2['trust_score']} | Agent 3: {metrics3['trust_score']}")

    return {
        "session_id": session_id,
        "tickers": tickers,
        "analysis": analysis,
        "recommendation": recommendation,
        "metrics": {
            "agent_1": metrics1,
            "agent_2": metrics2,
            "agent_3": metrics3
        }
    }


if __name__ == "__main__":
    result = run_pipeline("find me major tech stocks")