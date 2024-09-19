from dataclasses import dataclass


@dataclass
class Player:
    player_name: str
    position: str
    team: str
    season: int
    games: int
    points: int
    assists: int
    turnovers: int
    two_fg: float
    two_attempts: float
    two_percent: float
    three_fg: float
    three_attempts: float
    three_percent: float
    atr: float = None
    ppg_ratio: float = None
    id: int = None
