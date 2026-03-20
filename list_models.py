import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Antigravity\AI Agent(3600-8600)\ai_assistant\.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Listing models...")
try:
    for m in genai.list_models():
        print(f"Model Name: {m.name}, Methods: {m.supported_generation_methods}")
except Exception as e:

    print(f"Error: {e}")
