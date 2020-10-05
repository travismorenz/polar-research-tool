import os

from app.admins import admins
from app.models import Category, Keyphrase, Person, Project, db
from flask import Blueprint, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login_post():
    if not current_user.is_authenticated:
        form_data = request.get_json()
        username = form_data['username']
        password = form_data['password']
        person = Person.query.filter_by(username=username).first()
        if person is None or not person.check_password(password):
            return {'error': 'Credentials are incorrect'}
        login_user(person, remember=True)
    projects = [project.serialize() for project in current_user.projects]
    return {'data': {'username': current_user.username, 'projects': projects, 'isAdmin': current_user.admin}}


@auth.route('/api/register', methods=['POST'])
def register_post():
    form_data = request.get_json()
    username = form_data['username']
    password = form_data['password']
    # Make sure user is unique
    person = Person.query.filter_by(username=username).first()
    if person is not None:
        return {'error': 'That name is taken'}
    # Create user in DB
    person = Person(username=username, admin=username in admins)
    person.set_password(password)
    db.session.add(person)
    db.session.commit()
    # Follow same precedure as /login
    login_user(person, remember=True)
    projects = [project.serialize() for project in current_user.projects]
    return {'data': {'username': current_user.username, 'projects': projects}}


@auth.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    return {}


@auth.route('/api/account', methods=['GET'])
def account():
    context = {}
    context['projects'] = []
    for p in current_user.projects:
        project = {'name': p.name}
        project['keyphrases'] = ', '.join(sorted(list(map(lambda x: x.name, p.keyphrases))))
        project['categories'] = ', '.join(sorted(list(map(lambda x: x.name, p.categories))))
        context['projects'].append(project)
    return render_template('account.html', **context)
