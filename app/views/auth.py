from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import db, Person, Project, Keyphrase, Category
from flask_login import current_user, login_user, logout_user
from app.admins import admins
import os

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    if not current_user.is_authenticated:
        form_data = request.get_json()
        username = form_data['username']
        password = form_data['password']
        if not username or not username.strip():
            return {'error': 'Username is missing.'}
        if not password:
            return {'error': 'Password is missing'}
        person = Person.query.filter_by(username=username).first()
        if person is None or not person.check_password(password):
            return {'error': 'Credentials are incorrect'}
        login_user(person, remember=True)
    projects = [project.serialize() for project in current_user.projects]
    return {'data': {'username': current_user.username, 'projects': projects}}

@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    # Input validation
    if not username or not username.strip():
        return render_template("register.html", error="Username is missing.")
    if not password:
        return render_template("register.html", error="Password is missing.")
    if len(password) < 7:
        return render_template("register.html", error="Password must be at least 7 characters.")
    if len(password) > 50:
        return render_template("register.html", error="Password may be a maximum of 50 characters.")
    if len(username) > 50:
        return render_template("register.html", error="Username may be a maximum of 50 characters.")

    person = Person.query.filter_by(username=username).first()
    if person is not None:
        return render_template("register.html", error="User already exists.")
    person = Person(username=username, admin=username in admins)
    person.set_password(password)
    db.session.add(person)
    db.session.commit()
    flash("User successfully created!")
    return redirect(url_for("auth.login_get"))


@auth.route('/logout', methods=['POST'])
def logout():
    session.clear();
    logout_user()
    return {}


@auth.route('/account', methods=['GET'])
def account():
    context = {}
    context['projects'] = []
    for p in current_user.projects:
        project = {'name': p.name}
        project['keyphrases'] = ', '.join(sorted(list(map(lambda x: x.name, p.keyphrases))))
        project['categories'] = ', '.join(sorted(list(map(lambda x: x.name, p.categories))))
        context['projects'].append(project)
    return render_template('account.html', **context)


#####
#  All project endpoints will be moved into their own view file at some point
#####
@auth.route('/create-project', methods=['POST'])
def create_project():
    res = {'selector': '#create-project-error'}
    name = request.form['name'].strip()
    if name == "":
        res['error'] = 'Missing'
        return res, 400
    project = Project.query.filter_by(name=name).first()
    if project is not None:
        res['error'] = "That project already exists"
        return res, 400
    project = Project(name=name)
    current_user.projects.append(project)
    db.session.add(current_user)
    db.session.commit()
    return res


@auth.route('/delete-project', methods=['POST'])
def delete_project():
    res = {}
    name = request.form['name']
    project = Project.query.filter_by(name=name).first()
    db.session.delete(project)
    db.session.commit()
    return res


@auth.route('/join-project', methods=['POST'])
def join_project():
    res = {'selector': '#join-project-error'}
    name = request.form['name'].strip()
    if name == "":
        res['error'] = 'Missing'
        return res, 400
    project = Project.query.filter_by(name=name).first()
    if project is None:
        res['error'] = "That project does not exist"
        return res, 400
    current_user.projects.append(project)
    db.session.add(current_user)
    db.session.commit()
    return res


# By convention, this should be DELETE. jQuery only has built in post tho, so I'm going to be lazy and leave it
@auth.route('/leave-project', methods=['POST'])
def leave_project():
    res = {}
    name = request.form['name']
    project = Project.query.filter_by(name=name).first()
    current_user.projects.remove(project)
    db.session.add(current_user)
    db.session.commit()
    return res


# Utility function for save-projects
def clean_input(input):
    input = input.split(',')
    return sorted([x.strip() for x in set(filter(lambda x: x != '', input))])

@auth.route('/save-projects', methods={'POST'})
def save_projects():
    res = {}
    projects = request.get_json(force=True)
    for curr_name in projects:
        new_name = projects[curr_name]['name'].strip()
        new_keyphrases = clean_input(projects[curr_name]['keyphrases'])
        new_categories = clean_input(projects[curr_name]['categories'])

        changes = False
        name_change = False
        project = Project.query.filter_by(name=curr_name).first()
        curr_keyphrases = sorted(list(map(lambda x: x.name, project.keyphrases)))
        curr_categories = sorted(list(map(lambda x: x.name, project.categories)))
        if curr_name != new_name:
            changes = True
            name_change = True
            project.name = new_name
        if curr_keyphrases != new_keyphrases:
            changes = True
            project.keyphrases = []
            for kp in new_keyphrases:
                keyphrase = Keyphrase.query.filter_by(name=kp).first()
                if keyphrase is None:
                    keyphrase = Keyphrase(name=kp)
                project.keyphrases.append(keyphrase)
        if curr_categories != new_categories:
            changes = True
            project.categories = []
            for c in new_categories:
                # TODO: validate categories here
                category = Category.query.filter_by(name=c).first()
                if category is None:
                    category = Category(name=c)
                project.categories.append(category)
        if changes:
            db.session.add(project)
            db.session.commit()
            res['msg'] = 'Saved. Next update is scheduled for ' + os.getenv('UPDATE_TIME')
            if name_change:
                res['nameChange'] = True
    return res


def parse_project_names(form):
    projects = []
    for key in form:
        if key != 'edit-projects':
            name = key.split('-')[1]
            if name not in projects:
                projects.append(name)
    return projects
