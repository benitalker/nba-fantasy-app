from repository.database import is_tables_exists, create_tables, drop_all_tables
from repository.player_repository import load_players


def seed():
    if not is_tables_exists():
        create_tables()
        is_tables_exists()
        load_players()
    # drop_all_tables()
