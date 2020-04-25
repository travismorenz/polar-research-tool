from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

persons_projects = db.Table('persons_projects', 
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True))


persons_articles = db.Table('persons_articles', 
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True))


articles_categories = db.Table('articles_categories',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True))


articles_keyphrases = db.Table('articles_keyphrases',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('keyphrase_id', db.Integer, db.ForeignKey('keyphrase.id'), primary_key=True))

articles_authors = db.Table('articles_authors',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True))

projects_keyphrases = db.Table('projects_keyphrases',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('keyphrase_id', db.Integer, db.ForeignKey('keyphrase.id'), primary_key=True))

projects_categories = db.Table('projects_categories',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True))

class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text,unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    projects = db.relationship('Project', secondary=persons_projects, back_populates='persons')
    library = db.relationship('Article', secondary=persons_articles, back_populates='persons')
    comments = db.relationship('Comment', back_populates='persons')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    persons = db.relationship('Person', secondary=persons_projects, back_populates='projects')
    keyphrases = db.relationship('Keyphrase', secondary=projects_keyphrases, back_populates='projects')
    categories = db.relationship('Category', secondary=projects_categories, back_populates="projects")


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arxiv_id = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, unique=True, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=True) # This might be nullable=False, not sure yet
    # TODO: Analysis result fields will probably go here

    persons = db.relationship('Person', secondary=persons_articles, back_populates='library')
    comments = db.relationship('Comment', back_populates='articles')
    categories = db.relationship('Category', secondary=articles_categories, back_populates="articles")
    keyphrases = db.relationship('Keyphrase', secondary=articles_keyphrases, back_populates="articles")
    authors = db.relationship('Author', secondary=articles_authors, back_populates="articles")

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    articles = db.relationship('Article', secondary=articles_authors, back_populates="authors")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    persons = db.relationship('Person', back_populates='comments')
    articles = db.relationship('Article', back_populates='comments')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    articles = db.relationship('Article', secondary=articles_categories, back_populates="categories")
    projects = db.relationship('Project', secondary=projects_categories, back_populates="categories")


class Keyphrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    articles = db.relationship('Article', secondary=articles_keyphrases, back_populates="keyphrases")
    projects = db.relationship('Project', secondary=projects_keyphrases, back_populates="keyphrases")

