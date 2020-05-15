import urllib.request
import feedparser
from app import celery_app
import time
import datetime
from app.models import db, Project, Author, Category, Keyphrase, Article
from io import StringIO, BytesIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Helpers
def log(*msg):
    print(str(datetime.datetime.now())+":", *msg, file=open("./log_"+datetime.datetime.today().strftime('%Y-%m-%d'), "a"))

def get_content(links):
    """
    converts the pdf from an arxiv article link to text in memory
    """
    url = ''
    for x in links:
        if x['type'] == 'application/pdf':
            url = x['href']
    if url != '':
        pdf = urllib.request.urlopen(url).read()
        in_file = BytesIO(pdf)
        output_string = StringIO()
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        # sanitize NUL strings since postgres can't handle them
        return output_string.getvalue().replace('\x00','') 
    else:
        raise Exception('No pdf link found for article')

def map_to_strings(arr):
    return list(map(lambda x: x.name, arr))

def parse_arxiv_url(url):
    """
    examples is http://arxiv.org/abs/1512.08756v2
    we want to extract the raw id and the version
    """
    ix = url.rfind('/')
    idversion = url[ix + 1:]  # extract just the id (and the version)
    parts = idversion.split('v')
    assert len(parts) == 2, 'error parsing url ' + url
    return parts[0], int(parts[1])

def clean_entry(e):
    d = {}
    d['arxiv_id'], d['version'] = parse_arxiv_url(e['link'])
    d['publish_date'] = e['published']
    d['summary'] = e['summary']
    d['title'] = e['title']
    d['url'] = e['link']
    authors = list(map(lambda x: x.name, e['authors']))
    categories = list(filter(lambda x: '.' in x, list(map(lambda x: x.term, e['tags']))))
    return d, authors, categories 

@celery_app.task
def update():
    # Query size settings
    start_index = 0
    max_index = 10000
    results_per_iteration = 100

    # Only update articles for projects with both keyphrases and categories
    projects = list(filter(lambda x: x.keyphrases != [] and x.categories != [], Project.query.all()))
    for project in projects:
        keyphrase_strings = map_to_strings(project.keyphrases)
        category_strings = map_to_strings(project.categories)
        cat_string = '+OR+'.join(map(lambda x: 'cat:'+x, category_strings))
        # Loop through each project keyphrase, constructing a query using it and the categories
        for idx, kp in enumerate(keyphrase_strings):
            sq = 'all:"' + '+'.join(kp.split()) + '"+AND+' + cat_string
            log(idx)
            log('Searching arXiv for %s' % (sq,))
            for i in range(start_index, max_index, results_per_iteration):
                log("Results %i - %i" % (i, i + results_per_iteration))
                query = 'http://export.arxiv.org/api/query?search_query=%s&sortBy=lastUpdatedDate&start=%i&max_results=%i' % (sq, i, results_per_iteration)

                with urllib.request.urlopen(query) as url:
                    response = url.read()
                response = feedparser.parse(response).entries
                num_added = 0
                num_skipped = 0
                num_failed = 0
                for entry in response:
                    article_info, auths, cats = clean_entry(entry)
                    article = Article.query.filter_by(url=article_info['url']).first()
                    exists = False
                    # If article does not already exist, populate it
                    if article is None:
                        exists = True
                        # PDF parsing can fail, this will catch that
                        try:
                            article_info['content'] = get_content(entry['links'])
                        except Exception as e:
                            log('PARSING ERROR =>', e)
                            num_failed += 1
                            continue
                        article = Article(**article_info)
                        for a in auths:
                            author = Author.query.filter_by(name=a).first()
                            if author is None:
                                author = Author(name=a)
                            article.authors.append(author)
                        for c  in cats:
                            category = Category.query.filter_by(name=c).first()
                            if category is None:
                                category = Category(name=c)
                            article.categories.append(category)
                    # Keyphrases should be updated even on existing articles
                    keyphrase = Keyphrase.query.filter_by(name=kp).first()
                    if keyphrase not in article.keyphrases:
                        article.keyphrases.append(keyphrase)
                    db.session.add(article)
                    db.session.commit()
                    if exists:
                        num_added += 1
                    else:
                        num_skipped += 1
                # log some information
                log('Added %d papers, already had %d. %d failed to parse.' % (num_added, num_skipped, num_failed))

                if len(response) == 0:
                    log('Received no results from arxiv. Rate limiting? Exiting. Restart later maybe.')
                    break

                if num_added == 0 and False:
                    log('No new papers were added. Assuming no new papers exist. Exiting.')
                    break

                log('Sleeping for %i seconds\n' % (5,))
                time.sleep(5)
    log('Finished----')
