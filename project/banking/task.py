import time

from celery import shared_task


@shared_task
def create_task(username, password, code):
    from banking.api.views import WSUNNAX

    ws = WSUNNAX(username, password)
    ws.read_data()
    ws.save_data(code)
    return True
