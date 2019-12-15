# fantasy-analytics

<p align="center">
<a href="https://travis-ci.com/leonkozlowski/fantasy-analytics"><img alt="Build Status" src="https://travis-ci.com/leonkozlowski/fantasy-analytics.svg?branch=master"></a>
<a href='https://coveralls.io/github/themarathoncontinues/fantasy-analytics'><img src='https://coveralls.io/repos/github/themarathoncontinues/fantasy-analytics/badge.svg' alt='Coverage Status' /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

#### Authors

* **Mitchell Bregman**
* **Leon Kozlowski**

## Setup

```bash
$ git clone https://github.com/themarathoncontinues/fantasy-analytics.git
$ cd fantasy-analytics

$ python3.6 -m venv venv
$ source venv/bin/activate

$ pip install -e .
```

## Local Testing
In order to see any logger level logs test locally

```bash
$ echo "espn_s2 = {your_espn_s2_here}" >> .env
$ echo "swid = {your_swid_here}" >> .env
$ echo "username = {your_username_here}" >> .env
$ echo "password = {your_password_here}" >> .env

$ python notebooks/league_tester.py
```

## Flows
With [Prefect](https://github.com/PrefectHQ/prefect) flows all downstream and upstream tasks can be tracked

1) `Flow('league_flow')`

* fetch league metadata for a given league and year
<p align="center">
  <img width="499", height="639" src="https://imgur.com/JEryNID.png">


2) `Flow('players_flow)`

* fetch players for every roster in a league
<p align="center">
  <img width="443.5", height="400" src="https://imgur.com/yjZVgkT.png">
