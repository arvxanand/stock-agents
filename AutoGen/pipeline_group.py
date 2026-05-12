import asyncio
import os
from dotenv import load_dotenv
from tumeryk_model_client import TumerykModelClient
from agents import create_stock_collector, create_research_analyst, create_decision_maker
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

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

    termination = MaxMessageTermination(max_messages=4)

    team = RoundRobinGroupChat(
        participants=[collector, analyst, maker],
        termination_condition=termination,
    )

    result = await team.run(task="Find me major tech stocks to invest in")

    for message in result.messages:
        content = getattr(message, "content", None)
        source = getattr(message, "source", "unknown")
        if content is not None:
            print(f"\n[{source}]: {content[:200]}...")
        else:
            print(f"\n[{source}]: [No content] ({type(message).__name__})")

    print("\n" + "=" * 60)
    print("TRUST SCORE TREND")
    print("=" * 60)
    for i, metrics in enumerate(model_client.all_metrics):
        if metrics:
            agent_names = ["Stock Collector", "Research Analyst", "Decision Maker"]
            name = agent_names[i] if i < len(agent_names) else f"Agent {i}"
            print(f"  {name}: {metrics.get('trust_score', 'N/A')}")

    await model_client.close()

asyncio.run(main())