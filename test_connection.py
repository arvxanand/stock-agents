from dotenv import load_dotenv
import tumeryk_guardrails
import os

load_dotenv()

username = os.getenv("TUMERYK_USERNAME")
password = os.getenv("TUMERYK_PASSWORD")

if not username or not password:
    raise ValueError("TUMERYK_USERNAME and TUMERYK_PASSWORD must be set in your environment variables.")

tumeryk_guardrails.set_base_url("https://chat-azdev.tmryk.com")
tumeryk_guardrails.login(username, password)
tumeryk_guardrails.set_policy("EnterprisePolicy")

messages = [{"role": "user", "content": "What is the capital of France?"}]
response = tumeryk_guardrails.tumeryk_completions(messages)

print("Response:", response["messages"][0]["content"])
print("\n--- Metrics ---")
print("Trust Score:", response["metrics"]["trust_score"])
print("Jailbreak Score:", response["metrics"]["jailbreak_score"])
print("Moderation (Input):", response["metrics"]["moderation_score_input"])
print("Moderation (Output):", response["metrics"]["moderation_score_output"])
print("Violation:", response["metrics"]["violation"])