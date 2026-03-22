import requests
import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv("PORT_BACKEND", "8600")
url = f"http://127.0.0.1:{port}/upload"

file_path = r"c:\Antigravity\AI Agent(3600-8600)\03-09 EM-EM-009 15ppm BILGE ALARM MONITOR CALIBRATION 방법.pdf"

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

print(f"Uploading {file_path} to {url}...")
with open(file_path, "rb") as f:
    files = {"file": (os.path.basename(file_path), f, "application/pdf")}
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request Error: {e}")
