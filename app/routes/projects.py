from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import db, Person, Project, Keyphrase, Category
from flask_login import current_user, login_user, logout_user
from app.admins import admins
import os

projects = Blueprint('projects', __name__)

@projects.route("/api/add-keyphrase/<string:project_id>", methods=['POST'])
def add_keyphrase(project_id):
   keyphrase = request.get_json()['keyphrase']
   project = Project.query.filter_by(id=project_id).first()
   keyphrase_obj = Keyphrase(name=keyphrase)
   project.keyphrases.append(keyphrase_obj)
   db.session.add(project)
   db.session.commit()
   print([k.serialize() for k in project.keyphrases])
   return {'keyphrases': [k.serialize() for k in project.keyphrases]}
