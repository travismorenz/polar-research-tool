from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import db, Person, Project, Keyphrase, Category
from flask_login import current_user, login_user, logout_user
from app.admins import admins
import os

projects = Blueprint('projects', __name__)

@projects.route("/api/add-keyphrase/<string:project_id>", methods=['POST'])
def add_keyphrase(project_id):
   keyphrase_name = request.get_json()['keyphrase']
   project = Project.query.filter_by(id=project_id).first()
   keyphrase = Keyphrase(name=keyphrase_name)
   if keyphrase not in project.keyphrases:
      project.keyphrases.append(keyphrase)
      db.session.add(project)
      db.session.commit()
   return {'keyphrases': [k.serialize() for k in project.keyphrases]}

@projects.route("/api/remove-keyphrase/<string:project_id>", methods=['POST'])
def remove_keyphrase(project_id):
   keyphrase_name = request.get_json()['keyphrase']
   project = Project.query.filter_by(id=project_id).first()
   keyphrase = Keyphrase.query.filter_by(name=keyphrase_name).first()
   if keyphrase in project.keyphrases:
      project.keyphrases.remove(keyphrase)
      db.session.add(project)
      db.session.commit()
   return {'keyphrases': [k.serialize() for k in project.keyphrases]}
