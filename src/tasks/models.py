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
    name='query-existing-tables',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    fetch="all",
    query="""
    SELECT * FROM information_schema.tables;
    """
)

existing_schemas = PostgresFetch(
    name='query-existing-schemas',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    fetch="all",
    query="""
    SELECT * FROM information_schema.schemata;
    """
)

create_schema = PostgresExecute(
    name='create-fantasy-schema',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE SCHEMA IF NOT EXISTS fantasy_analytics;
    """
)

create_users_table = PostgresExecute(
    name='create-users-table',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.users(
        id SERIAL PRIMARY KEY,
        email VARCHAR(128) UNIQUE NOT NULL,
        created_on TIMESTAMP NOT NULL
    );
    """
)

create_rosters_table = PostgresExecute(
    name='create-rosters-table',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    # upstream_tasks=['create_users_table'],
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.rosters(
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES fantasy_analytics.users (id)
    );
    """
)

create_matchups_table = PostgresExecute(
    name='create-matchups-table',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    # upstream_tasks=['create_rosters_table'],
    query="""
    CREATE TABLE IF NOT EXISTS fantasy_analytics.matchups(
        id SERIAL PRIMARY KEY,
        roster_1_id INTEGER REFERENCES fantasy_analytics.rosters (id),
        roster_2_id INTEGER REFERENCES fantasy_analytics.rosters (id),
        played_on TIMESTAMP NOT NULL
    );
    """
)

