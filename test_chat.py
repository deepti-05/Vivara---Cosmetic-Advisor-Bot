
import requests
import json

GEMINI_API_KEY = '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'
GEMINI_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

MODEL_NAME = "google/gemini-2.0-flash-exp:free"

payload = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user",
            "content": "Hello, simply reply with 'Working'"
        }
    ]
}

headers = {
    "Authorization": f"Bearer {GEMINI_API_KEY}",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "Vivara Backend",
    "Content-Type": "application/json"
}

try:
    print(f"Testing model: {MODEL_NAME}")
    response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
