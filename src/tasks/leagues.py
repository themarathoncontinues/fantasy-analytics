import prefect
from prefect.tasks.postgres import PostgresExecute, PostgresFetch

from settings import (
    POSTGRES_DBNAME,
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


insert_league = PostgresExecute(
    name='insert-league',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    INSERT INTO fantasy_analytics.leagues (
        id,
        name,
        year
    ) VALUES (
        %s,
        %s,
        %s
    ) ON CONFLICT DO NOTHING
    """
)

