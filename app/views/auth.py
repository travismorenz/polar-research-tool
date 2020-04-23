from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, Person, Project, Keyphrase, Category
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('newmain'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    if not username or not username.strip():
        return render_template("login.html", error="Username is missing.")
    if not password:
        return render_template("login.html", error="Password is missing.")
    person = Person.query.filter_by(username=username).first()
    if person is None or not person.check_password(password):
        return render_template("login.html", error="Credentials are incorrect.")
    login_user(person, remember=True)
    return redirect(url_for('site.intmain'))


@auth.route('/register', methods=['GET'])
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for('newmain'))
    return render_template('register.html')
        

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
    person = Person(username=username)
    person.set_password(password)
    db.session.add(person)
    db.session.commit()
    flash("User successfully created!")
    return redirect(url_for("auth.login_get"))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.intmain'))

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


def parse_project_names(form):
    projects = []
    for key in form:
        if key != 'edit-projects':
            name = key.split('-')[1]
            if name not in projects:
                projects.append(name)
    return projects


def clean_up_input(arr):
    return [x.strip() for x in set(filter(lambda x: x != '', arr))]

@auth.route('/account', methods=['GET', 'POST'])
def account():
    def get_context():
        context = {}
        context['projects'] = []
        p = Project()
        for p in current_user.projects:
            project = {'name': p.name}
            if hasattr(p, 'keyphrases'):
                project['keyphrases'] = ', '.join(sorted(list(map(lambda x: x.name, p.keyphrases))))
            if hasattr(p, 'categories'):
                project['categories'] = ', '.join(sorted(list(map(lambda x: x.name, p.categories))))
            context['projects'].append(project)
        return context
    context = get_context()
    if request.method == "POST":
        # Project leaving
        left = False
        if 'leave-project' in request.form:
            name = request.form['leave-project']
            project = Project.query.filter_by(name=name).first()
            current_user.projects.remove(project)
            db.session.add(current_user)
            db.session.commit()
            left = True
        # Project editing
        if 'edit-projects' in request.form and not left:
            names = parse_project_names(request.form)
            requires_update = set()
            for name in names:
                changes = False
                project = Project.query.filter_by(name=name).first()
                new_name = request.form['name-'+name].strip()
                new_keyphrases = clean_up_input(request.form['keyphrases-'+name].split(', '))
                new_categories = clean_up_input(request.form['categories-'+name].split(', '))
                # Update name
                if new_name == "":
                    context['projects_error'] = name+": new name can't be empty"
                    return render_template('account.html', **context)
                if project.name != new_name:
                    check_name = Project.query.filter_by(name=new_name).first()
                    if check_name is not None:
                        context['projects_error'] = name+": project with that name already exists"
                        return render_template('account.html', **context)
                    project.name = new_name
                    changes = True
                # Update keyphrases
                if hasattr(project, 'keyphrases'):
                    old_keyphrases = list(map(lambda x: x.name, project.keyphrases))
                    if set(new_keyphrases) != set(old_keyphrases):
                        changes = True
                        requires_update.add(name)
                        project.keyphrases = []
                        for name in new_keyphrases:
                            keyphrase = Keyphrase.query.filter_by(name=name).first()
                            if keyphrase is None:
                                keyphrase = Keyphrase(name=name)
                            project.keyphrases.append(keyphrase)
                # Update categories
                if hasattr(project, 'categories'):
                    old_categories = list(map(lambda x: x.name, project.categories))
                    if set(new_categories) != set(old_categories):
                        changes = True
                        requires_update.add(name)
                        project.categories = []
                        for name in new_categories:
                            category = Category.query.filter_by(name=name).first()
                            if category is None:
                                category = Category(name=name)
                            project.categories.append(category)
                if changes:
                    db.session.add(project)
                    db.session.commit()
            if len(requires_update) != 0:
                print('UPDATE', requires_update)
    # update projects in case they have changed
    context = get_context()
    return render_template('account.html', **context)
