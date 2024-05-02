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
model = LLM("local") 

class SearchQuery(BaseModel):
    query: str

class LlmQuery(BaseModel):
    user_desc: str
    query: str

@app.post("/search")
async def search(search_query: SearchQuery):
    results = engine.search(search_query.query)
    return JSONResponse(content={"titles": results[0], "authors": results[1], "abstracts": results[2]})

# made a seperate endpoint for now, since localLLM will take several minutes to run
@app.post("/llm")
async def llm(llm_query: LlmQuery):
    results = model.local_llm(llm_query.user_desc, llm_query.query)
    # results = '''From the input passage, I've extracted two difficult healthcare words:\n\n1. **Pathology**: Pathology is the study of the nature of diseases, and it involves the examination of tissues, cells, and bodily fluids to diagnose and understand diseases. In a broader sense, pathology can also refer to the branch of medicine that deals with the examination of diseased tissues and organs.\n\nExample sentence: \"The doctor sent the tissue sample to the pathology lab for further examination.\"\n\n2. **Chemistry**: In the context of healthcare, chemistry refers to the study of the chemical composition and properties of substances found in the human body. It's an essential aspect of medicine, as it helps healthcare professionals understand the biochemical processes that occur within the body and develop treatments for various diseases.\n\nExample sentence: \"The doctor ordered a chemistry panel to test the patient's blood for any abnormalities.\"\n\nLet me know if you'd like me to define any other words or phrases from the passage!'''
    return results

if __name__ == "__main__":
    print("Starting...")
    uvicorn.run("main:app", host="127.0.0.1", reload=False)