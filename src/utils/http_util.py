import logging

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


def request_status(status):
    """
    Check Request Status and raise exception where applicable
    :param status:
    :return:
    """
    if 500 <= status <= 503:
        logger.error(f"Exception: {status}")
        raise Exception(status)

    elif status == 401:
        logger.error(f"Exception: {status} - Access Denied")
        raise Exception(status)

    elif status == 404:
        logger.error(f"Exception: {status} - Invalid League")
        raise Exception(status)

    elif status != 200:
        logger.error(f"Exception: {status} - Unknown Error")

    else:
        logger.info(f"Status: {status}")
