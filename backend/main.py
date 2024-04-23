from http.client import HTTPException
from fastapi import FastAPI
from searchengine import SearchEngine
from llm import LLM
import uvicorn
import os
import requests
import json

app = FastAPI()

engine = SearchEngine(r'./index/index')
llm = LLM("API")

@app.get("/search")
async def search(query):
    results = engine.search(query)
    return results

# made a seperate endpoint for now, since localLLM will take several minutes to run
@app.get("/llm")
async def llm(query):
    results = llm.local_llm(query)
    return results

if __name__ == "__main__":
    print("Starting...")
    uvicorn.run("main:app", host="127.0.0.1", reload=False)