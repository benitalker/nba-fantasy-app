from toolz import curry, pipe
from models.Player import Player
from repository.player_repository import get_player_position_by_id
from repository.team_repository import (
    create_team, update_team, delete_team,
    get_team_by_id, get_team_by_id_statistic,
    get_team_by_name_statistic
)
from typing import List, Dict, Optional
from statistics import mean

# Functions to manage teams
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

# Functions to calculate team stats
def calculate_team_stats_from_players(team: Dict[str, any]) -> Dict[str, any]:
    players = team['players']  # This should be a list of Player objects
    return {
        'team': team['team_name'],
        'points': sum(getattr(player, 'points', 0) for player in players),
        'twoPercent': safe_mean('two_percent', players),
        'threePercent': safe_mean('three_percent', players),
        'ATR': safe_mean('atr', players),
        'PPG_Ratio': safe_mean('ppg_ratio', players)
    }

def calculate_team_stats_from_dict(team: Dict[str, any]) -> Dict[str, any]:
    players = team['players']  # This should be a list of player dictionaries
    return {
        'team': team['team_name'],
        'points': sum(player.get('points', 0) for player in players),
        'twoPercent': safe_mean_dict('two_percent', players),
        'threePercent': safe_mean_dict('three_percent', players),
        'ATR': safe_mean_dict('atr', players),
        'PPG_Ratio': safe_mean_dict('ppg_ratio', players)
    }

@curry
def safe_mean(key: str, players: List[Player]) -> float:
    values = [getattr(player, key, 0) for player in players if getattr(player, key, None) is not None]
    return mean(values) if values else 0.0

@curry
def safe_mean_dict(key: str, players: List[Dict[str, any]]) -> float:
    values = [player.get(key, 0) for player in players if player.get(key) is not None]
    return mean(values) if values else 0.0

def sort_teams(teams: List[Dict[str, any]]) -> List[Dict[str, any]]:
    return sorted(teams, key=lambda t: t['PPG_Ratio'], reverse=True)

@curry
def process_team(get_team_func, team_identifier, use_dict=False):
    return pipe(
        team_identifier,
        get_team_func,
        lambda team: None if team is None else (
            calculate_team_stats_from_dict(team) if use_dict else calculate_team_stats_from_players(team)
        )
    )

def compare_teams(team_ids: List[int]) -> Optional[List[Dict[str, any]]]:
    return pipe(
        team_ids,
        lambda ids: map(process_team(get_team_by_id_statistic, use_dict=False), ids),
        list,
        lambda teams: None if None in teams else teams,
        lambda teams: sort_teams(teams) if teams is not None else None
    )

def compare_teams_by_name(team_names: List[str]) -> Optional[List[Dict[str, any]]]:
    return pipe(
        team_names,
        lambda names: map(process_team(get_team_by_name_statistic, use_dict=False), names),
        list,
        lambda teams: None if None in teams else teams,
        lambda teams: sort_teams(teams) if teams is not None else None
    )
