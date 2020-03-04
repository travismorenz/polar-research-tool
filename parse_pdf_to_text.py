import urllib.request
from io import StringIO, BytesIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Based on https://pdfminersix.readthedocs.io/en/latest/tutorials/composable.html
def parse_pdf_to_text(url):
  try:
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
    return output_string.getvalue()
  except Exception as err:
    return err
