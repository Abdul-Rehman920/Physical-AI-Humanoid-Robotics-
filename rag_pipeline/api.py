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
    agent_initialized: bool

class QueryRequest(BaseModel):
    query: str = Field(..., max_length=2000, min_length=1)

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    error: Optional[str] = None
    status: str
    query_time_ms: float
    confidence: str

app = FastAPI(
    title="RAG Agent API",
    description="API for RAG Agent to answer questions about book content.",
    version="1.0.0",
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
    """Initialize RAG Agent on startup"""
    global rag_agent
    logging.info("🚀 Starting up RAG Agent...")
    try:
        rag_agent = RAGAgent()
        logging.info("✅ RAG Agent initialized successfully")
    except Exception as e:
        logging.error(f"❌ Failed to initialize RAG Agent: {e}")
        rag_agent = None

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logging.info("👋 Shutting down...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Chatbot API is running!",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "health_check": "GET /health",
            "ask_question": "POST /ask"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    is_healthy = rag_agent is not None
    return HealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        message="Service is running" if is_healthy else "Agent initialization failed",
        agent_initialized=is_healthy
    )

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Ask a question to the RAG agent
    
    - **query**: Your question about the book content
    """
    if rag_agent is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG Agent not initialized. Please check server logs."
        )
    
    try:
        logging.info(f"📝 Received query: '{request.query[:50]}...'")
        
        start_time = time.time()
        response_data = rag_agent.query_agent(request.query)
        query_time_ms = (time.time() - start_time) * 1000
        
        logging.info(f"✅ Query processed in {query_time_ms:.2f}ms")
        
        return QueryResponse(
            answer=response_data.get("answer", "No answer generated"),
            sources=response_data.get("sources", []),
            error=response_data.get("error"),
            status=response_data.get("status", "success"),
            query_time_ms=query_time_ms,
            confidence=response_data.get("confidence", "low")
        )
    
    except Exception as e:
        logging.error(f"❌ Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)