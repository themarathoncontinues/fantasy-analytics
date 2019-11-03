"""App entry point."""
import ast

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

		leage_url = request.values.get('league-url')
		username = request.values.get('username')
		password = request.values.get('password')
		cookies = request.values.get('cookies')

		if not (username and password) and cookies == '':
			return 404

		if cookies != '':
			creds = ast.literal_eval(cookies)
		elif (username and password):
			creds = espn_authenticate(username, password)
		else:
			return 404

		session['espn_cred_cookies'] = creds

		return render_template(
			'dashboard.html',
			creds=creds
		)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
