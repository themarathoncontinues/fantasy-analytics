import prefect
from prefect.tasks.postgres import PostgresFetch

from settings import (
    POSTGRES_DBNAME,
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


existing = PostgresFetch(
    name='query-existing-tables',
    db_name=POSTGRES_DBNAME,
    user=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    fetch="all",
    tags=["projects"],
    query="""
    SELECT * FROM information_schema.tables
    """
)

