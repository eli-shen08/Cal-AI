from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
# from endpoints import router

vectordb_ready = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectordb_ready

    print("Loading RAG System")
    from rag import get_rag_response

    vectordb_ready =True
    print("RAG System Ready")

    yield


class queryModel(BaseModel):
    query: str

app = FastAPI(lifespan=lifespan)
# app.include_router(router)

# Endpoint to check if vectordb is created
@app.get("/health")
async def health():
    return {
        "status": "ready" if vectordb_ready else "initializing",
        "vectordb_ready": vectordb_ready
    }


# Endpoint for RAG System
@app.post("/") 
async def query_rag_system(query: queryModel):
    if not vectordb_ready:
        raise HTTPException(
            status_code=503,
            detail="⏳ System is still initializing. Please wait."
        )
    try:
        from rag import get_rag_response
        # Pass the query string to your RAG system and return the response
        response = await get_rag_response(query.query)
        return {"query": query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))