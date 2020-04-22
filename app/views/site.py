from flask import Blueprint, render_template, redirect, url_for
from app.models import db

site = Blueprint('site', __name__)

@site.route("/")
def intmain():
    return render_template('newmain.html')


