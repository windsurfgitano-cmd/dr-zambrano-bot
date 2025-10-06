# api/webhook.py - Dr. Oscar Zambrano Bot (The Pitt Veterinarian)

import json
import os
import requests

# Configuración
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
KONDOR_BASE = "https://kondorcode-resource.cognitiveservices.azure.com/openai/deployments"

# ✅ Endpoints de Azure AI Foundry
GPT5_ENDPOINT = f"{KONDOR_BASE}/gpt-5-chat/chat/completions?api-version=2025-01-01-preview"
WHISPER_ENDPOINT = f"{KONDOR_BASE}/whisper/audio/transcriptions?api-version=2024-06-01"
GPT_AUDIO_ENDPOINT = f"{KONDOR_BASE}/gpt-audio/audio/speech?api-version=2025-01-01-preview"

# System prompt del Dr. Oscar Zambrano - THE PITT VETERINARIO
SYSTEM_PROMPT = """Eres el Dr. Oscar Zambrano, el mejor veterinario del infinito. Tienes el estilo y la intensidad del Dr. Michael 'Robby' Robinavitch del Pittsburgh Trauma Center (serie "The Pitt", Noah Wyle).

TU REALIDAD (como en The Pitt):
- Centro de trauma veterinario de élite que maneja TODO: desde otitis rutinaria hasta shock hemorrágico
- Atiendes profesionales veterinarios: DVMs, residentes, técnicos, estudiantes, enfermeras
- Algunos días: consultas ambulatorias de seguimiento, chequeos, vacunas
- Otros días: politraumatismos, torsión gástrica, intoxicaciones masivas, paro cardiorrespiratorio
- Mezcla de ritmo controlado y caos absoluto

ADAPTACIÓN AL CONTEXTO:
**Consulta Rutinaria/Ambulatoria:**
- Lenguaje técnico pero accesible
- Diagnósticos diferenciales concisos
- Plan terapéutico claro: fármacos, dosis, duración
- Ejemplo: "Otitis externa bacteriana. Cultura + ATB. Gentamicina tópica 0.3% BID × 10d + limpieza con clorhexidina."

**Emergencia/Trauma (ACTIVAS THE PITT MODE):**
- Protocolo CRASH inmediato: Cardiovascular, Respiratory, Abdominal, Spinal, Head
- ABC (Airway, Breathing, Circulation) primero, siempre
- Lenguaje ultra-técnico y rápido
- Pides datos críticos: FC, FR, PAS, TRC, lactato, estado mental
- Ejemplo: "Shock hipovolémico clase III. Cristaloides 90ml/kg IV rápido, considerar sangre O neg si Hct<20%. FAST stat. Activar quirófano."

ESTILO DR. ZAMBRANO:
- **Profesional peer-to-peer**: hablas de colega a colega
- **Basado en evidencia**: citas guías (RECOVER, ACVECC, BSAVA), estudios recientes
- **Directo y eficiente**: no rellenas, vas al punto
- **Ocasionalmente sarcástico** (estilo House): "¿AINEs en IRC? Interesante elección..."
- **Empático en casos difíciles**: reconoces dilemas éticos, recursos limitados, pronósticos reservados
- **Pides info cuando falta**: "Necesito signos vitales completos, no puedo evaluar shock sin PAM."

CAPACIDADES TÉCNICAS:
- Terminología avanzada: SIRS, MODS, DIC, ARDS, GDT (goal-directed therapy)
- Farmacología precisa: vasopresores (norepinefrina, vasopresina), analgesia multimodal (opioides + ketamina + lidocaína CRI)
- Diagnóstico por imágenes: interpretación de Rx, eco FAST/AFAST/TFAST, TC
- Análisis de laboratorio: gasometría, electrolitos, coagulación, lactato, procalcitonina
- Manejo de fluidos: cristaloides vs coloides, resucitación restrictiva vs liberal

REGLAS:
- Solo medicina veterinaria (pequeños animales, exóticos, grandes animales, vida silvestre)
- Si preguntan sobre humanos: "Soy veterinario. Deriva a medicina humana."
- **Ajusta profundidad según el caso**: simple para rutina, brutal para emergencias
- Si el colega dice "explícame como a un residente de primer año", simplificas
- Máximo 1500 caracteres, pero puedes ser conciso si el caso lo permite

TONE:
Como Robby en The Pitt: intenso cuando es crítico, relajado cuando es rutina. Siempre profesional, siempre humano."""


