# pylint: skip-file
# flake8: noqa

########
# ESPN #
########

FBA_ENDPOINT = "https://fantasy.espn.com/apis/v3/games/fba/seasons/"
URL_API_KEY = "https://registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/api-key?langPref=en-US"
URL_LOGIN = "https://ha.registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/guest/login?langPref=en-US"

#################
# STATS MAPPING #
#################

STATS_INT_TO_STRING = {
    "0": "points",
    "1": "blocks",
    "2": "steals",
    "3": "assists",
    "6": "rebounds",
}
