import prefect
from prefect.tasks.postgres import PostgresExecute, PostgresFetch

from settings import (
    POSTGRES_DBNAME,
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


insert_user = PostgresExecute(
    name="insert-user",
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    query="""
    INSERT INTO fantasy_analytics.users (
        username,
        created_on,
        is_premium_member,
        espn_team_id,
        espn_team_name,
        espn_team_abbrev,
        league_id
    ) VALUES (
        %s,
        NOW(),
        false,
        %s,
        %s,
        %s,
        %s
    ) ON CONFLICT DO NOTHING
    """,
)
