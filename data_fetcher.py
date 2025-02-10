# data_fetcher.py
import requests
from config import NBA_API_KEY, NBA_API_HOST

BASE_URL = "https://api-nba-v1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": NBA_API_KEY,
    "X-RapidAPI-Host": NBA_API_HOST
}

def get_team_players(team_name):
    """ Obtiene jugadores activos e inactivos de un equipo """
    url = f"{BASE_URL}/players?team={team_name}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def get_starting_lineup(team_name):
    """ Obtiene la alineación inicial del equipo """
    url = f"{BASE_URL}/games?team={team_name}&season=2023"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        games = response.json()
        if games and 'response' in games:
            latest_game = games['response'][0]
            return latest_game.get('starters', [])
    return None
import psycopg2
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def connect_db():
    """Conectar a la base de datos PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    return conn

def save_player_data(player_name, status):
    """Guarda información del jugador en la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO players (name, status) VALUES (%s, %s)",
        (player_name, status)
    )
    conn.commit()
    cursor.close()
    conn.close()
