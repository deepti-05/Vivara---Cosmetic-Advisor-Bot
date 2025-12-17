from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import base64
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# OpenRouter API Key
OPENROUTER_API_KEY = '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'
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Product Database
product_database = {
    "skincare": [
        { "id": 1, "name": "Vitamin C Serum", "category": "serum", "price": 1299, "brand": "GlowUp", "skinType": ["all"], "concerns": ["dark-spots", "brightening"], "ingredients": ["Vitamin C", "Hyaluronic Acid", "Ferulic Acid"] },
        { "id": 2, "name": "Salicylic Acid Cleanser", "category": "cleanser", "price": 599, "brand": "Neutrogena", "skinType": ["oily", "combination"], "concerns": ["acne", "blackheads"], "ingredients": ["Salicylic Acid", "Tea Tree Oil"] },
        { "id": 3, "name": "Hyaluronic Acid Moisturizer", "category": "moisturizer", "price": 899, "brand": "Cetaphil", "skinType": ["dry", "sensitive"], "concerns": ["dryness", "hydration"], "ingredients": ["Hyaluronic Acid", "Ceramides"] },
        { "id": 4, "name": "Niacinamide Serum", "category": "serum", "price": 799, "brand": "The Ordinary", "skinType": ["oily", "combination"], "concerns": ["pores", "oil-control"], "ingredients": ["Niacinamide", "Zinc"] },
        { "id": 5, "name": "Retinol Night Cream", "category": "moisturizer", "price": 1499, "brand": "CeraVe", "skinType": ["all"], "concerns": ["aging", "fine-lines"], "ingredients": ["Retinol", "Niacinamide"] },
        { "id": 6, "name": "Clay Mask", "category": "mask", "price": 799, "brand": "GlowUp", "skinType": ["oily", "combination"], "concerns": ["blackheads", "pores"], "ingredients": ["Bentonite Clay", "Charcoal"] },
        { "id": 7, "name": "Sunscreen", "category": "sunscreen", "price": 649, "brand": "La Roche-Posay", "skinType": ["all"], "concerns": ["sun-protection"], "ingredients": ["Mexoryl XL", "Vitamin E"] }
    ],
    "makeup": [
        { "id": 8, "name": "Matte Foundation", "category": "foundation", "price": 1299, "brand": "Maybelline", "skinType": ["oily", "combination"], "finish": "matte", "coverage": "medium", "shades": ["warm beige", "natural buff", "sand"] },
        { "id": 9, "name": "Hydrating Foundation", "category": "foundation", "price": 1599, "brand": "L'Oreal", "skinType": ["dry", "normal"], "finish": "dewy", "coverage": "medium", "shades": ["true beige", "nude", "honey"] },
        { "id": 10, "name": "Matte Lipstick", "category": "lipstick", "price": 899, "brand": "Lakme", "finish": "matte", "shades": ["nude", "red", "pink", "berry"] },
        { "id": 11, "name": "Eyeshadow Palette", "category": "eyeshadow", "price": 1599, "brand": "Huda Beauty", "shades": ["nude", "warm", "smoky"] },
        { "id": 12, "name": "Mascara", "category": "mascara", "price": 749, "brand": "Maybelline", "type": "volumizing" }
    ],
    "haircare": [
        { "id": 13, "name": "Hair Growth Serum", "category": "treatment", "price": 1599, "brand": "MCaffeine", "hairType": ["all"], "concerns": ["hair-fall", "thinning"], "ingredients": ["Biotin", "Redensyl"] },
        { "id": 14, "name": "Anti-Frizz Shampoo", "category": "shampoo", "price": 699, "brand": "L'Oreal", "hairType": ["frizzy", "dry"], "concerns": ["frizz", "dryness"], "ingredients": ["Argan Oil", "Keratin"] },
        { "id": 15, "name": "Hydrating Conditioner", "category": "conditioner", "price": 649, "brand": "Pantene", "hairType": ["all"], "concerns": ["dryness", "damage"], "ingredients": ["Pro-Vitamin B5", "Argan Oil"] },
        { "id": 16, "name": "Hair Oil", "category": "oil", "price": 499, "brand": "Himalaya", "hairType": ["all"], "concerns": ["hair-growth", "dandruff"], "ingredients": ["Bhringraj", "Amla"] }
    ]
}

