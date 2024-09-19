from typing import List

from models.Player import Player


def compute_position_stats(data: List[dict]) -> dict:
    position_stats = {}

    for player_data in data:
        position = player_data['position']
        points = player_data['points']
        games = player_data['games']

        if games > 0:
            if position not in position_stats:
                position_stats[position] = {'total_points': 0, 'total_games': 0}
            position_stats[position]['total_points'] += points
            position_stats[position]['total_games'] += games

    return {pos: stats['total_points'] / stats['total_games'] for pos, stats in position_stats.items()}


def create_player(player_data: dict, position_avg: dict) -> Player:
    position = player_data['position']
    points = player_data['points']
    games = player_data['games']

    avg_points = points / games if games > 0 else 0

    player = Player(
        player_name=player_data['playerName'],
        position=position,
        team=player_data['team'],
        season=player_data['season'],
        games=games,
        points=points,
        assists=player_data['assists'],
        turnovers=player_data['turnovers'],
        two_fg=player_data['twoFg'],
        two_attempts=player_data['twoAttempts'],
        two_percent=player_data['twoPercent'],
        three_fg=player_data['threeFg'],
        three_attempts=player_data['threeAttempts'],
        three_percent=player_data['threePercent']
    )

    player.atr = player.assists / player.turnovers if player.turnovers > 0 else 0
    player.ppg_ratio = avg_points / position_avg.get(position, 1)

    return player