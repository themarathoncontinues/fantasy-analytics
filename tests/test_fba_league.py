import json
import mock
import os
import pytest

from prefect import (
    Flow,
)

from src.fba_league import (
    url_generator,
    fetch_league_meta,
    fetch_team_meta,
    build,
    execute,
    league
)

from src.constants import FBA_ENDPOINT


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


class MockFlowResponse(dict):
    def __init__(self, data: dict):
        super(MockFlowResponse, self).__init__(data)

    @property
    def serialize(self):
        return self

    def __call__(self):
        return self.serialize


def test_flow_build():
    test_flow = build(
        year=2020,
        league_id=1234,
        cookies={}
    )

    assert isinstance(test_flow, Flow)


def test_url_generator():
    test_year = 2020
    test_league_id = 1234

    result = url_generator.run(
        year=test_year,
        league_id=test_league_id
    )

    assert result == f"{FBA_ENDPOINT}2020/segments/0/leagues/1234"


@mock.patch('requests.get')
@mock.patch('prefect.context')
def test_fetch_league_meta(mock_prefect_context, mock_request):
    mock_json = _resolve_relative_import('testData/league_meta_response.json')

    mock_prefect_context.return_value = 'logger'
    mock_request.return_value = MockRequestsObject(data=mock_json)

    result = fetch_league_meta.run(
        base_url='someUrl',
        cookies={
            'some': 'cookies'
        }
    )

    assert isinstance(result, dict)


@pytest.mark.parametrize('team_id',
                         [
                             1,
                             2,
                             3,
                             4,
                             5,
                             6,
                             7,
                             8,
                             9,
                             10
                         ])
@mock.patch('requests.get')
@mock.patch('prefect.context')
def test_fetch_team_meta(mock_prefect_context, mock_request, team_id):
    mock_json = _resolve_relative_import('testData/team_meta_response.json')

    mock_prefect_context.return_value = 'logger'
    mock_request.return_value = MockRequestsObject(data=mock_json)

    result = fetch_team_meta.run(
        base_url='someUrl',
        team_id=team_id,
        cookies={
            'swid': 'someSwid'
        }
    )

    assert result.get('id') == team_id
    assert isinstance(result.get('record'), dict)
    assert result.get('isCurrentUser') is False


def test_execute_flow_exception():
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


def test_league_exception():
    with pytest.raises(Exception):
        league(
            year=2020,
            league_id=1234,
            cookies={}
        )


@mock.patch('src.fba_league.execute')
def test_league_runner_pass(mock_flow_response):
    mock_json = _resolve_relative_import('testData/flow_response_mock.json')

    mock_flow_response.return_value = MockFlowResponse(data=mock_json)

    result = league(
        year=2020,
        league_id=1234,
        cookies={}
    )

    assert isinstance(result, dict)


def _resolve_relative_import(test_file):
    in_file = os.path.join(os.path.dirname(__file__), test_file)
    with open(in_file) as f:
        raw_json = f.read()
        return json.loads(raw_json)
