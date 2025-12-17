
import requests
import json

GEMINI_API_KEY = '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'
GEMINI_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Using a known stable model for testing first, or same model if needed
# But let's verify the specific model in the code first
MODEL_NAME = "google/gemini-2.0-flash-lite-preview-02-05:free"
# Trying another model if the above fails
MODEL_NAME = "google/gemini-2.0-flash-exp:free"

payload = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user",
            "content": "Hello, are you working?"
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
    print(f"Testing Auth and fetching models...")
    response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        models = response.json()['data']
        print(f"Found {len(models)} models.")
        # Print a few google models
        for m in models:
            if 'gemini' in m['id']:
                print(f"Model: {m['id']}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

