from typing import List
import requests
from models.Player import Player


def fetch_data(season) -> List[Player]:
    url = f"http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={season}&pageSize=10"
    response = requests.get(url)
    data = response.json()

    position_stats = {}
    for player_data in data:
        position = player_data['position']
        points = player_data['points']
        games = player_data['games']
        if games > 0:
            avg_points = points / games
            if position not in position_stats:
                position_stats[position] = {'total_points': 0, 'total_games': 0}
            position_stats[position]['total_points'] += points
            position_stats[position]['total_games'] += games

    position_avg = {pos: stats['total_points'] / stats['total_games'] for pos, stats in position_stats.items()}

    players = []
    for player_data in data:
        position = player_data['position']
        points = player_data['points']
        games = player_data['games']
        if games > 0:
            avg_points = points / games
        else:
            avg_points = 0

        player = Player(
            player_name=player_data['playerName'],
            position=position,
            team=player_data['team'],
            season=season,
            games=games,
            points=points,
            assists=player_data['assists'],
            turnovers=player_data['turnovers'],
            two_fg=player_data['twoFg'],
            two_attempts=player_data['twoAttempts'],
            three_fg=player_data['threeFg'],
            three_attempts=player_data['threeAttempts']
        )
        player.atr = player.assists / player.turnovers if player.turnovers > 0 else 0
        player.ppg_ratio = avg_points / position_avg.get(position, 1)
        players.append(player)

    return players
