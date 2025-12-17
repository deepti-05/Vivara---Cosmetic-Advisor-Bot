import requests

# Quick test of the Flask backend
print("Testing Flask backend at http://localhost:5000...")

try:
    # Test health endpoint
    health_response = requests.get("http://localhost:5000/health", timeout=5)
    print(f"\nHealth Check: {health_response.status_code}")
    print(f"Response: {health_response.json()}")
    
    # Test chat endpoint
    print("\n" + "="*60)
    print("Testing chat endpoint with sample query...")
    print("="*60)
    
    chat_response = requests.post(
        "http://localhost:5000/chat",
        json={"message": "I have oily skin with acne"},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print(f"\nChat Status: {chat_response.status_code}")
    
    if chat_response.status_code == 200:
        result = chat_response.json()
        if 'choices' in result and len(result['choices']) > 0:
            print("\n✓ Backend is working!")
            print("\nBot Response:")
            print("-"*60)
            print(result['choices'][0]['message']['content'][:500] + "...")
            print("-"*60)
        else:
            print(result)
    else:
        print(f"Error: {chat_response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ Cannot connect to Flask server")
    print("Make sure the server is running on http://localhost:5000")
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
