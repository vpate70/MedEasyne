from fastapi import FastAPI
from searchengine import SearchEngine

app = FastAPI()

engine = SearchEngine(r'./index/index')

@app.get("/search")
async def search(query):
    results = engine.search(query)
    return results