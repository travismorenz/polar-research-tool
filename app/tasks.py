import time
from app import celery_app


@celery_app.task
def update():
    print('UPDATE IS COMMENCING')
