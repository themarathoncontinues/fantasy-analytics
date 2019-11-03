from src.league import League

cookies = {'espn_s2': 'AEBOWNkcIP1JC4HYn8pKEGJHRJcTKXuYj%2BCj8mZsBx8gvMloxR6OmnDVbY%2FRTvWKDTsoVuZ%2FBmUt3EhnTXa%2FfkSzcVTH8cLcQaj0DjwqjxCY3eH6X64tqBpk9wCnUMOYXN7IdRyRcn5Rle9wQY1ZxsQNVDJW4fROPu3nQsE7jd7k61KSxnciVSlg6MReQV8OJzIhDSAgOILzS40dQ15cGTXy0EMx3jriEwAnif0ax1hfYKODdx4gpcrHw%2FlMW6nvkZAMuAZ9g%2F%2F4LqTSsFwSKLrX', 'swid': '{DD012212-1A35-417E-9883-4B1E44BDF89C}'}

my_league = League(league_id=69561285, year=2020, team_id=4, cookies=cookies)

print(my_league)