"""App entry point."""
import logging
import os
import re

from flask import flash, jsonify, redirect, render_template, request, session, url_for

from app import create_app

from src.auth import espn_authenticate

from src.fba_league import league

from src.fba_players import players

from src.utils.flask_celery import make_celery

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

app = create_app()
app.config["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL")
app.config["CELERY_BACKEND"] = os.getenv("CELERY_BACKEND")

celery = make_celery(app)


def dir_last_updated(folder):
    return str(
        max(
            os.path.getmtime(os.path.join(root_path, f))
            for root_path, dirs, files in os.walk(folder)
            for f in files
        )
    )


@app.route("/", methods=["GET"])
def credentials():
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":

        league_url = request.values.get("league-url")
        username = request.values.get("username")
        password = request.values.get("password")
        cookies = espn_authenticate(user=username, pwd=password)
        year = int(request.values.get("league-year"))

        league_id = re.search("(?<=leagueId=)(.*)(?=&)", league_url).group()
        league_id = int(league_id)

        meta = {"league_id": league_id, "year": year, "creds": cookies}

        task = fetch_league.apply_async(args=[meta])

        return (
            jsonify(
                {"status": 202, "taskId": task.id, "leagueId": league_id, "year": year}
            ),
            202,
        )  # {'bar-prog': url_for('taskstatus', task_id=task.id)}


@app.route("/status/<task_id>")
def taskstatus(task_id):
    task = fetch_league.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),
        }

    return jsonify(response)


@celery.task(bind=True, name="wsgi.fetch_league")
def fetch_league(self, meta):
    league(league_id=meta["league_id"], year=meta["year"], cookies=meta["creds"])

    self.update_state(state="PROGRESS")

    return self


@celery.task(name="wsgi.fetch_players")
def fetch_players(meta):
    return players(
        league_id=meta["league_id"], year=meta["year"], cookies=meta["creds"]
    )


@app.route("/my-team", methods=["POST"])
def my_team():
    meta = session.get("session_info")

    fetch_league.delay(meta)
    fetch_players.delay(meta)
    flash(f'Aggregating data for {meta["league_id"]}')

    return redirect(url_for("/my-team"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
