import time

from celery import shared_task


@shared_task
def create_task(ws, bkd):
    ws.read_data()
    ws.save_data(bkd)
    return True
