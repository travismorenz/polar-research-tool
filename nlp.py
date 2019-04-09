import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import spacy
nlp = spacy.load("en", disable=['ner', 'parser'])
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import pandas as pd
from pprint import pprint
import datetime
import pickle
import rake
import summa
import os

# Gensim
import gensim
from gensim.models import CoherenceModel

# Plotting tools
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
from matplotlib import rcParams


# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
smart_stop = open('smart_stoplist.txt', 'r').read().strip().split('\n')
stop_words.extend(smart_stop)
stop_words = sorted(list(set(stop_words)))
pprint(stop_words)


def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True, max_len=20))


def remove_stopwords(texts):
    return [[word for word in doc if word not in stop_words] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out  # text = lemmas(text)


def lemmas(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if token.pos_ in allowed_postags])

db = pickle.load(open('db.p', 'rb'))
print('%s Articles' % len(db))

arxiv_texts = [v['summary'] for v in db.values()]
dates = [datetime.datetime.strptime(v['published'], '%Y-%m-%dT%H:%M:%SZ') for v in db.values()]
datetexts = sorted(zip(arxiv_texts, dates), key=lambda x: x[1])
datetextchunks = [[k for k in datetexts if k[1].year == i] for i in range(min(dates).year, max(dates).year + 1)]
plt.bar(range(min(dates).year, max(dates).year + 1), [len(k) for k in datetextchunks])
plt.xticks(range(min(dates).year, max(dates).year + 1), rotation=90)
plt.savefig('static/year_freq.pdf')
plt.show()

date_30_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
recent_arxiv_texts = [k[0] for k in datetexts if (k[1] > date_30_days_ago)]
print('%s new articles in the last 30 days' % len(recent_arxiv_texts))

rake_object = rake.Rake('smart_stoplist.txt', 5, 3, 4)
text = ' '.join(arxiv_texts)
keywords = rake_object.run(text)

keywords = [(w, s) for w, s in keywords if len(w.split()) > 1]
df = pd.DataFrame(keywords, columns =['Key Phrase: RAKE', 'Score'])
df.to_html('templates/rake_keyphrase.html')
print(df)

kw = keywords[:30]
kw.reverse()
scores = np.array([t[1] for t in kw])
scores /= max(scores)
plt.barh(range(30), scores)
plt.yticks(range(30), labels=[tw[0] for tw in kw], fontsize=7)
plt.axes().set_aspect('auto')
plt.tight_layout()
plt.savefig('static/rake_global.pdf')
plt.show()

splittext = text.split()
text = ' '.join([word for word in splittext if word not in stop_words])
text = lemmas(text)
kw = summa.keywords.keywords(text, ratio=0.3, scores=True)
kw = [(w, s) for w, s in kw if len(w.split()) > 1 and len(w.split()) < 5]

df = pd.DataFrame(kw, columns =['Key Phrase: Text Rank', 'Score'])
df.to_html('templates/textrank_keyphrase.html')
print(df)

kw = kw[:30]
kw.reverse()
scores = np.array([t[1] for t in kw])
scores /= max(scores)
plt.barh(range(30), scores)
plt.yticks(range(30), labels=[tw[0] for tw in kw], fontsize=7)
plt.axes().set_aspect('auto')
plt.tight_layout()
plt.savefig('static/textrank_global.pdf')
plt.show()

