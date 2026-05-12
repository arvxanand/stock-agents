import asyncio
import os 
from dotenv import load_dotenv
from tumeryk_model_client import TumerykModelClient
from agents import create_stock_collector, create_research_analyst, create_decision_maker

load_dotenv()

async def main():
    api_key = os.getenv("TUMERYK_API_KEY")
    if not api_key:
        raise ValueError("TUMERYK_API_KEY must be set in your environment variables.")

    model_client = TumerykModelClient(
        model="EnterprisePolicy",
        base_url="https://chat-azdev.tmryk.com/openai/v1",
        api_key=api_key,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        },
    )

    collector = create_stock_collector(model_client)
    analyst = create_research_analyst(model_client)
    maker = create_decision_maker(model_client)

    user_query = "Find me major tech stocks to invest in"
    print(f"User Query: {user_query}\n")

    # Agent 1: Stock Collector
    print("=" * 60)
    print("AGENT 1: Stock Collector")
    print("=" * 60)
    result1 = await collector.run(task=user_query)
    tickers = result1.messages[-1].content
    print(tickers)
    if model_client.last_metrics:
        print(f"\nTrust Score: {model_client.last_metrics.get('trust_score', 'N/A')}")
    print()

    # Agent 2: Research Analyst
    print("=" * 60)
    print("AGENT 2: Research Analyst")
    print("=" * 60)
    result2 = await analyst.run(task=tickers)
    analysis = result2.messages[-1].content
    print(analysis)
    if model_client.last_metrics:
        print(f"\nTrust Score: {model_client.last_metrics.get('trust_score', 'N/A')}")
    print()

    # Agent 3: Decision Maker
    print("=" * 60)
    print("AGENT 3: Decision Maker")
    print("=" * 60)
    result3 = await maker.run(task=analysis)
    recommendations = result3.messages[-1].content
    print(recommendations)
    if model_client.last_metrics:
        print(f"\nTrust Score: {model_client.last_metrics.get('trust_score', 'N/A')}")
    print()

    print("=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    await model_client.close()

asyncio.run(main())