# utils.py
def format_players(players):
    """ Formatea la lista de jugadores para enviar en Telegram """
    if not players:
        return "No se encontraron jugadores."
    
    msg = "📋 **Lista de Jugadores:**\n"
    for player in players[:10]:  # Limitar a 10 jugadores
        name = player.get("name", "Desconocido")
        position = player.get("position", "N/A")
        status = "Activo" if player.get("active", False) else "Inactivo"
        msg += f"🏀 {name} - {position} ({status})\n"
    
    return msg
