import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models_to_try = [
    "models/text-embedding-004",
    "text-embedding-004",
    "models/embedding-001",
    "embedding-001",
    "models/text-embedding-gecko@001",
    "text-embedding-gecko@001"
]

for model in models_to_try:
    print(f"Trying model: {model}...")
    try:
        result = genai.embed_content(
            model=model,
            content="Hello world",
            task_type="retrieval_document"
        )
        print(f"SUCCESS with {model}!")
        break
    except Exception as e:
        print(f"FAILED with {model}: {e}")
