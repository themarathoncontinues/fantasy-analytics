"""App entry point."""
import ast
import re


from flask import redirect, render_template, request, session
from app import create_app

from src.auth import espn_authenticate
from src.league import League


app = create_app()


@app.route('/', methods=['GET'])
def credentials():

	return render_template('login.html')


@app.route('/dashboard', methods=['POST'])
def dashboard():

	if request.method == 'POST':

		league_url = request.values.get('league-url')
		username = request.values.get('username')
		password = request.values.get('password')
		cookies = request.values.get('cookies')
		year = int(request.values.get('league-year'))

		if not (username and password) and cookies == '':
			return 404

		if cookies != '':
			creds = ast.literal_eval(cookies)
		elif (username and password):
			creds = espn_authenticate(username, password)
		else:
			return 404

		league_id = re.search('(?<=leagueId=)(.*)(?=&)', league_url).group()
		team_id = re.search('(?<=teamId=)(.*)', league_url).group()

		session['session_info'] = {
			'creds': creds,
			'league_id': league_id,
			'team_id': team_id,
			'year': int(year)
		}

		league = League(
			league_id=league_id,
			year=year,
			team_id=int(team_id),
			cookies=creds
		)

		return render_template(
			'dashboard.html',
			creds=creds,
			year=int(year),
			league_id=league_id,
			team_id=team_id,
			league_obj=dir(league),
			roster_stats=league.stat_totals
		)


@app.route('/my-team')
def my_team():

	meta = session.get('session_info')

	league = League(
		league_id=meta['league_id'],
		year=meta['year'],
		team_id=int(meta['team_id']),
		cookies=meta['creds']
	)

	info = {
		'session': meta,
		'roster': league._fetch_roster()
	}

	return info


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
