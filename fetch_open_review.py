from __future__ import print_function
import openreview
import pickle
import time
from utils import Config, safe_pickle_dump
import os
import math
import time
c = openreview.Client(baseurl='https://openreview.net', username='aaron.tuor@pnnl.gov',
                      password='!trex1000')
db = pickle.load(open('db.p', 'rb'))

advnotes = pickle.load(open('aml_notes.pkl', 'rb'))
def urlfrombibtex(bib):
    url = bib.split('url={')[-1].split('}')[0]
    return url

print(len(advnotes))
pdffolder = Config.pdf_dir
for idx, n in enumerate(advnotes):
    print(idx, n.content['title'])
    print(os.path.join(pdffolder, n.id) + '.pdf')
    entry = dict()
    entry['id'] = 'https://openreview.net/forum?id=' + n.id
    entry['guidislink'] = True
    entry['link'] = 'https://openreview.net/forum?id=' + n.id
    entry['updated_parsed'] = time.gmtime(math.ceil(n.tmdate/1000))
    entry['updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry['updated_parsed'])
    print(entry['updated'])
    entry['published_parsed'] = time.gmtime(math.ceil(n.tmdate/1000))
    entry['published'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry['published_parsed']) 
    print(entry['published'])
    entry['title'] = n.content['title']
    entry['title_detail'] = {'type': 'text/plain', 'language': None, 'base': '',
                            'value': n.content['title']}
    entry['summary'] = n.content['abstract']
    entry['summary_detail'] = {'type': 'text/plain', 'language': None, 'base': '',
                               'value': n.content['abstract']}
    entry['authors'] = list([{'name': name} for name in n.content['authors']])
    entry['author'] = n.content['authors'][0]
    entry['author_detail'] = {'name': entry['author']}
    entry['links'] = [{'title': 'doi', 'href': entry['link'],
                    'rel': 'related',
                    'type': 'text/html'},
                    {'href': entry['link'],
                    'rel': 'alternate',
                    'type': 'text/html'},
                    {'title': 'pdf',
                     'href': 'https://openreview.net/pdf?id=' + n.id,
                    'rel': 'related',
                    'type': 'application/pdf'}],
    entry['arxiv_primary_category'] = {'term': 'OpenReview', 'scheme':'http://arxiv.org/schemas/atom'}
    entry['arxiv_comment'] = ''
    entry['tags'] = [{'term': 'OpenReview', 'scheme':'http://arxiv.org/schemas/atom', 'label':None}] 
    entry['_rawid'] = n.id
    entry['_version'] = 0
    entry['time_updated'] = math.ceil(n.tmdate/1000)
    entry['time_published'] = math.ceil(n.tmdate/1000)
    db[n.id] = entry 
    f = c.get_pdf(id=n.id)
    with open(os.path.join(pdffolder, n.id) + 'v' + str(entry['_version']) + '.pdf', 'wb') as op: 
        op.write(f)
    # time.sleep(1)

safe_pickle_dump(db, Config.db_path)



# notekeys = ['id', 'original', 'number', 'cdate', 'tcdate', 'tmdate', 'ddate', 'content', 'forum', 
# 'referent', 'invitation', 'replyto', 'readers', 'nonreaders', 'signatures', 'writers', 'details']
# dbkeys = ['id', 'guidislink', 'link', 'updated', 'updated_parsed', 'published', 
# 'published_parsed', 'title', 'title_detail', 'summary', 'summary_detail', 'authors', 
# 'author_detail', 'author', 'links', 'arxiv_primary_category', 'tags', '_rawid', '_version']
# Note(id = 'Hk6kPgZA-',original = 'SJ6kPgWC-',number = 596,cdate = 1518730171899,tcdate = 1509127909457,
# tmdate = 1546570475487,ddate = None,
# content = {'title': 'Certifying Some Distributional Robustness with Principled Adversarial Training', 
# 'abstract': 'Neural networks are vulnerable to adversarial examples and researchers have proposed many heuristic attack and defense mechanisms. We address this problem through the principled lens of distributionally robust optimization, which guarantees performance under adversarial input perturbations.  By considering a Lagrangian penalty formulation of perturbing the underlying data distribution in a Wasserstein ball, we provide a training procedure that augments model parameter updates with worst-case perturbations of training data. For smooth losses, our procedure provably achieves moderate levels of robustness with little computational or statistical cost relative to empirical risk minimization. Furthermore, our statistical guarantees allow us to efficiently certify robustness for the population loss. For imperceptible perturbations, our method matches or outperforms heuristic approaches.\n', 
#     'pdf': '/pdf/f35b7c6c945a42b2b053053616d2393ae0ee6304.pdf', 'TL;DR': 'We provide a fast, principled adversarial training procedure with computational and statistical performance guarantees.', 'paperhash': 'sinha|certifying_some_distributional_robustness_with_principled_adversarial_training', 
#     'authors': ['Aman Sinha', 'Hongseok Namkoong', 'John Duchi'], 
#     'keywords': ['adversarial training', 'distributionally robust optimization', 'deep learning', 'optimization', 'learning theory'], 
#     'authorids': ['amans@stanford.edu', 'hnamk@stanford.edu', 'jduchi@stanford.edu'], 
#     '_bibtex': '@inproceedings{\nsinha2018certifiable,'
#                                '\ntitle={Certifiable Distributional Robustness with Principled Adversarial Training},'
#                                '\nauthor={Aman Sinha and Hongseok Namkoong and John Duchi},'
#                                '\nbooktitle={International Conference on Learning Representations},'
#                                '\nyear={2018},'
#                                '\nurl={https://openreview.net/forum?id=Hk6kPgZA-},\n}'},
#     forum = 'Hk6kPgZA-',referent = None,invitation = 'ICLR.cc/2018/Conference/-/Blind_Submission',
#     replyto = None,readers = ['everyone'],nonreaders = [],
#     signatures = ['ICLR.cc/2018/Conference'],writers = ['ICLR.cc/2018/Conference'],details = {'replyCount': 20})
# {'id': 'http://arxiv.org/abs/1801.00349v2',
#  'guidislink': True,
#  'link': 'http://arxiv.org/abs/1801.00349v2',
#  'updated': '2019-04-04T01:14:44Z',
#  'updated_parsed': time.struct_time(tm_year=2019, tm_mon=4, tm_mday=4, tm_hour=1, tm_min=14, tm_sec=44, tm_wday=3, tm_yday=94, tm_isdst=0),
#  'published': '2017-12-31T20:17:45Z',
#  'published_parsed': time.struct_time(tm_year=2017, tm_mon=12, tm_mday=31, tm_hour=20, tm_min=17, tm_sec=45, tm_wday=6, tm_yday=365, tm_isdst=0),
#  'title': 'A General Framework for Adversarial Examples with Objectives',
#  'title_detail': {'type': 'text/plain',
#   'language': None,
#   'base': '',
#   'value': 'A General Framework for Adversarial Examples with Objectives'},
#  'summary': 'Images perturbed subtly to be misclassified by neural networks, called\nadversarial examples, have emerged as a technically deep challenge and an\nimportant concern for several application domains. Most research on adversarial\nexamples takes as its only constraint that the perturbed images are similar to\nthe originals. However, real-world application of these ideas often requires\nthe examples to satisfy additional objectives, which are typically enforced\nthrough custom modifications of the perturbation process. In this paper, we\npropose adversarial generative nets (AGNs), a general methodology to train a\ngenerator neural network to emit adversarial examples satisfying desired\nobjectives. We demonstrate the ability of AGNs to accommodate a wide range of\nobjectives, including imprecise ones difficult to model, in two application\ndomains. In particular, we demonstrate physical adversarial examples---eyeglass\nframes designed to fool face recognition---with better robustness,\ninconspicuousness, and scalability than previous approaches, as well as a new\nattack to fool a handwritten-digit classifier.',
#  'summary_detail': {'type': 'text/plain',
#   'language': None,
#   'base': '',
#   'value': 'Images perturbed subtly to be misclassified by neural networks, called\nadversarial examples, have emerged as a technically deep challenge and an\nimportant concern for several application domains. Most research on adversarial\nexamples takes as its only constraint that the perturbed images are similar to\nthe originals. However, real-world application of these ideas often requires\nthe examples to satisfy additional objectives, which are typically enforced\nthrough custom modifications of the perturbation process. In this paper, we\npropose adversarial generative nets (AGNs), a general methodology to train a\ngenerator neural network to emit adversarial examples satisfying desired\nobjectives. We demonstrate the ability of AGNs to accommodate a wide range of\nobjectives, including imprecise ones difficult to model, in two application\ndomains. In particular, we demonstrate physical adversarial examples---eyeglass\nframes designed to fool face recognition---with better robustness,\ninconspicuousness, and scalability than previous approaches, as well as a new\nattack to fool a handwritten-digit classifier.'},
#  'authors': [{'name': 'Mahmood Sharif'},
#   {'name': 'Sruti Bhagavatula'},
#   {'name': 'Lujo Bauer'},
#   {'name': 'Michael K. Reiter'}],
#  'author_detail': {'name': 'Michael K. Reiter'},
#  'author': 'Michael K. Reiter',
#  'arxiv_doi': '10.1145/3317611',
#  'links': [{'title': 'doi',
#    'href': 'http://dx.doi.org/10.1145/3317611',
#    'rel': 'related',
#    'type': 'text/html'},
#   {'href': 'http://arxiv.org/abs/1801.00349v2',
#    'rel': 'alternate',
#    'type': 'text/html'},
#   {'title': 'pdf',
#    'href': 'http://arxiv.org/pdf/1801.00349v2',
#    'rel': 'related',
#    'type': 'application/pdf'}],
#  'arxiv_comment': 'Accepted for publication at ACM TOPS',
#  'arxiv_primary_category': {'term': 'cs.CV',
#   'scheme': 'http://arxiv.org/schemas/atom'},
#  'tags': [{'term': 'cs.CV',
#    'scheme': 'http://arxiv.org/schemas/atom',
#    'label': None},
#   {'term': 'cs.CR', 'scheme': 'http://arxiv.org/schemas/atom', 'label': None}],
#  '_rawid': '1801.00349',
#  '_version': 2,
#  'time_updated': 1554369284,
#  'time_published': 1514780265,
#  'tscore': 1.0}

 


# '2017-12-31T20:17:45Z'