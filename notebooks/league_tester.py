import os

from src.fba_league import league
from src.fba_players import players

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


def tester():
    league_data = league(
        year=2020,
        league_id=69561285,
        cookies=cookies
    )

    player_data = players(
        year=2020,
        league_id=69561285,
        cookies=cookies
    )


if __name__ == '__main__':
    tester()
