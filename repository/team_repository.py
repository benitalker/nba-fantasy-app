from typing import List
from psycopg2.extras import execute_values
import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI


def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)


def create_team(team_name: str) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO teams (team_name) VALUES (%s) RETURNING id',
            (team_name,)
        )
        team_id = cursor.fetchone()['id']
        connection.commit()
    return team_id


def update_team(team_id: int, player_ids: List[int]) -> bool:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1 FROM teams WHERE id = %s', (team_id,))
            if not cursor.fetchone():
                return False
            cursor.execute('DELETE FROM team_players WHERE team_id = %s', (team_id,))
            values = [(team_id, player_id) for player_id in player_ids]
            execute_values(
                cursor,
                'INSERT INTO team_players (team_id, player_id) VALUES %s',
                values
            )
            connection.commit()
    return True



def delete_team(team_id: int) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT 1 FROM teams WHERE id = %s', (team_id,))
        exists = cursor.fetchone() is not None

        if not exists:
            return False

        cursor.execute('DELETE FROM teams WHERE id = %s', (team_id,))
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
        with connection.cursor() as cursor:
            cursor.execute(query, (team_id,))
            result = cursor.fetchall()

    if not result:
        return {'team_name': "team not exists", 'players': []}

    team_name = result[0]['team_name']
    players = [{'player_id': row['player_id'], 'player_name': row['player_name'], 'position': row['position'],
                'team': row['team']} for row in result]

    return {'team_name': team_name, 'players': players}

