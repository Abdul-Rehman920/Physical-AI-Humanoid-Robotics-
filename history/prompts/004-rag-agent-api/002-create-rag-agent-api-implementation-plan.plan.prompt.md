---
id: 002
title: Create RAG Agent API Implementation Plan
stage: plan
date: 2025-12-23
surface: agent
model: gemini-pro
feature: 004-rag-agent-api
branch: 004-rag-agent-api
user: ""
command: "/sp.plan Create implementation plan for RAG Agent API (Spec-3)"
labels: [planning, api, rag]
links:
  spec: specs/004-rag-agent-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-rag-agent-api/plan.md
 - specs/004-rag-agent-api/research.md
 - specs/004-rag-agent-api/data-model.md
 - specs/004-rag-agent-api/quickstart.md
tests:
  []
---

## Prompt

/sp.plan Create implementation plan for RAG Agent API (Spec-3)

Technical architecture:

**File 1: agent.py (OpenAI Agent SDK Implementation)**
- Import: Agent, Runner, function_tool from agents library
- Create @function_tool decorator for retrieve_information()
  - Tool calls RAGRetriever.retrieve() from retrieval.py (Spec-2)
  - Parameters: query (str)
  - Returns: Dict with retrieved_chunks, total_results
  - Handle errors gracefully
- Build RAGAgent class:
  - __init__: Initialize Agent with instructions and tools list
  - query_agent(query_text): Main entry point
  - _async_query_agent(query_text): Internal async method using Runner.run()
  - _calculate_confidence(matched_chunks): Returns "high"/"medium"/"low"
- Handle async/sync execution properly (asyncio event loop management)
- Add logging for debugging
- Include main() function for standalone testing

**File 2: api.py (FastAPI Implementation)**
- Create FastAPI app instance with title, description, version
- Add CORSMiddleware (allow all origins for development)
- Define Pydantic models:
  - QueryRequest: query field
  - MatchedChunk: content, url, position, similarity_score
  - QueryResponse: answer, sources, matched_chunks, error, status, query_time_ms, confidence
  - HealthResponse: status, message
- Global variable: rag_agent = None
- @app.on_event("startup"): Initialize RAGAgent instance
- POST /ask endpoint:
  - Validate query (not empty, max 2000 chars)
  - Call rag_agent.query_agent()
  - Format response with proper error handling
  - Return QueryResponse
- GET /health endpoint: Return service status
- Add uvicorn runner in __main__

**Integration points:**
- agent.py imports RAGRetriever from retrieval.py (Spec-2)
- api.py imports RAGAgent from agent.py
- Both files use dotenv for environment variables
- Logging configured at INFO level

**Dependencies to add in requirements.txt:**
- agents (OpenAI Agent SDK)
- fastapi
- uvicorn[standard]
- pydantic

**Testing approach:**
- Test agent.py standalone with sample queries
- Test API with curl/Postman before frontend integration
- Verify CORS headers for cross-origin requests

## Response snapshot

I have successfully executed the implementation planning workflow.

- Updated `specs/004-rag-agent-api/plan.md` with the detailed technical plan.
- Created `specs/004-rag-agent-api/research.md` to document the technology choices.
- Created `specs/004-rag-agent-api/data-model.md` to define the API data structures.
- Created `specs/004-rag-agent-api/quickstart.md` with setup and usage instructions.
- Updated the agent context to include the new dependencies.

## Outcome

- ✅ Impact: High - The core plan for the RAG Agent API is now in place.
- 🧪 Tests: No tests were run.
- 📁 Files: 4 files created/updated in the `specs` directory.
- 🔁 Next prompts: The next step is to proceed with the implementation based on the created plan.
- 🧠 Reflection: The user provided a very detailed technical plan, which made the process smooth. The PHR script failure on Windows was an expected issue with a clear fallback.
