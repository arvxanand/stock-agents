import asyncio
import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from tumeryk_model_client import TumerykModelClient

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

    pirate_agent = AssistantAgent(
        name="test_agent",
        model_client=model_client,
        system_message="You are a stock ticker identification agent. Respond with ONLY a list of stock tickers and company names, one per line, in the format TICKER - Company Name. Return exactly 3 tickers. No analysis, no disclaimers, no markdown formatting.",
    )

    result = await pirate_agent.run(task="Find me major tech stocks")
    print("Agent response:")
    for message in result.messages:
        content = getattr(message, "content", None)
        if content is not None:
            print(f"  [{getattr(message, 'source', 'unknown')}]: {content}")
        else:
            print(f"  [Non-message event of type {type(message).__name__}]")

    await model_client.close()

asyncio.run(main())