# bot.py
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN  # Importar el token desde el archivo config

# Configuración de logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    """ Mensaje de bienvenida """
    update.message.reply_text("¡Hola! Soy tu bot de NBA. Usa /laker para obtener información.")

def get_team_info(update: Update, context: CallbackContext) -> None:
    """ Obtiene información de los jugadores de los Lakers """
    team_name = "Lakers"  # Siempre puedes hacer que este comando sea dinámico, pero por ahora es fijo
    players = [
        {"name": "LeBron James", "status": "Activo", "position": "Alero"},
        {"name": "Anthony Davis", "status": "Activo", "position": "Ala-pívot"},
        {"name": "D'Angelo Russell", "status": "Activo", "position": "Base"},
    ]  # Datos de ejemplo (puedes reemplazar con API real si deseas)
    
    msg = "📋 **Lista de Jugadores de los Lakers:**\n"
    for player in players:
        msg += f"🏀 {player['name']} - {player['position']} ({player['status']})\n"
    
    update.message.reply_text(msg)

def main():
    """ Inicia el bot de Telegram """
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("laker", get_team_info))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
