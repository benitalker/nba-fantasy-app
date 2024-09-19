from dataclasses import dataclass
from typing import List
from models.Player import Player


@dataclass
class FantasyTeam:
    team_name: str
    players: List[Player]
    id: int = None
