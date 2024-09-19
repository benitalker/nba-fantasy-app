from api.players_api import fetch_data
from models.Player import Player
from repository.database import get_db_connection

def load_players():
    sessions = [2022,2023,2024]
    for session in sessions:
        players = fetch_data(session)
        for player in players:
            create_player(player)

def create_player(player: Player) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO players (
                player_name, position, team, season, games, points, assists, turnovers, 
                two_fg, two_attempts, three_fg, three_attempts, atr, ppg_ratio
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id
            ''',
            (
                player.player_name, player.position, player.team, player.season,
                player.games, player.points, player.assists, player.turnovers,
                player.two_fg, player.two_attempts, player.three_fg, player.three_attempts,
                player.atr, player.ppg_ratio
            )
        )
        result = cursor.fetchone()
        if result is None:
            raise ValueError("No ID returned after player creation.")
        new_id = result['id']
        connection.commit()
        return new_id
