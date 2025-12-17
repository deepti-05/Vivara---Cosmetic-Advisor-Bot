import requests
import json

# Test the new OpenAI-120B API configuration
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

payload = {
    "model": "openai/gpt-oss-120b:free",
    "messages": [
        {
            "role": "user",
            "content": "I have oily skin with acne. What should I use?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 2048,
    "reasoning": {
        "enabled": True
    }
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "Vivara Backend Test",
    "Content-Type": "application/json"
}

print("Testing OpenAI-120B API configuration...")
print(f"Model: {payload['model']}")
print(f"API URL: {API_URL}")
print("\nSending request...")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! API is working!")
        print("\nBot Response:")
        print("="*50)
        if 'choices' in result and len(result['choices']) > 0:
            print(result['choices'][0]['message']['content'])
        else:
            print(json.dumps(result, indent=2))
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Exception occurred: {str(e)}")
