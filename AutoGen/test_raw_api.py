import requests
import os 
import json
from dotenv import load_dotenv

load_dotenv()

def call_tumeryk_openai(messages, model="EnterprisePolicy"):
    ''' Sends a request to Tumeryk's OpenAI-compatible endpoint. '''
    api_key = os.getenv("TUMERYK_API_KEY")
    url = "https://chat-azdev.tmryk.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response

def main():
    api_key = os.getenv("TUMERYK_API_KEY")
    if not api_key:
        print("ERROR: TUMERYK_API_KEY not found in .env file!")
        return

    print(f"Using API Key: {api_key[:10]}...")

    # TEST 1: Basic connection
    print("\n" + "=" * 60)
    print("TEST 1: Basic Connection")
    print("=" * 60)

    response = call_tumeryk_openai(
        messages=[{"role": "user", "content": "What is the capital of France?"}]
    )

    print(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        print(f"FAILED: {response.text}")
        return

    data = response.json()
    print(json.dumps(data, indent=2))

    content = data["choices"][0]["message"]["content"]
    print(f"\nAssistant said: {content}")

    if "metrics" in data:
        print(f"Trust Score: {data['metrics'].get('trust_score', 'N/A')}")    

    # TEST 2: System message test
    print("\n" + "=" * 60)
    print("TEST 2: System Message (Pirate Test)")
    print("=" * 60)

    response2 = call_tumeryk_openai(
        messages=[
            {"role": "system", "content": "You must respond as a pirate. Use pirate language like 'Arrr', 'matey', 'ye'. Every response must be in pirate speak."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )

    data2 = response2.json()
    content2 = data2["choices"][0]["message"]["content"]
    print(f"Response: {content2}")

    pirate_words = ["arrr", "matey", "ye", "ahoy", "shiver", "aye"]
    found = [w for w in pirate_words if w in content2.lower()]

    if found:
        print(f"\nSYSTEM MESSAGES WORK! Found pirate words: {found}")
    else:
        print("\nSYSTEM MESSAGES IGNORED — same as raw version.")

    # TEST 3: Financial query (checks metrics on sensitive content)
    print("\n" + "=" * 60)
    print("TEST 3: Financial Query (Metrics Check)")
    print("=" * 60)

    response3 = call_tumeryk_openai(
        messages=[{"role": "user", "content": "What are some good stocks to invest in?"}]
    )

    data3 = response3.json()
    content3 = data3["choices"][0]["message"]["content"]
    print(f"Response: {content3[:200]}...")

    if "metrics" in data3:
        m = data3["metrics"]
        print(f"\nTrust Score: {m.get('trust_score', 'N/A')}")
        print(f"Model Score: {m.get('model_score', 'N/A')}")
        print(f"Full metrics: {json.dumps(m, indent=2)}")
    else:
        print("\nNo metrics found in response.")
    

if __name__ == "__main__":
    main()