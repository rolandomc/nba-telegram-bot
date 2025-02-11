import logging
import os
import requests
import tweepy
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from bs4 import BeautifulSoup

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener el token desde la variable de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Verificar que el token de Telegram se ha cargado correctamente
if TELEGRAM_TOKEN is None:
    raise ValueError("El token de Telegram no está configurado correctamente en las variables de entorno.")

# Configuración de autenticación con la API de X (Twitter)
CONSUMER_KEY = os.getenv('X_API_KEY')
CONSUMER_SECRET = os.getenv('X_API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

# Autenticación con la API de X
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Función para obtener información de la API de X
def obtener_info_x():
    tweets = api.user_timeline(screen_name='Underdog__NBA', count=5)  # Obtiene los 5 últimos tweets
    info = ""
    
    for tweet in tweets:
        if 'ruled out' in tweet.text.lower() or 'injury' in tweet.text.lower():
            info += f"Tweet: {tweet.text}\n\n"
    
    if info == "":
        info = "No hay actualizaciones recientes sobre jugadores lesionados o activos en X."
    
    return info

# Función para obtener información de ESPN (usando BeautifulSoup)
def obtener_info_espn():
    url = 'https://www.espn.com/nba/'  # Página de ESPN de NBA
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ejemplo de cómo obtener información relevante de ESPN
    news_items = soup.find_all('article', {'class': 'headlineStack__list'})  # Verifica la clase de ESPN
    info = ""
    
    for item in news_items:
        headline = item.find('a').get_text()
        link = item.find('a')['href']
        info += f"{headline}\n{link}\n\n"
    
    if not info:
        info = "No hay actualizaciones recientes desde ESPN."
    
    return info

# Función para obtener información de Basketball Reference
def obtener_info_basketball_reference():
    url = 'https://www.basketball-reference.com/leagues/NBA_2023_injuries.html'  # Página de lesiones
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraemos las filas de la tabla de lesiones
    rows = soup.find_all('tr')
    info = ""
    
    for row in rows:
        columns = row.find_all('td')
        if columns:
            player_name = columns[0].get_text()
            injury = columns[1].get_text()
            status = columns[2].get_text()
            info += f"{player_name} - {injury} - {status}\n"
    
    if info == "":
        info = "No hay actualizaciones recientes sobre lesiones en Basketball Reference."
    
    return info

# Comando para responder a /jugadores
async def jugadores(update: Update, context: CallbackContext) -> None:
    info_x = obtener_info_x()  # De la API de X
    info_espn = obtener_info_espn()  # De ESPN
    info_basketball_reference = obtener_info_basketball_reference()  # De Basketball Reference
    
    # Combina toda la información obtenida
    info_completa = f"{info_x}\n---\n{info_espn}\n---\n{info_basketball_reference}"
    await update.message.reply_text(info_completa)

# Comando para iniciar el bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de NBA. Usa /jugadores para obtener información actualizada.')

# Función principal que arranca el bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jugadores", jugadores))

    # Obtener la URL pública de Railway y configurar el webhook
    # Asegúrate de que esta variable esté configurada correctamente en Railway
    webhook_url = f"https://{os.getenv('RAILWAY_URL')}/{TELEGRAM_TOKEN}"
    
    # Configurar el webhook
    application.run_webhook(
        listen="0.0.0.0",  # Escuchar en todas las interfaces
        port=5000,  # El puerto en el que el servidor escuchará las solicitudes
        url_path=TELEGRAM_TOKEN,
        webhook_url=webhook_url
    )

if __name__ == '__main__':
    main()
