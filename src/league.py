import json
import logging
import requests

from .constants import FBA_ENDPOINT

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

class League(object):
    """Get league instance from ESPN"""
    def __init__(self, league_id: int, year: int, team_id: int, cookies, debug=False):
        self.league_id = league_id
        self.year = year
        self.current_week = 0
        self.nba_week = 0
        self.team_id = team_id
        self.cookies = cookies
        if self.cookies:
            self.cookies = cookies
        else:
            logger.error(f'No Authorization Credentials')
            raise Exception

        self._fetch_league()
        self._fetch_team_id()
        self._fetch_teams()

    def __repr__(self):
        return f'League: {self.league_id} Year: {self.year}'

    def _fetch_league(self):
        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params='', cookies=self.cookies)

        self.status = resp.status_code

        league_data = resp.json()
        logger.info(f'League Data: {json.dumps(league_data, indent=4)}')

        self.current_week = league_data['status']['currentMatchupPeriod']
        self.nba_week = league_data['status']['latestScoringPeriod']

    def _fetch_team_id(self):
        params = {
            'view': 'mTeam'
        }

        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params=params, cookies=self.cookies)

        self.status = resp.status_code

        teams = resp.json()['teams']

        # NOTE: This can be fixed up to be faster
        team_id_data = [x for x in teams if x.get('id') == self.team_id]

        logger.info(f'My Team Data: {json.dumps(team_id_data, indent=4)}')

    def _fetch_teams(self):
        params = {
            'view': 'mTeam'
        }

        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params=params, cookies=self.cookies)

        self.status = resp.status_code

        team_data = resp.json()

    def _fetch_players(self):
        # here we will get players on waiver wire
        params = {
            'scoringPeriod': self.current_week,
            'view': 'players_wl'
        }
        pass

