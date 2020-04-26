from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models import db, Article, articles_categories, articles_keyphrases, projects_categories, projects_keyphrases, Project

site = Blueprint('site', __name__)

@site.route("/", methods=['GET'])
def intmain():
    articles = Article.query
    if session.get('selected-project') and session['selected-project'] != "none":
        project = Project.query.filter_by(name=session['selected-project']).first()
        articles = db.session.query(Article).distinct()\
            .join(articles_categories)\
            .join(articles_keyphrases)\
            .join(projects_categories, (projects_categories.c.category_id == articles_categories.c.category_id) & (projects_categories.c.project_id == project.id))\
            .join(projects_keyphrases, (projects_keyphrases.c.keyphrase_id == articles_keyphrases.c.keyphrase_id) & (projects_keyphrases.c.project_id == project.id))
    articles = articles.order_by(Article.publish_date.desc())
    articles = articles.paginate(max_per_page=10, error_out=False)

    for article in articles.items:
        version = article.version
        if version > 1:
            version1 = Article.query.filter_by(version=1, title=article.title).first()
            if version1 is not None:
                article.version1 = version1
    return render_template('main.html', articles=articles, tab='articles')


@site.route('/library', methods=['GET'])
def library():
    return redirect(url_for('site.intmain'))


@site.route('/select-project', methods=['POST'])
def select_project():
    session['selected-project'] = request.form['selection']
    return {}