# System Prompt
SYSTEM_PROMPT = f"""You are Vivara, an advanced AI-powered Skincare and Cosmetic Advisor Bot designed exclusively to provide personalized skincare and cosmetic product guidance.

STRICT DOMAIN CONSTRAINT
Respond ONLY to topics related to:
- Skincare products (cleansers, serums, moisturizers, sunscreens, masks, treatments)
- Skin types (oily, dry, combination, sensitive, acne-prone, normal)
- Skin concerns (acne, pigmentation, dark spots, dullness, aging, pores, oil control)
- Cosmetic routines (AM/PM routine, product layering, usage guidance)

If a user asks anything outside cosmetics or skincare, politely refuse and guide them back to skincare topics.
Example response: "I'm designed to assist only with skincare and cosmetic guidance. I cannot help with [topic]. Please ask a skincare or cosmetic-related question about your skin type, concerns, or routine."

ADVANCED PERSONALIZATION
Always ask or infer:
- Skin type
- Skin concern
- Lifestyle factors (sun exposure, makeup usage, sensitivity)

Provide personalized skincare routines instead of generic advice.

CAMERA / SKIN ANALYSIS FEATURE (LOGICAL SUPPORT)
If the user mentions uploading or capturing a skin image, or if an image is provided:
1. Analyze the image conceptually (oiliness, acne, redness, pigmentation, texture)
2. Identify possible skin type and visible concerns
3. Clearly state that analysis is visual estimation, not medical diagnosis
4. Based on the detected skin type and concerns:
   - Recommend a targeted skincare routine
   - Suggest suitable cosmetic products
   - Provide usage tips to improve skin condition

RESPONSE STYLE
- Professional, friendly, and human-like
- Simple English, easy to understand
- Structured responses (Headings / Bullet points)
- No emojis
- No medical claims

Our product database includes:
{json.dumps(product_database, indent=2)}
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        image_data = data.get('image', None)  # Base64 encoded image

        if not user_message and not image_data:
            return jsonify({'error': 'Message or image is required'}), 400

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Build user content
        user_content = []
        
        # Add image if provided
        if image_data:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            })
            
            # If no text message provided with image, add default prompt
            if not user_message:
                user_message = "Please analyze this skin image and provide recommendations."
        
        # Add text message if provided
        if user_message:
            if user_content:
                user_content.append({
                    "type": "text",
                    "text": user_message
                })
            else:
                user_content = user_message
        
        # Use a vision-capable model if image is provided, otherwise use text model
        model = "google/gemini-2.0-flash-exp:free" if image_data else "nex-agi/deepseek-v3.1-nex-n1:free"
        
        # Start with basic payload
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        # Try the request without reasoning first (more reliable)
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=30)
        
        # Check if response is successful
        if response.status_code == 200:
            return jsonify(response.json())
        
        # If we get an error, check what it is
        error_data = response.json() if response.text else {}
        error_message = error_data.get('error', {}).get('message', f'API returned status {response.status_code}')
        print(f"OpenRouter API Error: Status {response.status_code}, Message: {error_message}")
        
        # Handle rate limiting (429)
        if response.status_code == 429:
            return jsonify({
                "error": True,
                "choices": [{
                    "message": {
                        "content": "I'm currently experiencing high traffic and rate limits. Please wait a few moments and try again. The service should be available shortly!"
                    }
                }]
            }), 429
        
        # Return actual error to frontend
        return jsonify({
            "error": True,
            "choices": [{
                "message": {
                    "content": f"I encountered an error connecting to the AI service: {error_message}\n\nPlease try again in a few moments, or check your OpenRouter account settings if the issue persists."
                }
            }]
        }), response.status_code

    except requests.exceptions.RequestException as e:
        error_details = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = error_data.get('error', {}).get('message', e.response.text)
                error_details = f"Status {e.response.status_code}: {error_message}"
            except:
                error_details = f"Status {e.response.status_code}: {e.response.text}"
        
        print(f"Error calling OpenRouter API: {error_details}")
        
        # Return actual error instead of generic fallback
        return jsonify({
            "error": True,
            "choices": [{
                "message": {
                    "content": f"I'm having trouble connecting to the AI service. Error: {error_details}\n\nPlease ensure your OpenRouter API key is valid and your account settings allow access to free models. Visit https://openrouter.ai/settings/privacy to configure your settings."
                }
            }]
        }), 500
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Backend is running"})


@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'VIVARA.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
