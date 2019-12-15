import mock
import pytest

from prefect import (
    Flow,
)

from src.fba_players import (
    build,
    execute,
    players
)


def test_flow_build():
    test_flow = build(
        year=2020,
        league_id=1234,
        cookies={}
    )

    assert isinstance(test_flow, Flow)


def test_execute_flow():
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


@mock.patch('src.fba_players.execute')
def test_league_pass(mock_execute):
    mock_execute.return_value = True

    result = players(
        year=2020,
        league_id=1234,
        cookies={}
    )

    assert result is True


def test_league_raises():
    with pytest.raises(Exception):
        players(
            year=2020,
            league_id=1234,
            cookies={}
        )
