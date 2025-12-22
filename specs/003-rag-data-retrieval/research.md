# Research & Decisions: RAG Data Retrieval

**Branch**: `003-rag-data-retrieval` | **Date**: 2025-12-22 | **Plan**: [plan.md](plan.md)

This document records the research and key technical decisions made during the planning phase for the RAG Data Retrieval service.

---

### 1. Cohere Embedding Model

- **Decision**: The `embed-multilingual-v3.0` model will be used for generating query embeddings. The `input_type` will be set to `"search_query"`.
- **Rationale**: The `embed-multilingual-v3.0` model is specifically designed for high-performance retrieval tasks and supports multiple languages. Using the `"search_query"` input type optimizes the embedding for similarity search against a corpus of documents.
- **Alternatives Considered**:
    - Other Cohere models: The chosen model provides the best balance of performance and accuracy for this retrieval use case.

---

### 2. Qdrant Configuration

- **Decision**: The retrieval service will connect to the same Qdrant instance and collection (`rag_embedding`) used by the data ingestion pipeline.
- **Rationale**: This ensures that the retrieval service is querying the most up-to-date data available. The configuration is kept consistent between the two services for simplicity and reliability.
- **Alternatives Considered**:
    - Using a separate collection: This would require data to be duplicated or synchronized, adding unnecessary complexity.

---

### 3. Similarity Search Parameters

- **Decision**: The similarity search will use a `limit` parameter (`top_k`) to control the number of results and a `score_threshold` to filter out irrelevant results. The default `top_k` will be 5.
- **Rationale**: `top_k` allows the user to specify how many results they want, while the `score_threshold` ensures that only results with a certain level of similarity are returned, improving the quality of the output.
- **Alternatives Considered**:
    - Only using `top_k`: This could lead to irrelevant results being returned if there are no good matches in the database.
    - Only using `score_threshold`: This could lead to an unpredictable number of results being returned.

---

### 4. Retrieval Workflow

- **Decision**: The retrieval process will be orchestrated by a `retrieve` method that encapsulates the steps of generating a query embedding, searching for similar chunks, and formatting the response.
- **Rationale**: This approach provides a clean, high-level interface for the retrieval functionality, making it easy to integrate into other applications or services.
- **Alternatives Considered**:
    - Exposing the individual functions: This would require the user to understand the details of the retrieval process, making it more difficult to use.
