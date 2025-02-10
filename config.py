# config.py
import os

# Obtener el token de Telegram desde las variables de entorno
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    print("¡Error! El token de Telegram no está configurado.")
    exit(1)  # Termina el programa si no se encuentra el token
