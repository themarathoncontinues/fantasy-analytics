from prefect.tasks.postgres import PostgresExecute, PostgresFetch

from settings import (
    POSTGRES_DBNAME,
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


existing_tables = PostgresFetch(
    name="query-existing-tables",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    fetch="all",
    query="""
    SELECT * FROM information_schema.tables;
    """,
)

existing_schemas = PostgresFetch(
    name="query-existing-schemas",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    fetch="all",
    query="""
    SELECT * FROM information_schema.schemata;
    """,
)

create_schema = PostgresExecute(
    name="create-fantasy-schema",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE SCHEMA IF NOT EXISTS fantasy_analytics;
    """,
)

"""
Example:
(1, 'League Example', 2020)
"""
create_leagues_table = PostgresExecute(
    name="create-leagues-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.leagues(
        id INTEGER PRIMARY KEY,
        name VARCHAR(512),
        year INTEGER NOT NULL
    );
    """,
)

"""
Users:
(1, 'mitchbregs', 12-12-12T00:00:00Z, false, 55, 'New Jersey Shooters', 'NJM', 1)
"""
create_users_table = PostgresExecute(
    name="create-users-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(128) UNIQUE NOT NULL,
        created_on TIMESTAMP NOT NULL,
        is_premium_member BOOLEAN NOT NULL,
        espn_team_id INTEGER NOT NULL,
        espn_team_name VARCHAR(64),
        espn_team_abbrev VARCHAR(16),
        league_id INTEGER REFERENCES fantasy_analytics.leagues (id)
    );
    """,
)

"""
Matchups:
(1, 1, 2, 12-12-12T00:00:00Z)
"""
create_matchups_table = PostgresExecute(
    name="create-matchups-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.matchups(
        id SERIAL PRIMARY KEY,
        user_1_id INTEGER REFERENCES fantasy_analytics.users (id),
        user_2_id INTEGER REFERENCES fantasy_analytics.users (id),
        played_on TIMESTAMP NOT NULL
    );
    """,
)

"""
Rosters:
(1, 1)
"""
create_rosters_table = PostgresExecute(
    name="create-rosters-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.rosters(
        id SERIAL PRIMARY KEY,
        matchup_id INTEGER REFERENCES fantasy_analytics.matchups (id)
    );
    """,
)

"""
Associations:
(1, 'NBA', 'National Basketball Association')
"""
create_associations_table = PostgresExecute(
    name="create-associations-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.associations(
        id SERIAL PRIMARY KEY,
        abbrev VARCHAR(8),
        name VARCHAR(128)
    );
    """,
)

"""
Teams:
(1, 'Boston Celtics', 1)
"""
create_teams_table = PostgresExecute(
    name="create-teams-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.teams(
        id SERIAL PRIMARY KEY,
        name VARCHAR(256),
        association_id INTEGER REFERENCES fantasy_analytics.associations (id)
    );
    """,
)

"""
Players:
(1, 'Anthony Davis', 1, 1)
"""
create_players_table = PostgresExecute(
    name="create-players-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.players(
        id SERIAL PRIMARY KEY,
        name VARCHAR(128),
        roster_id INTEGER REFERENCES fantasy_analytics.rosters (id),
        team_id INTEGER REFERENCES fantasy_analytics.teams (id)
    );
    """,
)

"""
Games:
(1, 1, 2, 12-12-12T00:00:00Z)
"""
create_games_table = PostgresExecute(
    name="create-games-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.games(
        id SERIAL PRIMARY KEY,
        team_1_id INTEGER REFERENCES fantasy_analytics.teams (id),
        team_2_id INTEGER REFERENCES fantasy_analytics.teams (id),
        played_on TIMESTAMP NOT NULL
    );
    """,
)

"""
Metrics:
(1, 'Points')
"""
create_metrics_table = PostgresExecute(
    name="create-metrics-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.metrics(
        id SERIAL PRIMARY KEY,
        name VARCHAR(32)
    );
    """,
)


"""
Stats:
(1, 1, 1, 25.5, 1)
"""
create_stats_table = PostgresExecute(
    name="create-stats-table",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.stats(
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES fantasy_analytics.players (id),
        metric_id INTEGER REFERENCES fantasy_analytics.metrics (id),
        value DECIMAL,
        game_id INTEGER REFERENCES fantasy_analytics.games (id)
    );
    """,
)
