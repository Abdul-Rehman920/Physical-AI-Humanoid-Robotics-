from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from agent import RAGAgent
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HealthResponse(BaseModel):
    status: str
    message: str

class QueryRequest(BaseModel):
    query: str = Field(..., max_length=2000, min_length=1)

class MatchedChunk(BaseModel):
    content: str
    url: str
    position: int
    similarity_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    matched_chunks: List[MatchedChunk]
    error: Optional[str] = None
    status: str
    query_time_ms: float
    confidence: str

app = FastAPI(
    title="RAG Agent API",
    description="API for RAG Agent to answer questions about book content.",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_agent: Optional[RAGAgent] = None

@app.on_event("startup")
async def startup_event():
    global rag_agent
    rag_agent = RAGAgent()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", message="Service is healthy")

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    if rag_agent is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="RAG Agent not initialized."
        )
    
    start_time = time.time()
    response_data = rag_agent.query_agent(request.query)
    end_time = time.time()
    query_time_ms = (end_time - start_time) * 1000

    return QueryResponse(
        answer=response_data.get("answer", ""),
        sources=response_data.get("sources", []),
        matched_chunks=response_data.get("matched_chunks", []),
        error=response_data.get("error"),
        status=response_data.get("status", "success"),
        query_time_ms=query_time_ms,
        confidence=response_data.get("confidence", "low")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)