import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
from flask import Flask, url_for
from flask_cors import CORS
from flask_login import LoginManager

from app.models import Person, db

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
    app = Flask(__name__, static_url_path="/")
    CORS(app, supports_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.secret_key = os.getenv('SECRET_KEY')
    # Initialize database
    db.init_app(app)
    db.create_all(app=app)
    # Initialize login manager
    login.init_app(app)
    # Register the views 
    from app.routes.articles import articles
    from app.routes.auth import auth
    from app.routes.projects import projects
    app.register_blueprint(articles)
    app.register_blueprint(auth)
    app.register_blueprint(projects)
    return app
