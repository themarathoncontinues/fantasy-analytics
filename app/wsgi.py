"""App entry point."""
import os
import re

from flask import render_template, request, session

from app import create_app

from src.fba_league import league

from src.fba_players import players

from src.tasks import leagues, users

from src.utils.flask_celery import make_celery


app = create_app()
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_BACKEND'] = os.getenv('CELERY_BACKEND')

celery = make_celery(app)


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


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

        league_id = re.search('(?<=leagueId=)(.*)(?=&)', league_url).group()
        league_id = int(league_id)
        team_id = re.search('(?<=teamId=)(.*)', league_url).group()

        leagues.insert_league.run(
            data=(league_id, None, year)
        )
        users.insert_user.run(
            data=(username, team_id, None, None, league_id)
        )

        return {'created': f'{username}, {team_id}, {league_id}'}


@celery.task(name='wsgi.league')
def fetch_league(meta: dict):
    league_data = league(
        league_id=meta['league_id'],
        year=meta['year'],
        cookies=meta['creds']
    )

    return league_data


@celery.task(name='wsgi.league')
def fetch_players(meta: dict):
    info = {
        'session': meta,
        'roster': players(
            league_id=meta['league_id'],
            year=meta['year'],
            cookies=meta['creds']
        )
    }

    return info


@app.route('/my-team')
def my_team():
    meta = session.get('session_info')

    fetch_league.delay(meta)
    fetch_players.delay(meta)

    return 'Celery Tasks!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
