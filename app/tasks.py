import time
from app import celery_app
from app.models import Project, db

@celery_app.task
def create_project_task(name='create_project_task'):
    time.sleep(20)
    p = Project(name='yuhyeet')
    db.session.add(p)
    db.session.commit()

@celery_app.task
def update(name='update'):
    pass
