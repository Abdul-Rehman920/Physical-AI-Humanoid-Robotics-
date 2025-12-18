# Data Model: RAG Data Ingestion Pipeline

**Branch**: `002-rag-data-ingestion` | **Date**: 2025-12-18 | **Plan**: [plan.md](plan.md)
**Spec**: [spec.md](spec.md)

This document describes the data entities involved in the RAG Data Ingestion Pipeline.

---

## 1. Content Chunk

Represents a segment of text extracted from a Docusaurus webpage. This is the atomic unit that will be embedded.

-   **Fields**:
    -   `text_content` (string): The cleaned, textual content of the chunk.
    -   `source_url` (string): The URL of the webpage from which the chunk was extracted.
    -   `page_title` (string): The title of the webpage from which the chunk was extracted.
    -   `chunk_id` (string): A unique identifier for the chunk, potentially a hash of the content or a generated UUID.

-   **Validation Rules**:
    -   `text_content`: Must not be empty.
    -   `source_url`: Must be a valid URL.
    -   `page_title`: Should not be empty.

## 2. Embedding Vector

Represents the numerical vector embedding generated from a `Content Chunk` using the Cohere API.

-   **Fields**:
    -   `vector_data` (list of floats): The numerical representation of the `text_content`.
    -   `chunk_id` (string): A foreign key referencing the `chunk_id` of the `Content Chunk` it represents.

-   **Validation Rules**:
    -   `vector_data`: Must be a list of floats and match the expected dimensionality of the Cohere embedding model.
    -   `chunk_id`: Must reference an existing `Content Chunk`.

## 3. Qdrant Record

Represents a single point (record) stored in the Qdrant vector database. Each record combines an `Embedding Vector` with its associated `Content Chunk` metadata.

-   **Structure**:
    -   `id` (string): The unique identifier for the Qdrant point, derived from `chunk_id`.
    -   `vector` (list of floats): The `vector_data` from the `Embedding Vector`.
    -   `payload` (dictionary): A JSON object containing metadata.
        -   `payload.text_content` (string): The `text_content` from the associated `Content Chunk`.
        -   `payload.source_url` (string): The `source_url` from the associated `Content Chunk`.
        -   `payload.page_title` (string): The `page_title` from the associated `Content Chunk`.

-   **Relationships**:
    -   Each `Qdrant Record` corresponds directly to one `Content Chunk` and one `Embedding Vector`.
