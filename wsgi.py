"""App entry point."""
import ast
import re

from flask import redirect, render_template, request, session
from app import create_app

from utils.auth import espn_authenticate


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
		year = request.values.get('league-year')

		if not (username and password) and cookies == '':
			return 404

		if cookies != '':
			creds = ast.literal_eval(cookies)
		elif (username and password):
			creds = espn_authenticate(username, password)
		else:
			return 404

		session['espn_cred_cookies'] = creds
		league_id = re.search('(?<=leagueId=)(.*)(?=&)', league_url).group()
		team_id = re.search('(?<=teamId=)(.*)', league_url).group()

		return render_template(
			'dashboard.html',
			creds=creds,
			year=int(year),
			league_id=league_id,
			team_id=team_id
		)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
