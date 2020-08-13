from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import db, Person, Project, Keyphrase, Category
from flask_login import current_user, login_user, logout_user
from app.admins import admins
import os

test = Blueprint('test', __name__, static_folder='../static', static_url_path='/test/static')

@test.route('/')
def main():
    return test.send_static_file('index.html')
