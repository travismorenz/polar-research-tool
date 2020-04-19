from celery import Celery
from celery.schedules import crontab
from flask import Flask, render_template, redirect, url_for
from app.models import db, Project
import os
from dotenv import load_dotenv

load_dotenv()
celery_app = Celery(__name__, broker='redis://redis:6379/0')
hours_minutes = os.getenv('UPDATE_TIME').split(':')
celery_app.conf.beat_schedule = {
    'update': {
        'task': 'tasks.update',
        'schedule': crontab(hour=int(hours_minutes[0]), minute=int(hours_minutes[1]))
    }
}

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    # Initialize database
    db.init_app(app)
    db.create_all(app=app)
    # Register the views 
    from app.views.site import site
    app.register_blueprint(site)
    return app
