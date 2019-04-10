"""
This script collects author stats (top 50 author listing ordered by number of citations), 
citation graph, 
paper stats (top 50 paper listing ordered by number of citations)
venue stats (All venues listed ordered by number of papers)
"""
from collections import defaultdict
from utils import Config
import numpy as np 
import pandas as pd 
import os
import pickle
scholarkeys = ['arxivId', 'authors', 'citationVelocity', 'citations', 'doi', 
'influentialCitationCount', 'paperId', 'references', 'title', 'topics', 'url', 'venue', 'year']

dbkeys = ['id', 'guidislink', 'link', 'updated', 'updated_parsed', 'published', 
'published_parsed', 'title', 'title_detail', 'summary', 'summary_detail', 'authors', 
'author_detail', 'author', 'links', 'arxiv_primary_category', 'tags', '_rawid', '_version']

db = pickle.load(open(Config.db_path, 'rb'))
venues = defaultdict(int)
authors = defaultdict(int)
papers = defaultdict(int)
am = pd.DataFrame(np.zeros(shape=(len(db),len(db))),
                  columns=list(db.keys()), index=list(db.keys()))
graphlist = {db[k]['title'].replace(',', ' '): [] for k in list(db.keys())}
for idx, (arxivid, art) in enumerate(db.items()):
    print(idx)
    if 'citations' in art:
        for cite in art['citations']:
            if cite['arxivId'] in am.index:
                graphlist[db[cite['arxivId']]['title'].replace(',', ' ')].append(art['title'].replace(',', ' '))
                am[cite['arxivId']][arxivid] = 1
        for cite in art['references']:
            if cite['arxivId'] in am.index:
                graphlist[art['title'].replace(',', ' ')].append(db[cite['arxivId']]['title'].replace(',', ' '))
                am[arxivid][cite['arxivId']] = 1
        for author in art['authors']:
            authors[author['name']] += len(art['citations'])
        papers[art['title']] = len(art['citations'])
        venues[art['venue']] += 1

with pd.option_context('display.max_colwidth', 100), pd.option_context('display.expand_frame_repr', True):
    papers = pd.DataFrame(sorted(list(papers.items()),key=lambda x: x[1], reverse=True), columns=['Title', 'Citations'])
    papers.to_html('templates/papers.html')
    authors = pd.DataFrame(sorted(list(authors.items()),key=lambda x: x[1], reverse=True), columns=['Author', 'Citations'])
    authors.to_html('templates/authors.html')
    venues = pd.DataFrame(sorted(list(venues.items()),key=lambda x: x[1], reverse=True), columns=['Venue', 'Publications'])
    venues.to_html('templates/venues.html')

cols = am.columns
bt = am.apply(lambda x: x > 0)
nodelist = bt.apply(lambda x: list(cols[x.values]), axis=1)
print(type(nodelist))
print(type(nodelist[0]))
print(nodelist[0])
with open('nodes.csv', 'w') as nodefile:
    lists = [[k] + v for k, v in graphlist.items()]
    lines = '\n'.join([','.join(t) for t in lists])
    # lines = '\n'.join([','.join([db[k]['title'].replace(',', ' ') for k in n]) for n in nodelist if len(n) > 0])
    nodefile.write(lines)
    print(lines)

os.system('cd templates; cat head_keyphrase.html authors.html papers.html tail_keyphrase.html > rankings.html')
os.system('cd templates; cat head_keyphrase.html venues.html tail_keyphrase.html > venue.html')


    



