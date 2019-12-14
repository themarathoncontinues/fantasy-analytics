import datetime
import json
import logging
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

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


@task
def url_generator(year: Parameter, league_id: Parameter, cookies: Parameter):
    """Generate base URL for requests for a given year, league_id and cookies"""
    return f'{FBA_ENDPOINT}{year}/segments/0/leagues/{league_id}'


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=0))
def fetch_rosters(base_url: str, cookies: Parameter) -> dict:
    """

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
                'fullName': player_obj.full_name
            })

        logger.debug(f' >> Team {team_obj.team_id}'
                    f'Roster: {json.dumps(rosters.get(team_obj.team_id,), indent=4)}')

    return rosters


def build(year: int, league_id: int, cookies: dict) -> Flow:
    """
    with Parameter
    :return:
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

    with raise_on_exception():
        fout = flow.run(
            year=year,
            league_id=league_id,
            cookies=cookies
        )

        return fout


def players(year: int, league_id: int, cookies: dict) -> state:
    flow = build(
        year=year,
        league_id=league_id,
        cookies=cookies
    )

    fout = execute(
        flow=flow,
        year=year,
        league_id=league_id,
        cookies=cookies
    )

    flow.visualize()

    return fout
