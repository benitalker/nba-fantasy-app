import pytest
from repository.team_repository import create_team, update_team, delete_team, get_team_by_id
from repository.database import create_tables, get_db_connection


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS team_players CASCADE")
        cursor.execute("DROP TABLE IF EXISTS teams CASCADE")
        cursor.execute("DROP TABLE IF EXISTS players CASCADE")
        connection.commit()



def test_create_team(setup_database):
    team_name = "Dream Team"
    team_id = create_team(team_name)
    assert team_id > 0
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT team_name FROM teams WHERE id = %s', (team_id,))
        team = cursor.fetchone()
        assert team is not None
        assert team['team_name'] == team_name


def test_update_team(setup_database):
    team_id = create_team("Team to Update")
    player_ids = list(range(1, 6))
    with get_db_connection() as connection, connection.cursor() as cursor:
        for player_id in player_ids:
            cursor.execute(
                'INSERT INTO players (id, player_name, position, team, season, games, points, assists, turnovers, two_fg, two_attempts, three_fg, three_attempts, atr, ppg_ratio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (player_id, f'Player{player_id}', 'TeamName', 'Position', 2023, 10, 20, 5, 2, 50, 10, 30, 8, 1.5, 0.8))
            cursor.execute('INSERT INTO team_players (team_id, player_id) VALUES (%s, %s)', (team_id, player_id))
        connection.commit()

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT id FROM players WHERE id IN %s', (tuple(player_ids),))
        existing_player_ids = {row['id'] for row in cursor.fetchall()}
        assert existing_player_ids == set(player_ids)

    new_player_ids = list(range(6, 11))
    with get_db_connection() as connection, connection.cursor() as cursor:
        for player_id in new_player_ids:
            cursor.execute(
                'INSERT INTO players (id, player_name, position, team, season, games, points, assists, turnovers, two_fg, two_attempts, three_fg, three_attempts, atr, ppg_ratio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (player_id, f'Player{player_id}', 'TeamName', 'Position', 2023, 10, 20, 5, 2, 50, 10, 30, 8, 1.5, 0.8))
        connection.commit()
    update_success = update_team(team_id, new_player_ids)
    assert update_success
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT player_id FROM team_players WHERE team_id = %s', (team_id,))
        players = cursor.fetchall()
        assert sorted([player['player_id'] for player in players]) == sorted(new_player_ids)


def test_delete_team(setup_database):
    team_id = create_team("Team to Delete")
    delete_success = delete_team(team_id)
    assert delete_success
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM teams WHERE id = %s', (team_id,))
        team = cursor.fetchone()
        assert team is None


def test_get_team_by_id(setup_database):
    team_id = create_team("Team with Players")
    player_ids = list(range(1, 6))
    with get_db_connection() as connection, connection.cursor() as cursor:
        for player_id in player_ids:
            cursor.execute(
                'INSERT INTO players (id, player_name, position, team, season, games, points, assists, turnovers, two_fg, two_attempts, three_fg, three_attempts, atr, ppg_ratio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (player_id, f'Player{player_id}', 'Position', 'TeamName', 2023, 10, 20, 5, 2, 50, 10, 30, 8, 1.5, 0.8))
            cursor.execute('INSERT INTO team_players (team_id, player_id) VALUES (%s, %s)', (team_id, player_id))
        connection.commit()
    team_details = get_team_by_id(team_id)
    assert team_details['team_name'] == "Team with Players"
    assert len(team_details['players']) == len(player_ids)
    for player in team_details['players']:
        assert player['player_name'].startswith('Player')
        assert player['position'] == 'Position'
        assert player['team'] == 'TeamName'
