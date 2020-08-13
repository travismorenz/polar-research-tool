from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import db, Person, Project, Keyphrase, Category
from flask_login import current_user, login_user, logout_user
from app.admins import admins
import os

main = Blueprint('main', __name__, static_folder='../static', static_url_path='/main/static')

@main.route('/login')
@main.route('/register')
@main.route('/account')
@main.route('/library')
@main.route('/')
def get_main():
    return main.send_static_file('index.html')
