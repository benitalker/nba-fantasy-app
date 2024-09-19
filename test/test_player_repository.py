import pytest
from models.Player import Player
from repository.database import create_tables, get_db_connection
from repository.player_repository import create_player, get_players_by_position_and_season, load_players

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    load_players()
    yield
    # Tear down - happens after tests are finished
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS team_players;")
    cursor.execute("DROP TABLE IF EXISTS teams;")
    cursor.execute("DROP TABLE IF EXISTS players;")
    connection.commit()
    cursor.close()
    connection.close()

def test_create_player(setup_database):
    player = Player(
        player_name="John Doe",
        position="PG",
        team="Lakers",
        season=2024,
        games=82,
        points=500,
        assists=300,
        turnovers=100,
        two_fg=50.0,
        two_attempts=100.0,
        three_fg=30.0,
        three_attempts=80.0,
        atr=3.0,
        ppg_ratio=1.2
    )
    new_id = create_player(player)
    assert new_id > 0

def test_get_players_by_position(setup_database):
    players = get_players_by_position_and_season("PG")
    assert len(players) > 0
    for player in players:
        assert "PG" in player['position']

def test_get_players_by_season(setup_database):
    players = get_players_by_position_and_season("PG", 2024)
    assert len(players) > 0
    for player in players:
        assert player['season'] == 2024

def test_get_players_by_position_and_season(setup_database):
    players = get_players_by_position_and_season("PG", 2024)
    assert len(players) > 0
    for player in players:
        assert "PG" in player['position']
        assert player['season'] == 2024

def test_get_players_by_multiple_positions(setup_database):
    players = get_players_by_position_and_season("PG-SG")
    assert len(players) > 0
    for player in players:
        assert "PG" in player['position'] or "SG" in player['position']

def test_create_and_fetch_player(setup_database):
    player = Player(
        player_name="Jane Doe",
        position="SG",
        team="Warriors",
        season=2024,
        games=70,
        points=400,
        assists=250,
        turnovers=80,
        two_fg=60.0,
        two_attempts=120.0,
        three_fg=40.0,
        three_attempts=90.0,
        atr=3.125,
        ppg_ratio=1.3
    )
    player_id = create_player(player)
    fetched_players = get_players_by_position_and_season("SG", 2024)
    assert any(p['player_name'] == "Jane Doe" for p in fetched_players)

def test_no_players_for_invalid_position(setup_database):
    players = get_players_by_position_and_season("XYZ")
    assert len(players) == 0

def test_no_players_for_invalid_season(setup_database):
    players = get_players_by_position_and_season("PG", 3000)
    assert len(players) == 0
