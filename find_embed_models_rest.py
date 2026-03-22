import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment.")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
print(f"Requesting: {url.replace(api_key, 'REDACTED')}")

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Available Embedding Models:")
        for model in data.get("models", []):
            name = model.get("name")
            methods = model.get("supportedGenerationMethods", [])
            if "embedContent" in methods:
                print(f"- {name}")
    else:
        print(f"REST API Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error: {e}")
