import logging
import requests

from .constants import URL_API_KEY, URL_LOGIN

logging.basicConfig(level="DEBUG")
AUTH_LOGGER = logging.getLogger(__name__)


def espn_authenticate(user: str, pwd: str):  # pragma no cover
    """
    Make request to get ESPN API Key
    Args:
        user: (str) - user to authenticate
        pwd: (str) - password to authenticate
    Returns:
        (dict) - API Key
    """
    headers = {"Content-Type": "application/json"}
    response = requests.post(URL_API_KEY, headers=headers)

    if response.status_code != 200 or "api-key" not in response.headers:
        AUTH_LOGGER.debug("Unable to access API-Key")
        AUTH_LOGGER.debug("Retry the authentication")

        return None

    api_key = response.headers["api-key"]

    # Utilize API-Key and login information to get the swid and s2 keys
    headers["authorization"] = f"APIKEY {api_key}"
    payload = {"loginValue": user, "password": pwd}
    response = requests.post(URL_LOGIN, headers=headers, json=payload)

    if response.status_code != 200:
        AUTH_LOGGER.debug("Authentication unsuccessful - check credentials")
        AUTH_LOGGER.debug("Retry the authentication")
        return None

    data = response.json()

    if data["error"] is not None:
        AUTH_LOGGER.debug("Authentication unsuccessful - error: %s", data["error"])
        AUTH_LOGGER.debug("Retry the authentication")
        return None

    return {"espn_s2": data["data"]["s2"], "swid": data["data"]["profile"]["swid"]}
