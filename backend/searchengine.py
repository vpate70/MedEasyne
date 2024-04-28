from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser

class SearchEngine:
    def __init__(self, index_dir):
        self.index = open_dir(index_dir)
        pass

    def search(self, query, limit=3):
        with self.index.searcher() as searcher:
            parsed = MultifieldParser(["title", "abstract"], self.index.schema).parse(query)
            results = searcher.search(parsed, limit=limit)
            # some titles are enclosed with brackets; just strip them
            return [hit['title'].strip('[]') for hit in results], [hit['authors'] for hit in results], [hit['abstract'] for hit in results]