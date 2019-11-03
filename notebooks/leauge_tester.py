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

roster = League(league_id=69561285, year=2020, team_id=4, cookies=cookies)._calculate_totals()

# entries = roster['roster'].get('entries')
#
# for player in entries:
#     team_stats = []
#     stats = get_nested(player, 'playerPoolEntry.player.stats')
#
#     for statline in stats:
#         if statline.get('statSplitTypeId') == 2:
#             season_totals = statline.get('stats')
#
#             relevant_items = dict((STATS_INT_TO_STRING[k], v) for (k, v) in season_totals.items()
#                                   if k in STATS_INT_TO_STRING.keys())
#
#             player_metadata = {
#                 'name': get_nested(player, 'playerPoolEntry.player.fullName'),
#                 'id': get_nested(player, 'playerPoolEntry.player.id'),
#                 'stats': {
#                     'points': relevant_items.get('points'),
#                     'blocks': relevant_items.get('blocks'),
#                     'steals': relevant_items.get('steals'),
#                     'assists': relevant_items.get('assists'),
#                     'rebounds': relevant_items.get('rebounds')
#                 }
#             }
#
#             team_stats.append(player_metadata)
#
#     print(team_stats)