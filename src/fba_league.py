import datetime
import json
import prefect
import requests

from prefect import Flow, Parameter, task, unmapped

from prefect.utilities.debug import raise_on_exception, state

from .constants import FBA_ENDPOINT

from .utils.http_util import request_status

from .utils.object_util import TeamMetaAccess


@task
def url_generator(year: Parameter, league_id: Parameter):
    """
    Generate base URL for requests for a given year, league_id and cookies
    Args:
        year: (Parameter) - user season year
        league_id: (Parameter) - user league id

    Returns:
         (str) - request URL
    """
    return f"{FBA_ENDPOINT}{year}/segments/0/leagues/{league_id}"


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=0))
def fetch_league_meta(base_url: str, cookies: Parameter) -> dict:
    """
    Fetch relevant metadata on a league level
    Args:
        base_url: (str) - request url via url_generator
        cookies: (dict) - auth cookies
    Returns:
         meta: (dict) - metadata for league_id within base_url
    """
    league_meta_logger = prefect.context["logger"]

    resp = requests.get(url=base_url, cookies=cookies)

    # raise error for bad response
    request_status(resp.status_code)

    data = resp.json()

    members = [{"id": x["id"], "name": x["displayName"]} for x in data["members"]]

    # this index zero is bothering me for now
    teams = [
        {"id": x["id"], "owner": x["owners"][0], "name": x["nickname"]}
        for x in data["teams"]
    ]

    meta = {
        "current_week": data["status"].get("currentMatchupPeriod", None),
        "nba_day": data["status"].get("latestScoringPeriod", None),
        "members": members,
        "teams": teams,
        "team_ids": [team.get("id") for team in teams],
    }

    league_meta_logger.debug(f"League Data: {json.dumps(meta, indent=4)}")

    return meta


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=0))
def fetch_team_meta(base_url: str, team_id: int, cookies: Parameter) -> dict:
    """
    Fetch relevant metadata on a team level
    Args:
        base_url: (str) - request url via url_generator
        team_id: (int) - team id for team to fetch metadata
        cookies: (dict) - auth cookies
    Returns:
        team_meta: (dict) relevant team metadata for each team in a league
        (i.e.)
            {
                "id": 8,
                "abbrev": "FOOT",
                "owner": "{XZY-192-192}",
                "name": "Feet",
                "record": {
                        "w": 4,
                        "l": 2,
                        "t": 1
                },
                "stats": {
                        "0": 5597.0,
                        "1": 198.0,
                        "2": 281.0,
                        "3": 1237.0,
                        "37": 63.0,
                        "6": 1820.0,
                        "38": 3.0,
                        "7": 1.0,
                        "8": 6.0,
                        "10": 16.0,
                        "11": 732.0,
                        "12": 7.0,
                        "13": 2005.0,
                        "14": 4545.0,
                        "15": 982.0,
                        "17": 605.0,
                        "19": 0.44114411
                }
            }
    """
    team_meta_logger = prefect.context["logger"]

    params = {"view": "mTeam"}

    resp = requests.get(url=base_url, params=params, cookies=cookies)
    request_status(resp.status_code)
    teams = resp.json()["teams"]

    # team_id index starts at 1
    team = TeamMetaAccess(teams[team_id - 1])
    is_current_user = team.primary_owner == cookies["swid"]

    team_meta = {
        "id": team_id,
        "abbrev": team.abbrev,
        "owner": team.primary_owner,
        "name": team.nick_name,
        "record": {"w": team.wins, "l": team.losses, "t": team.ties},
        "stats": team.values_by_stat,
        "isCurrentUser": is_current_user,
    }

    team_meta_logger.info(
        f"id: {team_meta.get('id')}"
        f"isCurrentUser {team_meta.get('isCurrentUser')}"
    )

    return team_meta


def build(year: int, league_id: int, cookies: dict) -> Flow:
    """
    Flow builder with relevant tasks
    (increase modularity and abstraction)
    Args:
        year: (int) - year in which to make requests
        league_id: (int) - league id in which to make requests
        cookies: (dict) - auth cookies
    Returns:
        flow: (Flow) flow to be executed
    """
    with Flow("league_flow") as flow:
        year = Parameter("year")
        league_id = Parameter("league_id")
        cookies = Parameter("cookies")

        req = url_generator(year=year, league_id=league_id)

        meta = fetch_league_meta(base_url=req, cookies=cookies)

        fetch_team_meta.map(
            base_url=unmapped(req), team_id=meta["team_ids"], cookies=unmapped(cookies),
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
        league_state: (state) state of league flow
    """
    with raise_on_exception():
        league_state = flow.run(year=year, league_id=league_id, cookies=cookies)

        return league_state


def league(year: int, league_id: int, cookies: dict) -> state:
    """
    Caller for league flow
    (independent from build and run to increase modularity)
    Args:
        year: (int) - year in which to make requests
        league_id: (int) - league id in which to make requests
        cookies: (dict) - auth cookies
    Returns:
        league_state: (state) state of league flow
    """
    flow = build(year=year, league_id=league_id, cookies=cookies)

    league_state = execute(flow=flow, year=year, league_id=league_id, cookies=cookies)

    # flow.visualize()

    return league_state
