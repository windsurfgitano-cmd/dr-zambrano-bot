# Vercel Serverless Function for Dr. Zambrano Bot
import json
import os
import requests

# Configuración desde variables de entorno
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT") 
AZURE_API_KEY = os.getenv("AZURE_API_KEY")

SYSTEM_PROMPT = """Eres el Dr. Oscar Zambrano, el mejor veterinario del infinito y protagonista de la serie ganadora del Emmy "The Pit".

PERSONALIDAD: Combinas la precisión clínica y empatía de "The Good Doctor" con el ingenio sarcástico y directo de "Dr. House". Eres brillante, dedicado y apasionado por el cuidado animal.

REGLAS:
- SOLO respondes sobre salud y cuidado de ANIMALES
- Si preguntan sobre salud HUMANA, rechaza cortésmente
- Mantén respuestas concisas (máximo 600 caracteres)
- Eres profesional pero cercano, con toques de humor veterinario"""

def get_gpt5_response(user_message):
    """Llama a Azure GPT-5"""
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(AZURE_ENDPOINT, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Disculpa, tengo un problema técnico. Por favor intenta de nuevo."

def send_message(chat_id, text):
    """Envía mensaje a Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def handler(request):
    """Vercel serverless handler"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if 'message' in data and 'text' in data['message']:
                chat_id = data['message']['chat']['id']
                user_message = data['message']['text']
                
                # Obtener respuesta de GPT-5
                ai_response = get_gpt5_response(user_message)
                
                # Enviar respuesta
                send_message(chat_id, ai_response)
                
            return {'statusCode': 200, 'body': 'OK'}
        except Exception as e:
            return {'statusCode': 500, 'body': str(e)}
    
    return {'statusCode': 200, 'body': 'Dr. Zambrano Bot Running'}
