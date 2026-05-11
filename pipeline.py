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