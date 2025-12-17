import requests

# Check available models on OpenRouter
API_KEY = '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'

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("Fetching available models from OpenRouter...")
try:
    response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
    if response.status_code == 200:
        models = response.json()['data']
        print(f"\nFound {len(models)} models")
        print("\nSearching for OpenAI/GPT models...")
        print("="*60)
        
        openai_models = []
        for m in models:
            if 'openai' in m['id'].lower() or 'gpt' in m['id'].lower():
                openai_models.append(m)
                print(f"Model: {m['id']}")
                if 'pricing' in m:
                    if m['pricing'].get('prompt') == '0' or ':free' in m['id']:
                        print(f"  -> FREE MODEL!")
                print()
        
        print(f"\nTotal OpenAI/GPT models found: {len(openai_models)}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {str(e)}")
