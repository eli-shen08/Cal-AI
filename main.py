from fastapi import FastAPI, HTTPException
from rag import get_rag_response
from pydantic import BaseModel
# from endpoints import router

class queryModel(BaseModel):
    query: str

app = FastAPI()
# app.include_router(router)

@app.post("/") 
async def query_rag_system(query: queryModel):
    try:
        # Pass the query string to your RAG system and return the response
        response = await get_rag_response(query.query)
        return {"query": query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))