import pytest

from prefect import (
    Flow,
)

from src.fba_league import (
    url_generator,
    build,
    execute,
    league
)

from src.constants import FBA_ENDPOINT


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


def test_league():
    with pytest.raises(Exception):
        league(
            year=2020,
            league_id=1234,
            cookies={}
        )


def test_url_generator():
    test_year = 2020,
    test_league_id = 1234

    result = url_generator.run(
        year=test_year,
        league_id=test_league_id
    )

    assert result == f"{FBA_ENDPOINT}{test_year}/segments/0/leagues/{test_league_id}"
