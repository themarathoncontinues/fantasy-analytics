# fantasy-analytics

[![Build Status](https://travis-ci.com/leonkozlowski/fantasy-analytics.svg?branch=master)](https://travis-ci.com/leonkozlowski/fantasy-analytics)

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

![Screen Shot](https://imgur.com/JEryNID.png)


2) `Flow('players_flow)`

* fetch players for every roster in a league

![Screen Shot](https://imgur.com/yjZVgkT.png)