from flask import Blueprint, render_template, redirect, url_for
from app.models import db, Project
from app.tasks import create_project_task

site = Blueprint('site', __name__)

@site.route('/')
def index():
    projects = Project.query.all()
    return  render_template('index.html', projects=projects)


@site.route('/create-project', methods=['POST'])
def create_project():
    create_project_task.delay()
    return redirect(url_for('site.index'))
