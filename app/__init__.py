from celery import Celery
from celery.schedules import crontab
from flask_login import LoginManager
from flask import Flask, render_template, redirect, url_for
from app.models import db, Person
import os
from dotenv import load_dotenv

load_dotenv()

# Celery Setup (The import is janky, can probably be cleaned up)
celery_app = Celery(__name__, broker='redis://redis:6379/0')
hours_minutes = os.getenv('UPDATE_TIME').split(':')
celery_app.conf.beat_schedule = {
    'update': {
        'task': 'app.tasks.update',
        'schedule': crontab(hour=int(hours_minutes[0]), minute=int(hours_minutes[1]))
    }
}
celery_app.conf.timezone = os.getenv('UPDATE_TIMEZONE')
import app.tasks

login = LoginManager()
@login.user_loader
def load_user(username):
    return Person.query.get(username)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.secret_key = os.getenv('SECRET_KEY')
    # Initialize database
    db.init_app(app)
    db.create_all(app=app)
    # Initialize login manager
    login.init_app(app)
    # Register the views 
    from app.views.site import site
    from app.views.auth import auth
    app.register_blueprint(site)
    app.register_blueprint(auth)
    return app