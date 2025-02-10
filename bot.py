# bot.py
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN
from data_fetcher import get_team_players, get_starting_lineup
from utils import format_players

# Configuración de logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    """ Mensaje de bienvenida """
    update.message.reply_text("¡Hola! Soy tu bot de NBA. Usa /laker para obtener información.")

def get_team_info(update: Update, context: CallbackContext) -> None:
    """ Obtiene información de un equipo """
    team_name = "Lakers"  # Puedes hacer que esto sea dinámico según el comando
    players = get_team_players(team_name)
    if players:
        update.message.reply_text(format_players(players))

def get_lineup(update: Update, context: CallbackContext) -> None:
    """ Obtiene la alineación inicial del equipo """
    team_name = "Lakers"
    lineup = get_starting_lineup(team_name)
    if lineup:
        update.message.reply_text(f"🏀 **Quinteto Inicial de {team_name}**:\n" + "\n".join(lineup))
    else:
        update.message.reply_text("No se encontró la alineación inicial.")

def main():
    """ Inicia el bot de Telegram """
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("laker", get_team_info))
    dp.add_handler(CommandHandler("lineup", get_lineup))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
