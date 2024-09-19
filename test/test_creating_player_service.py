from models.Player import Player
from service.creating_player_service import compute_position_stats, create_player

sample_data = [
    {'playerName': 'Player1', 'position': 'PG', 'team': 'TeamA', 'season': 2022, 'games': 10, 'points': 200, 'assists': 50, 'turnovers': 20, 'twoFg': 50, 'twoAttempts': 100, 'threeFg': 30, 'threeAttempts': 80},
    {'playerName': 'Player2', 'position': 'SG', 'team': 'TeamB', 'season': 2022, 'games': 20, 'points': 400, 'assists': 70, 'turnovers': 30, 'twoFg': 80, 'twoAttempts': 150, 'threeFg': 60, 'threeAttempts': 90},
    {'playerName': 'Player3', 'position': 'PG', 'team': 'TeamC', 'season': 2023, 'games': 15, 'points': 300, 'assists': 40, 'turnovers': 10, 'twoFg': 60, 'twoAttempts': 120, 'threeFg': 40, 'threeAttempts': 70},
    {'playerName': 'Player4', 'position': 'SG', 'team': 'TeamA', 'season': 2023, 'games': 25, 'points': 500, 'assists': 90, 'turnovers': 25, 'twoFg': 90, 'twoAttempts': 160, 'threeFg': 70, 'threeAttempts': 100}
]

expected_position_stats = {
    'PG': (200 + 300) / (10 + 15),
    'SG': (400 + 500) / (20 + 25)
}

def test_compute_position_stats():
    result = compute_position_stats(sample_data)
    assert result['PG'] == expected_position_stats['PG']
    assert result['SG'] == expected_position_stats['SG']
    assert 'SF' not in result

def test_create_player():
    position_avg = compute_position_stats(sample_data)

    player_data = {
        'playerName': 'Player5',
        'position': 'PG',
        'team': 'TeamD',
        'season': 2024,
        'games': 12,
        'points': 240,
        'assists': 60,
        'turnovers': 15,
        'twoFg': 70,
        'twoAttempts': 140,
        'threeFg': 50,
        'threeAttempts': 100
    }

    player = create_player(player_data, position_avg)

    assert isinstance(player, Player)
    assert player.player_name == 'Player5'
    assert player.position == 'PG'
    assert player.team == 'TeamD'
    assert player.season == 2024
    assert player.games == 12
    assert player.points == 240
    assert player.assists == 60
    assert player.turnovers == 15
    assert player.two_fg == 70
    assert player.two_attempts == 140
    assert player.three_fg == 50
    assert player.three_attempts == 100
    assert player.atr == (60 / 15)
    assert player.ppg_ratio == (240 / 12) / position_avg['PG']

def test_create_player_zero_games():
    position_avg = compute_position_stats(sample_data)

    player_data = {
        'playerName': 'Player6',
        'position': 'SG',
        'team': 'TeamE',
        'season': 2024,
        'games': 0,
        'points': 0,
        'assists': 0,
        'turnovers': 0,
        'twoFg': 0,
        'twoAttempts': 0,
        'threeFg': 0,
        'threeAttempts': 0
    }

    player = create_player(player_data, position_avg)

    assert isinstance(player, Player)
    assert player.atr == 0
    assert player.ppg_ratio == 0

