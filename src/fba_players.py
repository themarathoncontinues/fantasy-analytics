import datetime
import json
import prefect
import requests

from .constants import FBA_ENDPOINT

from prefect import (
    Flow,
    Parameter,
    task,
)

from prefect.utilities.debug import (
    raise_on_exception,
    state
)

from src.utils.http_util import request_status

from src.utils.object_util import (
    RosterAccess,
    RosterEntryAccess
)


@task
def url_generator(year: Parameter, league_id: Parameter, cookies: Parameter):
    """Generate base URL for requests for a given year, league_id and cookies"""
    return f'{FBA_ENDPOINT}{year}/segments/0/leagues/{league_id}'


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=0))
def fetch_rosters(base_url: str, cookies: Parameter) -> dict:
    """
    Fetch rosters for league id
    Args:
        base_url: (str) base espn api url
        cookies: (dict) auth for requests to base_url
    Returns:
        rosters: (dict) containing all rosters from league
        (i.e)
            {
                1:  [
                        {
                            'id': 6583,
                            'name': 'Anthony Davis'
                        },
                        {
                            'id': 6450,
                            'name': 'Kawhi Leonard'
                        },
                        {
                            'id': 6479,
                            'name': 'Kemba Walker'
                        },
                        .
                        .
                        .
                    ],
                .
                .
                .
                10: [
                        {
                        'id': 3992,
                        'name': 'James Harden'
                        },
                        {
                            'id': 6478,
                            'name': 'Nikola Vucevic'
                        },
                        {
                            'id': 3995,
                            'name': 'Jrue Holiday'
                        },
                        .
                        .
                        .
                    ]
            }

    """
    roster_logger = prefect.context['logger']

    params = {
        'view': 'mRoster'
    }

    resp = requests.get(url=base_url, params=params, cookies=cookies)

    request_status(resp.status_code)

    data = resp.json()

    rosters = {}
    for team in data['teams']:
        team_obj = RosterAccess(team)
        rosters[team_obj.team_id] = []

        for player in team_obj.entries:
            player_obj = RosterEntryAccess(player)

            rosters[team_obj.team_id].append({
                'playerId': player_obj.player_id,
                'fullName': player_obj.full_name,
                'stats': player_obj.stats  # NOTE: we need to find a way to index this (maybe db level?)
            })

        roster_logger.debug(f' >> Team {team_obj.team_id} '
                            f'Roster: {json.dumps(rosters.get(team_obj.team_id,), indent=4)}')

    return rosters


def build(year: int, league_id: int, cookies: dict) -> Flow:
    """
    Flow builder with relevant tasks (increase modularity and abstraction)
    Args:
        year: (int) - year in which to make requests
        league_id: (int) - league id in which to make requests
        cookies: (dict) - auth cookies
    Returns:
        flow: (Flow) flow to be executed
    """
    with Flow('players_flow') as flow:
        year = Parameter('year')
        league_id = Parameter('league_id')
        cookies = Parameter('cookies')

        req = url_generator(
            year=year,
            league_id=league_id,
            cookies=cookies
        )

        fetch_rosters(
            base_url=req,
            cookies=cookies
        )

        return flow


def execute(flow: Flow, year: int, league_id: int, cookies: dict) -> state:
    """
    Flow executor/runner (increases abstraction)
    Args:
        flow: (Flow) flow to be executed
        year: (int) - year in which to make requests
        league_id: (int) - league id in which to make requests
        cookies: (dict) - auth cookies
    Returns:
        players_state: (state) state of league flow
    """
    with raise_on_exception():
        players_state = flow.run(
            year=year,
            league_id=league_id,
            cookies=cookies
        )

        return players_state


def players(year: int, league_id: int, cookies: dict) -> state:
    """
    Caller for league flow (independent from build and run to increase modularity)
    Args:
        year: (int) - year in which to make requests
        league_id: (int) - league id in which to make requests
        cookies: (dict) - auth cookies
    Returns:
        league_state: (state) state of league flow
    """
    flow = build(
        year=year,
        league_id=league_id,
        cookies=cookies
    )

    players_state = execute(
        flow=flow,
        year=year,
        league_id=league_id,
        cookies=cookies
    )

    # flow.visualize()

    return players_state
