import time

from celery import shared_task


import logging

logger = logging.getLogger(__name__)


@shared_task
def get_banking_data(username, password, code):
    from .utils import WSUNNAX

    try:
        ws = WSUNNAX(username, password)
        result = ws.read_data()
        if result == "OK":
            ws.save_data(code)
        else:
            logger.error(
                f"{result}, values username: {username} password: {password} code: {code}"
            )
            return False
    except Exception as e:
        logger.error(
            f"An error has occurred in the task get_banking_data {e}, values username: {username} password: {password} code: {code}"
        )
        return False
    logger.info(
        f"The task get_banking_d has finished successfully, values username: {username} password: {password} code: {code}"
    )
    return True
