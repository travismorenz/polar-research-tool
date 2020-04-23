from flask import Blueprint, render_template, redirect, url_for
from app.models import db, Article

site = Blueprint('site', __name__)

@site.route("/", methods=['GET'])
def intmain():
    articles = Article.query.order_by(Article.publish_date.desc()).paginate(1, 10, error_out=False)
    return render_template('main.html', articles=articles, tab='articles')

@site.route('/library', methods=['GET'])
def library():
    return redirect(url_for('site.intmain'))