best_score = -1000
data_words = list(sent_to_words(recent_arxiv_texts))
data_words_nostops = remove_stopwords(data_words)
data_lemmatized = lemmatization(data_words_nostops, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
data_lemmatized = [' '.join(k) for k in data_lemmatized]
counts = CountVectorizer(ngram_range=(2, 3))
counts.fit(data_lemmatized)
id2word = {v: k for k, v in counts.vocabulary_.items()}
x = counts.transform(data_lemmatized)
rows, cols = x.nonzero()
vals = [x[r, c] for r, c in zip(rows, cols)]
uniqrows = np.unique(rows)
corpus = [[(k, v) for i, k, v in zip(rows, cols, vals) if i == n] for n in uniqrows]
for i in range(3, 20):

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=i,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
    id2word = gensim.corpora.Dictionary.from_corpus(corpus, id2word)

    coherence_model_lda = CoherenceModel(model=lda_model, corpus=corpus, dictionary=id2word, coherence='u_mass')
    coherence_lda = coherence_model_lda.get_coherence()
    if coherence_lda > best_score:
        best_model = lda_model
        best_score = coherence_lda
        best_num = i
    print('%s: Coherence Score: %s' % (i, coherence_lda))

id2word = gensim.corpora.Dictionary.from_corpus(corpus, id2word)
vis = pyLDAvis.gensim.prepare(best_model, corpus, id2word)
pyLDAvis.save_html(vis, 'templates/recent_lda.html')

data_words = list(sent_to_words(arxiv_texts))
data_words_nostops = remove_stopwords(data_words)
data_lemmatized = lemmatization(data_words_nostops, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
data_lemmatized = [' '.join(k) for k in data_lemmatized]
counts = CountVectorizer(ngram_range=(2, 3))
counts.fit(data_lemmatized)
id2word = {v:k for k, v in counts.vocabulary_.items()}
x = counts.transform(data_lemmatized)
rows, cols = x.nonzero()
vals = [x[r, c] for r, c in zip(rows, cols)]
uniqrows = np.unique(rows)
corpus = [[(k, v) for i, k, v in zip(rows, cols, vals) if i == n] for n in uniqrows]
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

x = lda_model.get_topics()
words = x.sum(axis=0)
idxs = np.argsort(words)
topwords = [(id2word[i], words[i]) for i in idxs]
kw = topwords[-30:]
scores = np.array([t[1] for t in kw])

plt.barh(range(30), scores)
plt.yticks(range(30), labels=[tw[0] for tw in kw], fontsize=7)
plt.axes().set_aspect('auto')
plt.tight_layout()
plt.savefig('static/lda_global.pdf')
plt.show()

kw = sorted(topwords, key=lambda x: x[1], reverse=True)[:150]
df = pd.DataFrame(kw, columns =['Key Phrase: LDA', 'Score'])
df.to_html('templates/lda_keyphrase.html')
print(df)

tfidf = TfidfVectorizer(ngram_range=(2, 3), norm='l2')
tfidf.fit(data_lemmatized)
id2word = {v:k for k, v in tfidf.vocabulary_.items()}
x = tfidf.transform(data_lemmatized).toarray()
words = x.mean(axis=0)
idxs = np.argsort(words)

topwords = [(id2word[i], words[i]) for i in idxs if ' ' in id2word[i]]

plt.barh(range(0, len(topwords[-30:])*4, 4), [t[1] for t in topwords[-30:]], height=3)
plt.yticks(range(0, len(topwords[-30:])*4, 4), labels=[tw[0] for tw in topwords[-30:]], fontsize=7)
plt.axes().set_aspect('auto')
plt.tight_layout()
plt.savefig('static/tfidf_global.pdf')
plt.show()

kw = sorted(topwords, key=lambda x: x[1], reverse=True)[:150]
df = pd.DataFrame(kw, columns =['Key Phrase: TF-IDF', 'Score'])
df.to_html('templates/tfidf_keyphrase.html')
print(df)

rcParams.update({'figure.autolayout': False})
datetextchunks = [[k for k in datetexts if k[1].year == i] for i in range(2013, 2020)]
topwords = []
for ik, dtc in enumerate(datetextchunks):
    arxiv_texts_ = [k[0] for k in dtc]
    data_words = list(sent_to_words(arxiv_texts_))
    data_words = remove_stopwords(data_words)
    data_lemmatized = lemmatization(data_words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    data_lemmatized = [' '.join(t) for t in data_lemmatized]
    tfidf = TfidfVectorizer(ngram_range=(2, 3))
    tfidf.fit(data_lemmatized)
    id2word = {v: k for k, v in tfidf.vocabulary_.items()}
    x = tfidf.transform(data_lemmatized).toarray()
    words = x.mean(axis=0)
    idxs = np.argsort(words)
    ids = idxs[-30:]
    scores = words[ids]
    topwords.append([(id2word[i], words[i]) for i in ids])
f, axarr = plt.subplots(2, 4, figsize=(30, 20))
freq = list([len(d) for d in datetextchunks])
freq[-1] -= 2
axarr[0][0].bar(range(2013, 2020), freq, color='y')
axarr[0][0].set_xticks(range(2013, 2020))
axarr[0][0].set_xticklabels([str(k) for k in range(2013, 2020)], rotation=60)
axarr[0][0].set_title('Document Frequency per Year')
axarr[0][0].set_aspect('auto')
axarr[0][0].spines['top'].set_visible(False)
axarr[0][0].spines['right'].set_visible(False)
axarr[0][0].spines['bottom'].set_visible(False)
axarr[0][0].spines['left'].set_visible(False)

for i in range(2013, 2016):
    axarr[0][i - 2012].barh(range(0, len(topwords[0]) * 4, 4), [t[1] for t in topwords[i - 2013]], height=3, color='y')
    axarr[0][i - 2012].set_yticks(range(0, len(topwords[i - 2013]) * 4, 4))
    axarr[0][i - 2012].set_yticklabels([tw[0] for tw in topwords[i - 2013]], fontsize=12)
    axarr[0][i - 2012].set_aspect('auto')
    axarr[0][i - 2012].set_title(str(i))
    axarr[0][i - 2012].set_xlabel('Top Average TFIDFs')
    axarr[0][i - 2012].spines['top'].set_visible(False)
    axarr[0][i - 2012].spines['right'].set_visible(False)
    axarr[0][i - 2012].spines['bottom'].set_visible(False)
    axarr[0][i - 2012].spines['left'].set_visible(False)

for i in range(2016, 2020):
    axarr[1][i - 2016].barh(range(0, len(topwords[0]) * 4, 4), [t[1] for t in topwords[i - 2016]], height=3, color='y')
    axarr[1][i - 2016].set_yticks(range(0, len(topwords[i - 2016]) * 4, 4))
    axarr[1][i - 2016].set_yticklabels([tw[0] for tw in topwords[i - 2016]], fontsize=12)
    axarr[1][i - 2016].set_aspect('auto')
    axarr[1][i - 2016].set_title(str(i))
    axarr[1][i - 2016].set_xlabel('Top Average TFIDFs')
    axarr[1][i - 2016].spines['top'].set_visible(False)
    axarr[1][i - 2016].spines['right'].set_visible(False)
    axarr[1][i - 2016].spines['bottom'].set_visible(False)
    axarr[1][i - 2016].spines['left'].set_visible(False)

plt.savefig('static/tfidf_time.pdf')
plt.show()

topwords = []
for ik, dtc in enumerate(datetextchunks):
    arxiv_texts_ = [k[0] for k in dtc]
    data_words = list(sent_to_words(arxiv_texts_))
    data_words_nostops = remove_stopwords(data_words)
    data_lemmatized = lemmatization(data_words_nostops, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    data_lemmatized = [' '.join(k) for k in data_lemmatized]
    counts = CountVectorizer(ngram_range=(2, 3))
    counts.fit(data_lemmatized)
    id2word = {v: k for k, v in counts.vocabulary_.items()}
    x = counts.transform(data_lemmatized)
    rows, cols = x.nonzero()
    vals = [x[r, c] for r, c in zip(rows, cols)]
    uniqrows = np.unique(rows)
    corpus = [[(k, v) for i, k, v in zip(rows, cols, vals) if i == n] for n in uniqrows]
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=5,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

    x = lda_model.get_topics()
    words = x.sum(axis=0)
    idxs = np.argsort(words)
    ids = idxs[-30:]
    scores = words[ids]
    topwords.append([(id2word[i], words[i]) for i in ids])

f, axarr = plt.subplots(2, 4, figsize=(30, 20))
freq = list([len(d) for d in datetextchunks])
freq[-1] -= 2
axarr[0][0].bar(range(2013, 2020), freq, color='y')
axarr[0][0].set_xticks(range(2013, 2020))
axarr[0][0].set_xticklabels([str(k) for k in range(2013, 2020)], rotation=60)
axarr[0][0].set_title('Document Frequency per Year')
axarr[0][0].set_aspect('auto')
axarr[0][0].spines['top'].set_visible(False)
axarr[0][0].spines['right'].set_visible(False)
axarr[0][0].spines['bottom'].set_visible(False)
axarr[0][0].spines['left'].set_visible(False)

for i in range(2013, 2016):
    axarr[0][i - 2012].barh(range(0, len(topwords[0]) * 4, 4), [t[1] for t in topwords[i - 2013]], height=3, color='y')
    axarr[0][i - 2012].set_yticks(range(0, len(topwords[i - 2013]) * 4, 4))
    axarr[0][i - 2012].set_yticklabels([tw[0] for tw in topwords[i - 2013]], fontsize=12)
    axarr[0][i - 2012].set_aspect('auto')
    axarr[0][i - 2012].set_title(str(i))
    axarr[0][i - 2012].set_xlabel('Top Average Topic Weights')
    axarr[0][i - 2012].spines['top'].set_visible(False)
    axarr[0][i - 2012].spines['right'].set_visible(False)
    axarr[0][i - 2012].spines['bottom'].set_visible(False)
    axarr[0][i - 2012].spines['left'].set_visible(False)

for i in range(2016, 2020):
    axarr[1][i - 2016].barh(range(0, len(topwords[0]) * 4, 4), [t[1] for t in topwords[i - 2016]], height=3, color='y')
    axarr[1][i - 2016].set_yticks(range(0, len(topwords[i - 2016]) * 4, 4))
    axarr[1][i - 2016].set_yticklabels([tw[0] for tw in topwords[i - 2016]], fontsize=12)
    axarr[1][i - 2016].set_aspect('auto')
    axarr[1][i - 2016].set_title(str(i))
    axarr[1][i - 2016].set_xlabel('Top Average Topic Weights')
    axarr[1][i - 2016].spines['top'].set_visible(False)
    axarr[1][i - 2016].spines['right'].set_visible(False)
    axarr[1][i - 2016].spines['bottom'].set_visible(False)
    axarr[1][i - 2016].spines['left'].set_visible(False)

plt.savefig('static/lda_time.pdf')
plt.show()

os.system('cd templates; cat head_keyphrase.html tfidf_keyphrase.html lda_keyphrase.html textrank_keyphrase.html rake_keyphrase.html tail_keyphrase.html > keyphrase.html')