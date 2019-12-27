import datetime
import json
import os
import prefect
import requests

from prefect import Flow, unmapped
from prefect.engine.executors import DaskExecutor
from prefect.utilities.debug import raise_on_exception, state

from src.tasks import models


def build() -> Flow:
    """
    Returns:
        flow: (Flow) flow to be executed
    """
    with Flow("create-db-models") as flow:

        schema = models.create_schema()

        leagues = models.create_leagues_table()
        users = models.create_users_table(upstream_tasks=[leagues])
        matchups = models.create_matchups_table(upstream_tasks=[users])
        rosters = models.create_rosters_table(upstream_tasks=[matchups])
        associations = models.create_associations_table()
        teams = models.create_teams_table(upstream_tasks=[associations])
        players = models.create_players_table(upstream_tasks=[teams, rosters])
        games = models.create_games_table(upstream_tasks=[teams])
        metrics = models.create_metrics_table()
        stats = models.create_stats_table(upstream_tasks=[players, metrics, games])

    return flow


def execute(flow: Flow) -> state:
    """
    Returns:
        state: (state) state of league flow
    """
    with raise_on_exception():
        executor = DaskExecutor(address=os.getenv("WORKER_ADDRESS"))
        state = flow.run()

        return state


def create_models() -> state:
    """
    Caller for flow creating database models

    Returns:
        state: (state) state of league flow
    """
    flow = build()
    state = execute(flow=flow)

    return state.serialize()
