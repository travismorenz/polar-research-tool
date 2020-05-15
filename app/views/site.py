from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models import db, Article, articles_categories, articles_keyphrases, projects_categories, projects_keyphrases, Project, projects_articles

site = Blueprint('site', __name__)

@site.route("/", methods=['GET'])
def intmain():
    articles = Article.query
    project = None
    if session.get('selected-project') and session['selected-project'] != "none":
        project = Project.query.filter_by(name=session['selected-project']).first()
        # Query all articles that share at least one keyphrase and category with the selected project
        cat_sq = db.session.query(articles_categories)\
            .join(projects_categories, (articles_categories.c.category_id == projects_categories.c.category_id) & (projects_categories.c.project_id == project.id))\
            .filter(articles_categories.c.article_id == Article.id)
        kp_sq = db.session.query(articles_keyphrases)\
            .join(projects_keyphrases, (articles_keyphrases.c.keyphrase_id == projects_keyphrases.c.keyphrase_id) & (projects_keyphrases.c.project_id == project.id))\
            .filter(articles_keyphrases.c.article_id == Article.id)
        articles = db.session.query(Article).filter(cat_sq.exists() & kp_sq.exists())
    articles = articles.order_by(Article.publish_date.desc())
    articles = articles.paginate(max_per_page=10, error_out=False)

    for article in articles.items:
        version = article.version
        if version > 1:
            version1 = Article.query.filter_by(version=1, title=article.title).first()
            if version1 is not None:
                article.version1 = version1
    return render_template('main.html', articles=articles, tab='articles', project=project)


@site.route('/library', methods=['GET'])
def library():
    if session.get('selected-project') == None or session['selected-project'] == None:
        return redirect(url_for('site.intmain'))
    project = Project.query.filter_by(name=session["selected-project"]).first()
    if project is not None:
        articles = project.articles.order_by(Article.publish_date.desc()).paginate(max_per_page=10, error_out=False)
        for article in articles.items:
            version = article.version
            if version > 1:
                version1 = Article.query.filter_by(version=1, title=article.title).first()
                if version1 is not None:
                    article.version1 = version1
    return render_template('main.html', articles=articles, tab='library', project=project)


@site.route('/toggle-in-library', methods=['POST'])
def toggle_in_library():
    res = {}
    id = request.form['id']
    if session.get('selected-project') and session['selected-project'] != "none":
        article = Article.query.filter_by(id=id).first()
        project = Project.query.filter_by(name=session['selected-project']).first()
        if article in project.articles:
            project.articles.remove(article)
        else:
            project.articles.append(article)
        db.session.add(project)
        db.session.commit()
    return res
    

@site.route('/select-project', methods=['POST'])
def select_project():
    session['selected-project'] = request.form['selection']
    return {}
