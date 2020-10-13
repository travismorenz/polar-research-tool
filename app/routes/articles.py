from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_required
from functools import reduce
from app.models import db, Article, Author, articles_authors, articles_categories, articles_keyphrases, Category, Project, projects_articles, projects_categories, projects_keyphrases
import time

articles = Blueprint('articles', __name__)

LIMIT = 50 # num of articles per page
FILTER_QUERY = """
    WHERE EXISTS (
        SELECT * FROM articles_categories ac 
        JOIN projects_categories pc
            ON pc.category_id = ac.category_id AND pc.project_id = :id
        WHERE ac.article_id = a.id
    )
    AND EXISTS (
        SELECT * FROM articles_keyphrases ak 
        JOIN projects_keyphrases pk
            ON pk.keyphrase_id = ak.keyphrase_id AND pk.project_id = :id 
        WHERE ak.article_id = a.id
    )
"""


def set_pagination_info(articles, page):
    total = articles['total']
    curr_amount = len(articles['items'])
    articles['has_next'] = total > LIMIT * page + curr_amount
    articles['has_prev'] = page > 0
    articles['next_page'] = page + 1
    articles['prev_page'] = page - 1


def set_previous_versions(articles):
    for article in articles['items']:
        version = article.version
        if version > 1:
            version1 = Article.query.filter_by(version=1, title=article.title).first()
            if version1 is not None:
                article.version1 = version1


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
    return articles


def articles_query(ids):
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

@articles.route('/api/articles/', defaults={'project_id': ""})
@articles.route('/api/articles/<string:project_id>')
def get_articles(project_id):
    # Pull limit and offset from search params
    page = int(request.args.get('page')) or 0
    limit = request.args.get('limit') or LIMIT
    query_params = {
        'offset': page * limit,
        'limit': limit
    }
    
    # Filter articles by their project
    filter_query = ""
    if project_id:
        filter_query = FILTER_QUERY
        query_params['id'] = project_id

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
    article_ids = tuple([row['id'] for row in main_query_result])
    count = count_query_result[0][0]

    # Get the articles corresponding to those ids
    articles = articles_query(article_ids)
    return {'articles': articles, 'count': count}


@articles.route("/api/article-ids/", defaults={'project_id': ""})
@articles.route("/api/article-ids/<string:project_id>")
def get_article_ids(project_id):
    # Filter articles if project is selected
    query_params = {}
    filter_query = ""
    if project_id:
        filter_query = FILTER_QUERY
        query_params['id'] = project_id
    # Construct queries
    main_query = f"""
        SELECT a.id
        FROM article a
        {filter_query}
        ORDER BY a.publish_date DESC
    """
    # Populate articles and fill out article authors and categories
    main_query_result = db.engine.execute(db.text(main_query), **query_params).fetchall()
    article_ids = [row['id'] for row in main_query_result]
    return {'ids': article_ids}


@articles.route("/api/articles-by-library/<string:project_id>")
def get_articles_by_library(project_id):
    main_query = f"""
        SELECT a.id
        FROM project p
        JOIN projects_articles pa ON pa.project_id = p.id
        JOIN article a ON a.id = pa.article_id
        WHERE p.id = :id AND trash = false
    """
    # Populate articles with our query results
    main_query_result = db.engine.execute(db.text(main_query), id=project_id).fetchall()
    article_ids = [row['id'] for row in main_query_result]
    return {'ids': article_ids}


@articles.route("/api/toggle-in-library/<string:project_id>", methods=["POST"])
def toggle_in_library(project_id):
   article_id = request.get_json()['articleId']
   article = Article.query.filter_by(id=article_id).first()
   project = Project.query.filter_by(id=project_id).first()

   if article in project.articles:
       project.articles.remove(article)
   else:
        project.articles.append(article)
   db.session.add(project)
   db.session.commit()
   return {}
