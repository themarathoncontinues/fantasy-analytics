import json
import os
import pytest

from src.utils.http_util import request_status

from src.utils.object_util import (
    RosterAccess,
    RosterEntryAccess,
    TeamMetaAccess
)


# http_util.py tests
@pytest.mark.parametrize('status, exception', [(500, Exception),(401, Exception),(404, Exception)])
def test_request_status_raises(status, exception):
    with pytest.raises(exception):
        request_status(status)


@pytest.mark.parametrize('status', [202, 200])
def test_request_status_passes(status):
    result = request_status(status)

    assert result is None


# object_util.py tests
def test_roster_access():
    test_roster_input = _resolve_relative_import('testData/roster_access.json')
    test_roster_object = RosterAccess(test_roster_input)

    assert test_roster_object.team_id == 1
    assert isinstance(test_roster_object.roster, dict)
    assert len(test_roster_object.entries) == 16


def test_roster_entry_access():
    test_entry_input = _resolve_relative_import('testData/roster_entry_access.json')
    test_entry_object = RosterEntryAccess(test_entry_input)

    assert test_entry_object.player_id == 6583
    assert isinstance(test_entry_object.player_pool_entry, dict)
    assert isinstance(test_entry_object.player, dict)
    assert test_entry_object.full_name == 'Anthony Davis'
    assert isinstance(test_entry_object.stats, list)


def test_team_meta_access():
    test_team_input = _resolve_relative_import('testData/team_meta_access.json')
    test_team_object = TeamMetaAccess(test_team_input)

    assert test_team_object.abbrev == "MIA"
    assert test_team_object.nick_name == "Sammy "
    assert isinstance(test_team_object.values_by_stat, dict)
    assert isinstance(test_team_object.record, dict)
    assert test_team_object.primary_owner == "{dummyValue}"
    assert test_team_object.wins == 5
    assert test_team_object.losses == 2
    assert test_team_object.ties == 0


def _resolve_relative_import(test_file):
    in_file = os.path.join(os.path.dirname(__file__), test_file)
    with open(in_file) as f:
        raw_json = f.read()
        return json.loads(raw_json)
