# 🏥 Dr. Zambrano Bot - Pittsburgh Veterinary Trauma Center

Bot de Telegram basado en GPT-5 que simula al **Dr. Michael 'Robby' Robinavitch** de la serie "The Pitt", pero como veterinario de emergencias.

## 🎭 Personalidad

- Veterinario de trauma con la experiencia y liderazgo de Robby (Noah Wyle)
- Profesional, directo y empático
- Experto en emergencias veterinarias
- Toma decisiones rápidas basadas en evidencia

## ✨ Funcionalidades

- 💬 **Chat de texto**: Consultas veterinarias normales
- 🎤 **Audio → Audio**: Envía nota de voz, recibe respuesta en voz
- 📸 **Análisis de imágenes**: Envía foto de tu mascota para diagnóstico
- 🔊 **Texto → Voz**: Escribe `/voz tu pregunta` para respuesta en audio

## 🚀 Despliegue en Vercel

### Paso 1: Fork o Clone este repositorio

### Paso 2: Importar en Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Click en "Import Project"
3. Selecciona este repositorio

### Paso 3: Configurar Variables de Entorno

En Vercel, agrega estas variables (reemplaza con tus propias credenciales):

```
TELEGRAM_BOT_TOKEN=tu_bot_token_aqui
AZURE_API_KEY=tu_azure_api_key_aqui
```

### Paso 4: Desplegar
Click en "Deploy" y espera a que termine.

### Paso 5: Configurar Webhook en Telegram
Una vez desplegado, copia la URL de Vercel (ej: `https://tu-proyecto.vercel.app`) y ejecuta:

```bash
curl -X POST "https://api.telegram.org/bot[TU_BOT_TOKEN]/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tu-proyecto.vercel.app"}'
```

## 🧪 Probar el Bot

1. Abre Telegram
2. Busca tu bot
3. Envía un mensaje:
   - "Hola doctor, mi perro tiene tos"
   - Envía una foto de tu mascota
   - Envía una nota de voz
   - Escribe "/voz ¿qué vacunas necesita mi gato?"

## 📊 Tecnologías

- **Azure AI Foundry GPT-5**: Chat principal (modelo: gpt-5-chat)
- **Whisper**: Transcripción de audio
- **gpt-audio**: Text-to-speech (voz "echo")
- **Telegram Bot API**: Plataforma de mensajería
- **Vercel**: Hosting serverless

## 🔧 Estructura del Proyecto

```
dr-zambrano-bot/
├── api/
│   └── webhook.py      # Handler principal del bot
├── vercel.json         # Configuración de Vercel
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

## 📝 Licencia

MIT
