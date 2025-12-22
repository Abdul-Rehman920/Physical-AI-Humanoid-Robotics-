# Data Model: RAG Data Retrieval

**Branch**: `003-rag-data-retrieval` | **Date**: 2025-12-22 | **Plan**: [plan.md](plan.md)
**Spec**: [spec.md](spec.md)

This document describes the data entities involved in the RAG Data Retrieval service.

---

## 1. Query Input

Represents the user's query to the retrieval service.

-   **Fields**:
    -   `query` (string): The user's natural language query.
    -   `top_k` (integer, optional): The maximum number of results to return. Defaults to 5.
    -   `threshold` (float, optional): The minimum similarity score for a result to be included. Defaults to 0.0.

-   **Validation Rules**:
    -   `query`: Must not be empty.

## 2. Response Structure

Represents the JSON object returned by the retrieval service.

-   **Fields**:
    -   `query` (string): The original query string.
    -   `query_time` (float): The time taken to process the query, in seconds.
    -   `result_count` (integer): The number of results returned.
    -   `timestamp` (float): The UNIX timestamp of when the response was generated.
    -   `results` (list of objects): A list of the retrieved text chunks.
        -   `content` (string): The text content of the chunk.
        -   `url` (string): The URL of the page where the chunk was found.
        -   `position` (integer): The index of the chunk on the page.
        -   `similarity_score` (float): The similarity score between the query and the chunk.
        -   `chunk_id` (string): The unique ID of the chunk.
        -   `created_at` (string): The timestamp of when the chunk was created.

-   **Validation Rules**:
    -   `results`: Each object in the list must contain all the specified fields.
    -   `similarity_score`: Must be a float between 0.0 and 1.0.
