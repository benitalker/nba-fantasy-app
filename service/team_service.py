from repository.player_repository import get_player_position_by_id
from repository.team_repository import create_team, update_team, delete_team, get_team_by_id, get_team_by_id_statistic
from typing import List
from statistics import mean

def create_new_team(team_name: str, player_ids: List[int]) -> int:
    validate_team(player_ids)
    team_id = create_team(team_name)
    update_team(team_id, player_ids)
    return team_id

def update_existing_team(team_id: int, player_ids: List[int]) -> bool:
    validate_team(player_ids)
    return update_team(team_id, player_ids)

def remove_team(team_id: int) -> bool:
    return delete_team(team_id)

def retrieve_team(team_id: int) -> dict:
    return get_team_by_id(team_id)

def validate_team(player_ids: List[int]):
    if len(player_ids) < 5:
        raise ValueError("A team must have at least 5 players.")
    positions = set()
    for player_id in player_ids:
        position = get_player_position_by_id(player_id)
        positions.add(position)
    if len(positions) < 5:
        raise ValueError("Team must have at least one player in each position.")

def compare_teams(team_ids: list[int]) -> list[dict] | None:
    teams = []

    for team_id in team_ids:
        team = get_team_by_id_statistic(team_id)
        if not team:
            return None

        # Calculate statistics for the team, ensuring None values are ignored
        points = sum(player['points'] for player in team['players'] if player['points'] is not None)
        two_percent = mean(player['two_percent'] for player in team['players'] if player['two_percent'] is not None)
        three_percent = mean(player['three_percent'] for player in team['players'] if player['three_percent'] is not None)
        atr = mean(player['atr'] for player in team['players'] if player['atr'] is not None)
        ppg_ratio = mean(player['ppg_ratio'] for player in team['players'] if player['ppg_ratio'] is not None)

        teams.append({
            'team': team['team_name'],
            'points': points,
            'twoPercent': two_percent,
            'threePercent': three_percent,
            'ATR': atr,
            'PPG_Ratio': ppg_ratio
        })

    teams.sort(key=lambda t: t['PPG_Ratio'], reverse=True)

    return teams
