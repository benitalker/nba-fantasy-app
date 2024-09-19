import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI

def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)

def create_tables():
    create_table_players()
    create_table_teams()
    create_table_team_players()

def create_table_players():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            player_name VARCHAR(100) NOT NULL,
            position VARCHAR(10) NOT NULL,
            team VARCHAR(10) NOT NULL,   
            season INTEGER NOT NULL,
            games INTEGER,
            points FLOAT,
            assists FLOAT,
            turnovers FLOAT,
            two_fg FLOAT,
            two_attempts FLOAT,
            two_percent FLOAT,
            three_fg FLOAT,
            three_attempts FLOAT,
            three_percent FLOAT,
            atr FLOAT,
            ppg_ratio FLOAT
        )
        ''')
        connection.commit()

def create_table_teams():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            team_name VARCHAR(100) NOT NULL
        )
        ''')
        connection.commit()

def create_table_team_players():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_players (
            team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
            player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
            PRIMARY KEY (team_id, player_id)
        )
        ''')
        connection.commit()

def is_tables_exists() -> bool:
    table_names = ['players', 'teams', 'team_players']
    existing_tables = []

    with get_db_connection() as connection, connection.cursor() as cursor:
        for table_name in table_names:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table_name,))

            if cursor.fetchone()['exists']:
                existing_tables.append(table_name)
    print("The following tables exist:", ", ".join(existing_tables))
    if set(existing_tables) == set(table_names):
        print("All tables have been created successfully.")
        return True
    else:
        print("Missing tables:", ", ".join(set(table_names) - set(existing_tables)))
        return False

def drop_all_tables():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            DROP TABLE IF EXISTS team_players;
            DROP TABLE IF EXISTS teams;
            DROP TABLE IF EXISTS players;
        ''')
        connection.commit()
        print("All tables dropped successfully.")
