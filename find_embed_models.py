import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    print("Fetching models...")
    # Use a raw list call to avoid the Model.__init__ error if possible
    # or use a different endpoint
    models = genai.list_models()
    for m in models:
        try:
            # Bypass the __init__ error if it happens during iteration
            # by accessing the underlying object attributes if possible
            # But the error happens in the generator itself.
            pass
        except Exception:
            continue
    
    # Let's try to get them via the REST API directly to be safe
    import requests
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for model in data.get("models", []):
            name = model.get("name")
            methods = model.get("supportedGenerationMethods", [])
            if "embedContent" in methods:
                print(f"Supported Embedding Model: {name}")
    else:
        print(f"REST API Error: {response.status_code} - {response.text}")

except Exception as e:
    print(f"Error: {e}")
