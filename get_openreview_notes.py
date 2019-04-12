from __future__ import print_function
import openreview
import pickle

c = openreview.Client(baseurl='https://openreview.net', username='aaron.tuor@pnnl.gov',
                      password='!trex1000')
notes2019 = c.get_notes(invitation='ICLR.cc/2019/Conference/-/Blind_Submission')
notes2018 = c.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
notesGamesec = c.get_notes(invitation='gamesec-conf.org/GameSec/2019/Conference/-/Submission')
notesamlsearch = c.search_notes('adversarial machine learning')
pickle.dump(notes2019, open('openreview_iclr2019_notes.pkl', 'wb'))
pickle.dump(notes2018, open('openreview_iclr2018_notes.pkl', 'wb'))
pickle.dump(notesGamesec, open('openreview_gamesec2018_notes.pkl', 'wb'))
pickle.dump(notesamlsearch, open('openreview_aml_search.pkl', 'wb'))

titles2019 = open('titles/iclr2019_uniq.txt', 'r').read().strip().split('\n')
titles2019 = set([l.strip().lower().replace(' ', '') for l in titles2019])

titles2018 = open('titles/iclr2018_search.txt', 'r').read().strip().split('\n')
titles2018 = set([l.strip().lower().replace(' ', '') for l in titles2018])

titlesgamesec = open('titles/gamesec.txt', 'r').read().strip().split('\n')
titlesgamesec = set([l.strip().lower().replace(' ', '') for l in titlesgamesec])

titlesearch = open('titles/amlsearch.txt', 'r').read().strip().split('\n')
titlesearch = set([l.strip().lower().replace(' ', '') for l in titlesearch])

db = pickle.load(open('db.p', 'rb'))

iclr2019notes = pickle.load(open('openreview_iclr2019_notes.pkl', 'rb'))
iclr2018notes = pickle.load(open('openreview_iclr2018_notes.pkl', 'rb'))
gamesecnotes = pickle.load(open('openreview_gamesec2018_notes.pkl', 'rb'))
amlsearchnotes = pickle.load(open('openreview_aml_search.pkl', 'rb'))
advnotes = []
oldtitles = set([p['title'].strip().lower() for p in db.values()])
for n in iclr2019notes:
    if n.content['title'].lower().strip().replace(' ', '') in titles2019:
        if n.content['title'].lower().strip() not in oldtitles:
            oldtitles.add(n.content['title'].strip().lower())
            print(n.content['title'])
            advnotes.append(n)

for n in iclr2018notes:
    if n.content['title'].lower().strip().replace(' ', '') in titles2018:
        if n.content['title'].lower().strip() not in oldtitles:
            oldtitles.add(n.content['title'].strip().lower())
            print(n.content['title'])
            advnotes.append(n)

for n in gamesecnotes:
    if n.content['title'].lower().strip().replace(' ', '') in titlesgamesec:
        if n.content['title'].lower().strip() not in oldtitles:
            oldtitles.add(n.content['title'].strip().lower())
            print(n.content['title'])
            advnotes.append(n)

for n in amlsearchnotes:
    if n.content['title'].lower().strip().replace(' ', '') in titlesearch:

        if n.content['title'].lower().strip() not in oldtitles:
            oldtitles.add(n.content['title'].strip().lower())
            print(n.content['title'])
            advnotes.append(n)
print(len(advnotes))
pickle.dump(advnotes, open('aml_notes.pkl', 'wb'))