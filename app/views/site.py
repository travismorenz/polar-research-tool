from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models import db, Article, Author, articles_authors, articles_categories, articles_keyphrases, Category, Project, projects_articles, projects_categories, projects_keyphrases

site = Blueprint('site', __name__)

# TODO: 
# fix pagination
# fix count
# add search bar functionality (!! remember to sanitize input)

def build_search_query(project, terms):
    def like_statement(column_name):
        c = map(lambda t: f"{column_name} LIKE '%{t}%'", terms)
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

def build_filter_query(project_id):
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

@site.route("/", methods=['GET'])
def intmain():
    # Filter articles if project is selected
    filter_query = ""
    project = None
    if session.get('selected-project') and session['selected-project'] != "none":
        project = Project.query.filter_by(name=session['selected-project']).first()
        filter_query = build_filter_query(project.id)

    # Filter articles on search string
    search_string = "Martin Stetter,stat.ML"
    search_query = ""
    if search_string:
        terms = search_string.split(',')
        search_query = build_search_query(project, terms)

    # Main query including pagination functionality
    main_query = f"""
        SELECT *
            FROM article a
        {filter_query}
        {search_query}
        ORDER BY publish_date DESC
        LIMIT 50 OFFSET 0;
    """
    articles = Article.query.from_statement(db.text(main_query))
    if project:
        articles = articles.params(id=project.id)
    articles = articles.all()

    for article in articles:
        version = article.version
        if version > 1:
            version1 = Article.query.filter_by(version=1, title=article.title).first()
            if version1 is not None:
                article.version1 = version1
    return render_template('main.html', articles=articles, total=len(articles), tab='articles', project=project)


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
