import prefect
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

create_league_table = PostgresExecute(
    name="create-league-table",
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
        league_id INTEGER REFERENCES fantasy_analytics.league (id)
    );
    """,
)

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
        user_id INTEGER REFERENCES fantasy_analytics.users (id)
    );
    """,
)

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
        roster_1_id INTEGER REFERENCES fantasy_analytics.rosters (id),
        roster_2_id INTEGER REFERENCES fantasy_analytics.rosters (id),
        played_on TIMESTAMP NOT NULL
    );
    """,
)
