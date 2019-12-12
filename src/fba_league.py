import datetime
import json
import logging
import requests

from prefect import (
    Flow,
    Parameter,
    task,
    unmapped
)

from prefect.utilities.debug import raise_on_exception

from .constants import FBA_ENDPOINT

from .utils.http_util import request_status


logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


@task
def url_generator(year: Parameter, league_id: Parameter, cookies: Parameter):
    """Generate base URL for requests for a given year, league_id and cookies"""
    return f'{FBA_ENDPOINT}{year}/segments/0/leagues/{league_id}'


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=0))
def fetch_league_meta(base_url: str, cookies: Parameter) -> dict:
    """

    :return:
    """
    resp = requests.get(url=base_url, cookies=cookies)

    # raise error for bad response
    request_status(resp.status_code)

    data = resp.json()

    members = [{'id': x['id'], 'name': x['displayName']} for x in data['members']]

    # this index zero is bothering me for now
    teams = [{'id': x['id'], 'owner': x['owners'][0], 'name': x['nickname']} for x in data['teams']]

    meta = {
        'current_week': data['status']['currentMatchupPeriod'],
        'nba_day': data['status']['latestScoringPeriod'],
        'members': members,
        'teams': teams,
        'team_ids': [team.get('id') for team in teams]
    }

    logger.info(f'League Data: {json.dumps(meta, indent=4)}')

    return meta


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=0))
def fetch_team_meta(base_url: str, team_id: int, cookies: Parameter) -> dict:

    params = {
        'view': 'mTeam'
    }

    resp = requests.get(url=base_url, params=params, cookies=cookies)

    request_status(resp.status_code)

    teams = resp.json()['teams']

    logger.info(f' >> Fetching Team: {team_id}')

    # fantasy team ids start at 1 not 0
    current_team = teams[team_id - 1]

    team_meta = {
        'id': team_id,
        'abbrev': current_team['abbrev'],
        'owner': current_team['primaryOwner'],
        'name': current_team['nickname'],
        'record': {
            'w': current_team['record']['overall']['wins'],
            'l': current_team['record']['overall']['losses'],
            't': current_team['record']['overall']['ties']
        },
        'stats': current_team['valuesByStat']
    }

    logger.info(f'My Team Data: {json.dumps(team_meta, indent=4)}')

    return team_meta


def build(year: int, league_id: int, cookies: dict):
    """
    with Parameter
    :return:
    """

    with Flow('league_flow') as flow:
        year = Parameter('year')
        league_id = Parameter('league_id')
        cookies = Parameter('cookies')

        req = url_generator(
            year=year,
            league_id=league_id,
            cookies=cookies
        )

        meta = fetch_league_meta(
            base_url=req,
            cookies=cookies
        )

        fetch = fetch_team_meta.map(
            base_url=unmapped(req),  # this is something to look into
            team_id=meta['team_ids'],
            cookies=unmapped(cookies)
        )

        return flow


def execute(flow: Flow, year: int, league_id: int, cookies: dict):

    with raise_on_exception():
        fout = flow.run(
            year=year,
            league_id=league_id,
            cookies=cookies
        )

        return fout


def runner(year: int, league_id: int, cookies: dict):
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
