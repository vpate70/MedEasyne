import requests
import gzip
import xml.etree.ElementTree as ET
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
import os
import time

TO_FETCH = 200

schema = Schema(
    title=TEXT(stored=True),          # Title field for storing the title of the document
    authors=TEXT(stored=True),        # Authors field for storing the names of the authors
    abstract=TEXT(stored=True)        # Abstract field for storing the abstract of the document
)

indexdir = "./index"
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
ix = None
try:
  ix = create_in(indexdir, schema)
except:
  ix = open_dir(indexdir)

def index_files(title, abstract, authors, writer):
    writer.add_document(title=title, abstract=abstract, authors=authors)

# Function to download and decompress the file
def download_and_extract(url):
    response = requests.get(url, stream=True)
    with open("pubmed.xml.gz", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    with gzip.open("pubmed.xml.gz", "rb") as gz_file:
        with open("pubmed.xml", "wb") as xml_file:
            xml_file.write(gz_file.read())

# Function to extract information from XML
def extract_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    articles = root.findall('.//PubmedArticle')
    writer = ix.writer()
    for article in articles:
        title_element = article.find(".//ArticleTitle")
        title = title_element.text.strip() if title_element is not None and title_element.text is not None else ""
        abstract_element = article.find(".//AbstractText")
        abstract = abstract_element.text.strip() if abstract_element is not None and abstract_element.text is not None else ""
        author_elements = article.findall(".//Author")
        authors = [f"{author.find('ForeName').text} {author.find('LastName').text}" for author in author_elements if author.find('ForeName') is not None and author.find('LastName') is not None]
        index_files(title, abstract, authors, writer)
    writer.commit()

for i in range(1,TO_FETCH+1):
  n_zeros = 4 - len(str(i))
  url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed24n"+n_zeros*"0"+str(i)+".xml.gz"
  start = time.process_time()
  download_and_extract(url)
  extract_info('pubmed.xml')
  print(i, url, time.process_time() - start)
