import requests
import pickle
import json
import time
from utils import Config, safe_pickle_dump 
scholarkeys = ['arxivId', 'authors', 'citationVelocity', 'citations', 'doi', 
'influentialCitationCount', 'paperId', 'references', 'title', 'topics', 'url', 'venue', 'year']

dbkeys = ['id', 'guidislink', 'link', 'updated', 'updated_parsed', 'published', 
'published_parsed', 'title', 'title_detail', 'summary', 'summary_detail', 'authors', 
'author_detail', 'author', 'links', 'arxiv_primary_category', 'tags', '_rawid', '_version']

baseurl = 'http://api.semanticscholar.org/v1/paper/arXiv:'
e = 0
db = pickle.load(open(Config.db_path, 'rb'))
for idx, (arxid, art) in enumerate(db.items()):
    print(idx)
    if 'citationVelocity' in art:
        continue
    r = requests.get(baseurl + arxid).json()
    if 'error' in r:
        e +=1
        print(r['error'] + ': ' + str(e))
    else:
        art['citationVelocity'] = r['citationVelocity']
        art['citations'] = r['citations']
        art['references'] = r['references']
        art['influentialCitationCount'] = r['influentialCitationCount']
        art['topics'] = r['topics']
        art['venue'] = r['venue']
    time.sleep(1)

safe_pickle_dump(db, Config.db_path)