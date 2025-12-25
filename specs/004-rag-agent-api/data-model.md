# Data Models: RAG Agent API

This document outlines the data models used in the RAG Agent API. The models are defined using Pydantic for data validation and serialization.

## API Request/Response Models

### QueryRequest

Represents the request body for the `/ask` endpoint.

- **`query`** (`str`): The user's query string.

**Example**:
```json
{
  "query": "What is physical AI?"
}
```

### MatchedChunk

Represents a single chunk of retrieved text that matches the query.

- **`content`** (`str`): The text content of the chunk.
- **`url`** (`str`): The source URL of the content.
- **`position`** (`int`): The position of the chunk in the source document.
- **`similarity_score`** (`float`): The score indicating the relevance of the chunk to the query.


### QueryResponse

Represents the response body for the `/ask` endpoint.

- **`answer`** (`str`): The generated answer to the query.
- **`sources`** (`List[str]`): A list of source URLs cited in the answer.
- **`matched_chunks`** (`List[MatchedChunk]`): A list of the retrieved chunks used to generate the answer.
- **`error`** (`Optional[str]`): An error message if an error occurred.
- **`status`** (`str`): The status of the request (e.g., "success", "error").
- **`query_time_ms`** (`float`): The time taken to process the query in milliseconds.
- **`confidence`** (`str`): The confidence level of the answer ("high", "medium", or "low").

**Example**:
```json
{
  "answer": "Physical AI refers to artificial intelligence that interacts with the physical world through robotics.",
  "sources": [
    "/docs/module1-foundation/chapter1-physical-ai"
  ],
  "matched_chunks": [
    {
      "content": "Physical AI is the branch of AI that deals with...",
      "url": "/docs/module1-foundation/chapter1-physical-ai",
      "position": 1,
      "similarity_score": 0.92
    }
  ],
  "error": null,
  "status": "success",
  "query_time_ms": 1234.56,
  "confidence": "high"
}
```

### HealthResponse

Represents the response body for the `/health` endpoint.

- **`status`** (`str`): The status of the service (e.g., "ok").
- **`message`** (`str`): A message indicating the service is running.

**Example**:
```json
{
  "status": "ok",
  "message": "Service is healthy"
}
```
