from typing import List
import requests
from models.Player import Player
from service.creating_player_service import compute_position_stats, create_player


def fetch_data(season: int) -> List[Player]:
    url = f"http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={season}&pageSize=1000"
    response = requests.get(url)
    data = response.json()

    position_stats = compute_position_stats(data)

    players = [create_player(player_data, position_stats) for player_data in data]

    return players
