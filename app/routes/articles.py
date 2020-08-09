from flask import Blueprint, render_template, redirect, url_for, request, session
from functools import reduce
from app.models import db, Article, Author, articles_authors, articles_categories, articles_keyphrases, Category, Project, projects_articles, projects_categories, projects_keyphrases
import time

articles = Blueprint('articles', __name__)
LIMIT = 50 # num of articles per page

# TODO: 
# fulltext instead of LIKE

# This is a horrific bit of code. I couldn't find a proper point of reference for doing stuff
# like this but as soon as I do, I will wipe this garbage off the face of the planet.
def build_search_query(project, param_keys):
    def like_statement(column_name):
        c = map(lambda key: f"LOWER({column_name}) LIKE LOWER(:{key})", param_keys)
        return ' OR '.join(c)
    operator = 'AND' if project else 'WHERE'
    query = f"""
        {operator} (
				EXISTS (
					SELECT * from articles_authors aa
					JOIN author
						ON author.id = aa.author_id
					WHERE aa.article_id = a.id
					AND ({like_statement('author.name')})
				)
				OR EXISTS (
					SELECT * from articles_keyphrases ak
					JOIN keyphrase
						ON keyphrase.id = ak.keyphrase_id
					WHERE ak.article_id = a.id
					AND ({like_statement('keyphrase.name')})
				)
                OR EXISTS (
					SELECT * from articles_categories ac
					JOIN category
						ON category.id = ac.category_id
					WHERE ac.article_id = a.id
					AND ({like_statement('category.name')})
				)
                OR ({like_statement('a.title')})
        	)
        """
    return query

def get_filter_query(project_id):
    return """
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

def build_search_query_params(terms):
    params = {}
    for i in range(len(terms)):
        term = terms[i]
        params[f'term{str(i)}'] = f'%{term}%'
    return params


@articles.route("/api/articles/", defaults={'project_id': None})
@articles.route("/api/articles/<string:project_id>")
def articles_get(project_id):
    # Query params
    page = int(request.args.get('page')) if request.args.get('page') else 0
    search_string = request.args.get('search') if request.args.get('search') else ''

    query_params = {'limit': LIMIT, 'offset': page * LIMIT}

    # Filter articles if project is selected
    filter_query = ""
    project = project_id
    if project:
        project = Project.query.filter_by().first()
        filter_query = get_filter_query(project.id)
        query_params['id'] = project.id

    # Filter articles on search string
    search_query = ""
    search_query_params = None
    if search_string:
        terms = list(filter(lambda x: x, search_string.split(' '))) # split search string on space, remove empty strings
        search_query_params = build_search_query_params(terms)
        search_query = build_search_query(project, search_query_params.keys())
        query_params.update(search_query_params)

    # Construct queries
    main_query = f"""
        SELECT a.id, a.title, a.summary, a.url, a.version, a.publish_date, c.name as category_name, au.name as author_name
        FROM category c
        JOIN articles_categories ac ON ac.category_id = c.id
        JOIN (
            SELECT a.id, a.title, a.summary, a.url, a.version, a.publish_date
            FROM   article a
        {filter_query}
        {search_query}
        ORDER BY a.publish_date DESC
        LIMIT :limit OFFSET :offset) a
        ON a.id = ac.article_id
        JOIN articles_authors aa ON aa.article_id = a.id
        JOIN author au ON au.id = aa.author_id
    """
    count_query = f"""
        SELECT COUNT(*)
            FROM article a
        {filter_query}
        {search_query};
    """

    # Populate articles and fill out article authors and categories
    articles = {}
    count_query_result = db.engine.execute(db.text(count_query), **query_params).fetchall()
    count = dict(count_query_result[0])['count']
    main_query_result = db.engine.execute(db.text(main_query), **query_params).fetchall()
    for row in main_query_result:
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
    return {'articles': articles, 'count': count}

@articles.route('/library', methods=['GET'])
def library():
    if session.get('selected-project') == None or session['selected-project'] == None:
        return redirect(url_for('articles.intmain'))
    page = int(request.args.get('page')) if request.args.get('page') else 0
    project = Project.query.filter_by(name=session["selected-project"]).first()

    # Populate articles with our query results
    articles = {}
    articles['items'] = project.articles.order_by(Article.publish_date.desc()).limit(LIMIT).offset(page * LIMIT).all()
    articles['total'] = project.articles.count()

    # Add additional metadata to articles for display
    set_pagination_info(articles, page)
    set_previous_versions(articles)
    return render_template('main.html', articles=articles, tab='library', project=project)