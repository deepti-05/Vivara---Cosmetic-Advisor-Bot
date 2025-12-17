import requests
import json

# Test with exact configuration from app.py
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Simple test message
payload = {
    "model": "openai/gpt-oss-120b:free",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful skincare advisor."
        },
        {
            "role": "user",
            "content": "I have oily skin. What cleanser should I use?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 500
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "Vivara Backend",
    "Content-Type": "application/json"
}

print("Testing OpenAI-120B API...")
print(f"Model: {payload['model']}")
print("\nSending request...\n")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS! API is working!\n")
        print("Bot Response:")
        print("="*60)
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(content)
            print("="*60)
            print("\nConfiguration is CORRECT!")
        else:
            print(json.dumps(result, indent=2))
    else:
        print(f"ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("Request timed out. The model might be slow to respond.")
except Exception as e:
    print(f"Exception: {str(e)}")
