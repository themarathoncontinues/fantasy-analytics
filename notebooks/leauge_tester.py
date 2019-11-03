from src.league import League

cookies = {
    'espn_s2': 'something',
    'swid': 'swid'
}

my_league = League(league_id=69561285, year=2020, team_id=4, cookies=cookies)

print(my_league)