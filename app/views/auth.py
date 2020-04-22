from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, Person
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
    print(person.projects)
    if person is None or not person.check_password(password):
        return render_template("login.html", error="Credentials are incorrect.")
    login_user(person, remember=True)
    return redirect(url_for('newmain'))


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
    return redirect(url_for("login_get"))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('intmain'))
