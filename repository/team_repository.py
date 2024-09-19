from typing import List, Optional
from psycopg2.extras import execute_values, RealDictCursor
import psycopg2
from config.sql_config import SQL_URI
from models.Player import Player
from toolz import pipe, curry, compose
from functools import partial

def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)

@curry
def execute_query(query: str, params: tuple, connection):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

@curry
def execute_and_fetch_one(query: str, params: tuple, connection):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

def create_team(team_name: str) -> int:
    query = 'INSERT INTO teams (team_name) VALUES (%s) RETURNING id'
    with get_db_connection() as connection:
        return pipe(
            connection,
            execute_and_fetch_one(query, (team_name,)),
            lambda result: result['id']
        )

def update_team(team_id: int, player_ids: List[int]) -> bool:
    check_query = 'SELECT 1 FROM teams WHERE id = %s'
    delete_query = 'DELETE FROM team_players WHERE team_id = %s'
    insert_query = 'INSERT INTO team_players (team_id, player_id) VALUES %s'

    with get_db_connection() as connection:
        team_exists = pipe(
            connection,
            execute_and_fetch_one(check_query, (team_id,)),
            lambda result: result is not None
        )

        if not team_exists:
            return False

        with connection.cursor() as cursor:
            cursor.execute(delete_query, (team_id,))
            values = [(team_id, player_id) for player_id in player_ids]
            execute_values(cursor, insert_query, values)

        connection.commit()
        return True

def delete_team(team_id: int) -> bool:
    check_query = 'SELECT 1 FROM teams WHERE id = %s'
    delete_query = 'DELETE FROM teams WHERE id = %s'

    with get_db_connection() as connection:
        team_exists = pipe(
            connection,
            execute_and_fetch_one(check_query, (team_id,)),
            lambda result: result is not None
        )

        if not team_exists:
            return False

        with connection.cursor() as cursor:
            cursor.execute(delete_query, (team_id,))

        connection.commit()
        return True

def get_team_by_id(team_id: int) -> dict:
    query = """
        SELECT t.team_name, p.id AS player_id, p.player_name, p.position, p.team
        FROM teams t
        LEFT JOIN team_players tp ON t.id = tp.team_id
        LEFT JOIN players p ON tp.player_id = p.id
        WHERE t.id = %s
    """
    with get_db_connection() as connection:
        result = execute_query(query, (team_id,), connection)

    if not result:
        return {'team_name': "team not exists", 'players': []}

    team_name = result[0]['team_name']
    players = [{'player_id': row['player_id'], 'player_name': row['player_name'], 'position': row['position'],
                'team': row['team']} for row in result]

    return {'team_name': team_name, 'players': players}

def get_team_by_id_statistic(team_id: int) -> Optional[dict]:
    query = """
        SELECT t.team_name, p.id AS player_id, p.player_name, p.position, p.team,
               p.points, p.two_percent, p.three_percent, p.atr, p.ppg_ratio
        FROM teams t
        JOIN team_players tp ON t.id = tp.team_id
        JOIN players p ON tp.player_id = p.id
        WHERE t.id = %s
    """
    with get_db_connection() as connection:
        result = execute_query(query, (team_id,), connection)

    if not result:
        return None

    team_name = result[0]['team_name']
    players = [{'player_id': row['player_id'], 'player_name': row['player_name'], 'position': row['position'],
                'team': row['team'], 'points': row['points'], 'two_percent': row['two_percent'],
                'three_percent': row['three_percent'], 'atr': row['atr'], 'ppg_ratio': row['ppg_ratio']} for row in result]

    return {'team_name': team_name, 'players': players}

def row_to_player(row: dict) -> Player:
    return Player(**row)

def result_to_dict(team_name: str, players: List[Player]) -> dict:
    return {'team_name': team_name, 'players': players}

def get_team_by_name_statistic(team_name: str) -> Optional[dict]:
    query = """
    SELECT id, player_name, position, team, season, games,
           points, assists, turnovers, two_fg, two_attempts, two_percent,
           three_fg, three_attempts, three_percent, atr, ppg_ratio
    FROM players
    WHERE team = %s
    """

    with get_db_connection() as connection:
        return pipe(
            connection,
            execute_query(query, (team_name,)),
            lambda result: result if result else None,
            lambda result: None if result is None else map(row_to_player, result),
            lambda players: None if players is None else result_to_dict(team_name, list(players))
        )