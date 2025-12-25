# Tasks for RAG Agent API

This file outlines the tasks required to implement the RAG Agent API feature.

## Phase 1: Setup

- [X] T001 Update `requirements.txt` in `rag_pipeline/` with the new dependencies: `agents`, `fastapi`, `uvicorn[standard]`, `pydantic`, `python-dotenv`.
- [X] T002 Create the `agent.py` file in `rag_pipeline/`.
- [X] T003 Create the `api.py` file in `rag_pipeline/`.
- [X] T004 Create a `.env` file in `rag_pipeline/` for environment variables.

## Phase 2: User Story 1 - Health Check (P1)

**Goal**: A backend developer needs to confirm that the RAG Agent API is running and available.
**Test**: The `/health` endpoint can be called, and a successful response is received.

- [X] T005 [US1] In `rag_pipeline/api.py`, import `FastAPI` and create the app instance.
- [X] T006 [US1] In `rag_pipeline/api.py`, define the `HealthResponse` Pydantic model.
- [X] T007 [US1] In `rag_pipeline/api.py`, implement the `GET /health` endpoint that returns a `HealthResponse`.

## Phase 3: User Story 2 - Ask a Question (P1)

**Goal**: A backend developer wants to ask a question to the RAG agent and receive an answer based on the book's content.
**Test**: The `/ask` endpoint can be called with a question, and a successful response is received containing an answer, sources, and a confidence score.

- [X] T008 [P] [US2] In `rag_pipeline/api.py`, define the Pydantic models: `QueryRequest`, `MatchedChunk`, and `QueryResponse`.
- [X] T009 [P] [US2] In `rag_pipeline/agent.py`, import `Agent`, `Runner`, and `function_tool` from the `agents` library.
- [X] T010 [US2] In `rag_pipeline/agent.py`, implement the `retrieve_information` function as a `function_tool` that calls `RAGRetriever.retrieve()` from `retrieval.py`.
- [X] T011 [US2] In `rag_pipeline/agent.py`, create the `RAGAgent` class.
- [X] T012 [US2] In `rag_pipeline/agent.py`, implement the `__init__` method of `RAGAgent` to initialize the agent with instructions and the `retrieve_information` tool.
- [X] T013 [US2] In `rag_pipeline/agent.py`, implement the `_calculate_confidence` method.
- [X] T014 [US2] In `rag_pipeline/agent.py`, implement the `_async_query_agent` method using `Runner.run()`.
- [X] T015 [US2] In `rag_pipeline/agent.py`, implement the `query_agent` method to handle the async event loop and call `_async_query_agent`.
- [X] T016 [US2] In `rag_pipeline/api.py`, add a global `rag_agent` variable and initialize it in a `startup` event handler.
- [X] T017 [US2] In `rag_pipeline/api.py`, implement the `POST /ask` endpoint, which validates the request, calls `rag_agent.query_agent()`, and returns a `QueryResponse`.

## Phase 4: User Story 3 - Frontend Integration (P2)

**Goal**: A frontend developer wants to call the RAG Agent API from a web application.
**Test**: A pre-flight OPTIONS request can be made to the `/ask` endpoint from a different origin, and a successful response is received allowing the actual request.

- [X] T018 [US3] In `rag_pipeline/api.py`, import and add `CORSMiddleware` to the FastAPI app to allow all origins.

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T019 [P] Add logging configuration to `agent.py` and `api.py`.
- [X] T020 [P] In `rag_pipeline/agent.py`, add a `main()` function for standalone testing.
- [X] T021 [P] In `rag_pipeline/api.py`, add a `uvicorn` runner in a `__main__` block.


## Dependencies

- User Story 1 (`/health`) can be implemented independently.
- User Story 2 (`/ask`) depends on the completion of the agent implementation in `agent.py`.
- User Story 3 (CORS) can be implemented at any time but is most useful after User Story 2 is complete.

## Parallel Execution

- Within User Story 2, the Pydantic models (T008) and the basic agent structure (T009) can be created in parallel.
- The polish tasks (T019, T020, T021) can be worked on in parallel with the main features.

## Implementation Strategy

The implementation will follow an MVP approach, starting with the highest priority user stories.

1.  **MVP**: Implement User Story 1 (`/health`) and User Story 2 (`/ask`).
2.  **V1.1**: Add User Story 3 (CORS support).
3.  **V1.2**: Add polish and cross-cutting concerns.
