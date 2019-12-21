from src.auth import espn_authenticate


def test_espn_authenticate():
    uname='username'
    pword='password'

    result = espn_authenticate(user=uname, pwd=pword)

    assert result is None
