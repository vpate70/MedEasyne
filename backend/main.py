from http.client import HTTPException
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from searchengine import SearchEngine
from llm import LLM
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

engine = SearchEngine(r'./index')
llm = LLM("API")

class SearchQuery(BaseModel):
    query: str

@app.post("/search")
async def search(search_query: SearchQuery):
    results = engine.search(search_query.query)
    print(results)
    return JSONResponse(content={"titles": results[0], "authors": results[1], "abstracts": results[2]})

# made a seperate endpoint for now, since localLLM will take several minutes to run
@app.get("/llm")
async def llm(query):
    results = llm.local_llm(query)
    return results

if __name__ == "__main__":
    print("Starting...")
    uvicorn.run("main:app", host="127.0.0.1", reload=False)