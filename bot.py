import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from bs4 import BeautifulSoup

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener el token desde la variable de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Verificar que el token se ha cargado correctamente
if TELEGRAM_TOKEN is None:
    raise ValueError("El token de Telegram no está configurado correctamente en las variables de entorno.")

# Función para obtener la información de jugadores lesionados o activos
def obtener_info_jugadores():
    url = 'https://twitter.com/Underdog__NBA'  # URL de la fuente
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Aquí puedes extraer la información relevante del HTML
    # Necesitas ajustar el scraping según la estructura de la página web
    tweets = soup.find_all('div', {'class': 'tweet-text'})  # Este es solo un ejemplo
    info = ""
    
    for tweet in tweets:
        text = tweet.get_text()
        if 'injury' in text.lower() or 'active' in text.lower():
            info += text + '\n\n'
    
    if info == "":
        info = "No hay actualizaciones recientes sobre jugadores lesionados o activos."
    
    return info

# Comando para responder a /jugadores
async def jugadores(update: Update, context: CallbackContext) -> None:
    info = obtener_info_jugadores()
    await update.message.reply_text(info)

# Comando para iniciar el bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de NBA. Usa /jugadores para obtener información actualizada.')

# Función principal que arranca el bot
def main():
    # Crear el objeto Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Agregar los manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jugadores", jugadores))

    # Iniciar el polling para recibir actualizaciones
    application.run_polling()

if __name__ == '__main__':
    main()
