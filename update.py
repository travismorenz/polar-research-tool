import os
os.system('python fetch_keyphrase_papers.py')
os.system('python fetch_semantic_scholar.py')
os.system('python stats.py')
os.system('python download_pdfs.py')
os.system('python parse_pdf_to_text.py')
os.system('python thumb_pdf.py')
os.system('python analyze.py')
os.system('python buildsvm.py')
#os.system('make_cache.py')
#os.system('nlp.py')

