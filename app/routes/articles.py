import time
from functools import reduce
from app.models import (Article, Author, Category, Project, articles_authors,
                        articles_categories, articles_keyphrases, db,
                        projects_articles, projects_categories,
                        projects_keyphrases)
from flask import Blueprint, request, session, url_for
from flask_login import login_required

articles = Blueprint('articles', __name__)

LIMIT = 50 # num of articles per page

def format_articles(query_result):
    articles = {}
    for row in query_result:
        row = dict(row)
        row_id = row['id']
        author_name = row['author_name']
        category_name = row['category_name']
        if row_id not in articles:
            articles[row_id] = row
            row['authors'] = [author_name]
            row['categories'] = [category_name]
        if author_name not in articles[row_id]['authors']:
            articles[row_id]['authors'].append(author_name)
        if category_name not in articles[row_id]['categories']:
            articles[row_id]['categories'].append(category_name)
    
    return list(articles.values())


def get_articles_by_id(ids):
    query = f"""
        SELECT a.id, a.title, a.summary, a.url, a.version, a.publish_date, c.name as category_name, au.name as author_name
        FROM article a
        JOIN articles_categories ac ON ac.article_id = a.id
        JOIN category c ON c.id = ac.category_id
        JOIN articles_authors aa ON aa.article_id = a.id
        JOIN author au ON au.id = aa.author_id
        WHERE a.id IN :ids
    """
    query_result = db.engine.execute(db.text(query), ids=ids)
    articles = format_articles(query_result)
    return articles

feed_filter = """
    WHERE EXISTS (
        SELECT * FROM articles_categories ac 
        JOIN projects_categories pc
            ON pc.category_id = ac.category_id AND pc.project_id = :project_id
        WHERE ac.article_id = a.id
    )
    AND EXISTS (
        SELECT * FROM articles_keyphrases ak 
        JOIN projects_keyphrases pk
            ON pk.keyphrase_id = ak.keyphrase_id AND pk.project_id = :project_id 
        WHERE ak.article_id = a.id
    )
    AND NOT EXISTS (
        SELECT article_id, project_id
        FROM projects_articles
        WHERE article_id = a.id AND project_id = :project_id
    )
"""

def build_library_filter(tab):
    trash = 'false' if tab == 'library' else 'true'
    return f"""
        WHERE EXISTS
            (
                SELECT article_id, project_id, trash
                FROM projects_articles
                WHERE article_id = a.id AND project_id = :project_id AND trash = {trash}
            ) 
    """

@articles.route('/api/articles/', defaults={'project_id': ""})
@articles.route('/api/articles/<string:project_id>')
def get_articles(project_id):
    # Pull limit and offset from search params
    page = int(request.args.get('page'))
    tab = request.args.get('tab')
    query_params = {
        'offset': page * LIMIT,
        'limit': LIMIT
    }
    
    # Filter articles by their project
    filter_query = ""
    if project_id:
        filter_query = feed_filter if tab == "feed" else build_library_filter(tab)
        query_params['project_id'] = project_id

    # Get relevant article ids from the DB
    main_query = f"""
        SELECT a.id
        FROM article a
        {filter_query}
        ORDER BY a.publish_date DESC
        LIMIT :limit OFFSET :offset
    """
    count_query = f"""
        SELECT COUNT(*)
        FROM article a
        {filter_query}
    """
    main_query_result = db.engine.execute(db.text(main_query), **query_params).fetchall()
    count_query_result = db.engine.execute(db.text(count_query), **query_params).fetchall()
    article_ids = [row['id'] for row in main_query_result] + [-1]
    count = count_query_result[0][0]

    # Get the articles corresponding to those ids
    articles = get_articles_by_id(tuple(article_ids))
    return {'articles': articles, 'count': count}

def build_trash_query(value):
    return f"""
        UPDATE projects_articles
        SET trash = {value}
        WHERE project_id = :project_id AND article_id = :article_id
    """

@articles.route("/api/change-article-tab/<string:project_id>", methods=["POST"])
def toggle_in_library(project_id):
    article_id = request.get_json()['articleId']
    target_tab = request.get_json()['targetTab']

    article = Article.query.filter_by(id=article_id).first()
    project = Project.query.filter_by(id=project_id).first()

    # TODO: Find a better (actually working) solution to the problem of handling many fast updates
    tries = 0
    while tries < 10:
        try:
            if target_tab == "feed":
                project.articles.remove(article)
                db.session.add(project)
                db.session.commit()

            if target_tab == "library" or target_tab == "trash":
                if article not in project.articles:
                    project.articles.append(article)
                    db.session.add(project)
                    db.session.commit()
                trash = 'true' if target_tab == "trash" else "false"
                db.engine.execute(db.text(build_trash_query(trash)), project_id=project_id, article_id=article_id)

            break
        except Exception as e:
            print(e)
            print('error')
            tries += 1
    return {}
