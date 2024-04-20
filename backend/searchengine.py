from whoosh.index import open_dir
from whoosh.qparser import QueryParser

class SearchEngine:
    def __init__(self, index_dir):
        self.index = open_dir(index_dir)

    def search(self, query, limit=5):
        with self.index.searcher() as searcher:
            parsed = QueryParser("abstract", self.index.schema).parse(query) # needs to be that multiquery thing
            results = searcher.search(parsed, limit=limit)
            return results