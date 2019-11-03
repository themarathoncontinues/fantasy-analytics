import os

from src.league import League
from src.constants import STATS_INT_TO_STRING
from src.utils.json_util import get_nested

from dotenv import load_dotenv

from pathlib import Path

SRC = Path(os.getcwd()).absolute()
load_dotenv(dotenv_path=f'{SRC}/.env')

espn_s2 = os.environ['espn_s2']
swid = os.environ['swid']

cookies = {
    'espn_s2': espn_s2,
    'swid': swid
}

roster = League(league_id=69561285, year=2020, team_id=4, cookies=cookies).stat_totals
