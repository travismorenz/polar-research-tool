from flask import Blueprint, render_template, redirect, url_for, request, session
from functools import reduce
from app.models import db, Article, Author, articles_authors, articles_categories, articles_keyphrases, Category, Project, projects_articles, projects_categories, projects_keyphrases

site = Blueprint('site', __name__)
LIMIT = 20 # num of articles per page

# TODO: 
# add search bar functionality (!! remember to use prepared statements)
# fulltext instead of LIKE

def build_search_query(project, terms):
    def like_statement(column_name):
        c = map(lambda x: f"LOWER({column_name}) LIKE LOWER(:term_{x})", terms)
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

def params_reduce_helper(a, b):
    a['term_'+b] = f"%{b}%"
    return a


@site.route("/", methods=['GET'])
def intmain():
    page = int(request.args.get('page')) if request.args.get('page') else 0

    # Filter articles if project is selected
    filter_query = ""
    project = None
    if session.get('selected-project') and session['selected-project'] != "none":
        project = Project.query.filter_by(name=session['selected-project']).first()
        filter_query = get_filter_query(project.id)

    # Filter articles on search string
    search_string = ""
    search_query = ""
    search_params = None
    if search_string:
        terms = list(filter(lambda x: x, search_string.split(' '))) # split search string on space, remove empty strings
        search_query = build_search_query(project, terms)
        search_params = reduce(params_reduce_helper, terms, {}) # convert to dict of sql params

    # Construct queries
    main_query = f"""
        SELECT *
            FROM article a
        {filter_query}
        {search_query}
        ORDER BY publish_date DESC
        LIMIT :limit
        OFFSET :offset;
    """
    count_query = f"""
        SELECT COUNT(*)
            FROM article a
        {filter_query}
        {search_query};
    """
    # Populate articles dict with query results and metadata
    articles = {}
    query_params = {'limit': LIMIT, 'offset': page * LIMIT}
    if project:
        query_params['id'] = project.id
    if search_params:
        query_params.update(search_params)
    articles['items'] = Article.query.from_statement(db.text(main_query)).params(**query_params).all()
    articles['total'] = db.engine.execute(db.text(count_query), **query_params).fetchall()[0]['count']
    set_pagination_info(articles, page)
    set_previous_versions(articles)

    return render_template('main.html', articles=articles, tab='articles', project=project)


@site.route('/library', methods=['GET'])
def library():
    if session.get('selected-project') == None or session['selected-project'] == None:
        return redirect(url_for('site.intmain'))
    page = int(request.args.get('page')) if request.args.get('page') else 0
    project = Project.query.filter_by(name=session["selected-project"]).first()

    articles = {}
    articles['items'] = project.articles.order_by(Article.publish_date.desc()).limit(LIMIT).offset(page * LIMIT).all()
    articles['total'] = project.articles.count()
    set_pagination_info(articles, page)
    set_previous_versions(articles)
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
