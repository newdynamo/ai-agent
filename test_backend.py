import requests
import os

BACKEND_URL = "http://localhost:8600"
FILE_PATH = r"c:\Antigravity\AI Agent(3600-8600)\03-09 EM-EM-009 15ppm BILGE ALARM MONITOR CALIBRATION 방법.pdf"

def test_upload():
    print(f"Testing upload of {FILE_PATH}...")
    with open(FILE_PATH, "rb") as f:
        files = {"file": (os.path.basename(FILE_PATH), f, "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_chat():
    print("Testing chat...")
    payload = {"query": "What is in the document?"}
    response = requests.post(f"{BACKEND_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    if test_upload():
        test_chat()
