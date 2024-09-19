from typing import List

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

def get_players_by_position_and_season(position: str, season: int = None) -> List[dict]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        query = '''
            SELECT
                player_name,
                team,
                position,
                season,
                points,
                games,
                two_fg / NULLIF(two_attempts, 0) AS two_percent,
                three_fg / NULLIF(three_attempts, 0) AS three_percent,
                atr,
                ppg_ratio
            FROM players
            WHERE position LIKE %s
        '''
        params = [f'%{position}%']

        if season is not None:
            query += ' AND season = %s'
            params.append(season)

        cursor.execute(query, tuple(params))
        players = cursor.fetchall()

    return players

def get_player_position_by_id(id: int) -> str:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            'SELECT position FROM players WHERE id = %s',
            (id,)
        )
        result = cursor.fetchone()
        if result is None:
            raise ValueError(f"Player with ID {id} not found.")
        return result['position']
