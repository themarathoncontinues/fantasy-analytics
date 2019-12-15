import json
import mock
import os
import pytest

from prefect import (
    Flow,
)

from src.fba_players import (
    fetch_rosters,
    build,
    execute,
    players
)


class MockRequestsObject(dict):
    def __init__(self, data: dict):
        super(MockRequestsObject, self).__init__(data)

    @property
    def status_code(self):
        return 200

    @property
    def json(self):
        return self

    def __call__(self):
        return self.json


def test_flow_build():
    test_flow = build(
        year=2020,
        league_id=1234,
        cookies={}
    )

    assert isinstance(test_flow, Flow)


@mock.patch('src.fba_players.execute')
def test_league_runner_pass(mock_execute_state):
    mock_execute_state.return_value = True

    result = players(
        year=2020,
        league_id=1234,
        cookies={}
    )

    assert result is True


@mock.patch('requests.get')
@mock.patch('prefect.context')
def test_fetch_rosters_pass(mock_prefect_context, mock_request):
    mock_json = _resolve_relative_import('testData/rosters_meta_response.json')

    mock_prefect_context.return_value = 'logger'
    mock_request.return_value = MockRequestsObject(data=mock_json)

    result = fetch_rosters.run(
        base_url='someUrl',
        cookies={
            'swid': 'someSwid'
        }
    )

    assert isinstance(result, dict)
    assert len(result.get(1)) == 16


def test_execute_flow_raises():
    test_flow = build(
        year=2020,
        league_id=1234,
        cookies={}
    )

    with pytest.raises(Exception):
        execute(
            flow=test_flow,
            year=2020,
            league_id=1234,
            cookies={}
        )


def test_league_raises():
    with pytest.raises(Exception):
        players(
            year=2020,
            league_id=1234,
            cookies={}
        )


def _resolve_relative_import(test_file):
    in_file = os.path.join(os.path.dirname(__file__), test_file)
    with open(in_file) as f:
        raw_json = f.read()
        return json.loads(raw_json)
