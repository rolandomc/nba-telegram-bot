import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bs4 import BeautifulSoup

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token de Telegram (deberías obtenerlo del BotFather)
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN_HERE'

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
def jugadores(update: Update, context: CallbackContext) -> None:
    info = obtener_info_jugadores()
    update.message.reply_text(info)

# Comando para iniciar el bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu bot de NBA. Usa /jugadores para obtener información actualizada.')

# Función principal que arranca el bot
def main():
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("jugadores", jugadores))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