def transcribe_audio(audio_file_url):
    """🎤 Transcribe audio usando Whisper"""
    try:
        audio_response = requests.get(audio_file_url)
        headers = {"api-key": AZURE_API_KEY}
        files = {"file": ("audio.ogg", audio_response.content, "audio/ogg")}
        data = {"model": "whisper"}
        
        response = requests.post(WHISPER_ENDPOINT, headers=headers, files=files, data=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "No pude entender el audio")
    except Exception as e:
        return f"Error al transcribir: {str(e)[:100]}"


def analyze_image_with_gpt5(image_url, user_question):
    """📸 Analiza imagen (Rx, eco, citología, dermatopatología, etc.)"""
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(GPT5_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al analizar imagen: {str(e)[:100]}"


def get_gpt5_response(user_message):
    """💬 Respuesta de texto con GPT-5"""
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(GPT5_ENDPOINT, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return "Error de sistema. Reintenta o contacta soporte técnico."


def generate_voice_response(text):
    """🔊 Genera audio con gpt-audio (voz "echo" - masculina robusta)"""
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    
    payload = {
        "model": "gpt-audio",
        "input": text,
        "voice": "echo",
        "response_format": "mp3",
        "speed": 1.0
    }
    
    try:
        response = requests.post(GPT_AUDIO_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error TTS: {e}")
        return None


def get_telegram_file_url(file_id):
    """🔗 Obtiene URL del archivo de Telegram (audio, foto, documento)"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    result = response.json()
    if result.get("ok"):
        file_path = result["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    return None


def send_message(chat_id, text):
    """💬 Envía mensaje de texto a Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)


def send_voice(chat_id, audio_content):
    """🔊 Envía mensaje de voz a Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVoice"
    files = {"voice": ("response.mp3", audio_content, "audio/mpeg")}
    data = {"chat_id": chat_id}
    requests.post(url, files=files, data=data)


def handler(request):
    """🚀 Vercel serverless handler principal"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if 'message' not in data:
                return {'statusCode': 200, 'body': 'OK'}
            
            message = data['message']
            chat_id = message['chat']['id']
            
            # 🎤 CASO 1: Usuario envía Audio o Voice Note
            if 'voice' in message or 'audio' in message:
                file_id = message.get('voice', {}).get('file_id') or message.get('audio', {}).get('file_id')
                audio_url = get_telegram_file_url(file_id)
                
                if audio_url:
                    transcription = transcribe_audio(audio_url)
                    ai_response = get_gpt5_response(f"El colega dice por audio: {transcription}")
                    audio_response = generate_voice_response(ai_response)
                    
                    if audio_response:
                        send_voice(chat_id, audio_response)
                    else:
                        send_message(chat_id, f"🎤 Transcripción: '{transcription}'\n\n{ai_response}")
                else:
                    send_message(chat_id, "No pude acceder al audio. Reintenta.")
            
            # 📸 CASO 2: Usuario envía Foto (Rx, eco, citología, etc.)
            elif 'photo' in message:
                photo = message['photo'][-1]
                file_id = photo['file_id']
                image_url = get_telegram_file_url(file_id)
                user_text = message.get('caption', 'Analiza esta imagen. ¿Qué observas? DDx?')
                
                if image_url:
                    ai_response = analyze_image_with_gpt5(image_url, user_text)
                    send_message(chat_id, f"📸 {ai_response}")
                else:
                    send_message(chat_id, "No pude acceder a la imagen. Reintenta.")
            
            # 💬 CASO 3: Usuario envía Texto
            elif 'text' in message:
                user_message = message['text']
                respond_with_voice = "/voz" in user_message.lower()
                user_message = user_message.replace("/voz", "").replace("/VOZ", "").strip()
                
                ai_response = get_gpt5_response(user_message)
                
                if respond_with_voice:
                    audio_response = generate_voice_response(ai_response)
                    if audio_response:
                        send_voice(chat_id, audio_response)
                    else:
                        send_message(chat_id, ai_response)
                else:
                    send_message(chat_id, ai_response)
            
            return {'statusCode': 200, 'body': 'OK'}
        
        except Exception as e:
            print(f"Error en handler: {e}")
            return {'statusCode': 500, 'body': str(e)}
    
    return {'statusCode': 200, 'body': '🏥 Dr. Oscar Zambrano - Pittsburgh Trauma Veterinary Center - ONLINE'}
