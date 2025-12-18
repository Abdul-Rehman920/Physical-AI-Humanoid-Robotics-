# Research & Decisions: RAG Data Ingestion Pipeline

**Branch**: `002-rag-data-ingestion` | **Date**: 2025-12-18 | **Plan**: [plan.md](plan.md)

This document records the research and key technical decisions made during the planning phase for the RAG Data Ingestion Pipeline.

---

### 1. Secret Management (API Keys)

- **Decision**: API keys for Cohere and Qdrant will be managed using environment variables. A `.env` file will be used for local development, and `python-dotenv` will load the variables. A `.env.example` file will be committed to the repository to document the required variables.
- **Rationale**: This is a standard, secure practice that avoids hardcoding sensitive information in the source code. It allows for different environments (local, staging, production) to use different keys without code changes.
- **Alternatives Considered**:
    - Hardcoding keys: Insecure and inflexible. Rejected.
    - Using a dedicated secrets management service (e.g., HashiCorp Vault): Overkill for this project's scale. Rejected for simplicity.

---

### 2. Web Scraping Strategy

- **Decision**: The pipeline will parse the `sitemap.xml` file of the deployed Docusaurus website to discover all URLs. For each URL, `requests` will be used to fetch the HTML content and `BeautifulSoup4` for parsing.
- **Rationale**: Using `sitemap.xml` is efficient and standard for discovering all public-facing URLs of a website. It ensures comprehensive coverage and avoids the complexities of dynamic crawling for this specific use case.
- **Alternatives Considered**:
    - Crawling from a root URL: Rejected in favor of the more direct `sitemap.xml` approach given the user's explicit preference.
    - Using a full-fledged scraping framework (e.g., Scrapy): Still considered overkill for parsing a known static site structure.

---

### 3. Text Chunking Strategy

- **Decision**: Text will be chunked by paragraph. This means each `<p>` tag's content will be treated as a single chunk.
- **Rationale**: Chunking by paragraph ensures semantic integrity, as paragraphs typically represent a single coherent idea or topic. This aligns with the user's explicit preference.
- **Alternatives Considered**:
    - `langchain.text_splitter.RecursiveCharacterTextSplitter`: While generally effective for RAG, the user specifically requested paragraph-based chunking, which simplifies implementation for this use case.
    - Simple character splitting: Prone to breaking sentences and losing context.
    - Fixed token count: May split sentences or ideas across chunks.

---

### 4. Cohere API Integration

- **Decision**: The `cohere` Python client will be used. The pipeline will batch the text chunks and make requests to the `embed` endpoint to generate embeddings efficiently. The `embed-english-v3.0` model will be used.
- **Rationale**: Batching is crucial for performance and for staying within the API's rate limits. The official client handles the complexities of API interaction.
- **Alternatives Considered**:
    - Manual HTTP requests: More error-prone and requires manual implementation of batching and retry logic.

---

### 5. Qdrant Client Integration

- **Decision**: The `qdrant-client` will be used to interact with Qdrant Cloud. The pipeline will first check if the specified collection exists and create it if it doesn't, configuring the vector size to match the Cohere model's output. Data will be inserted using the `upsert` method, which allows for both initial creation and later updates.
- **Rationale**: The `upsert` operation is idempotent and simplifies the logic for re-running the pipeline, as it handles both new and existing data gracefully. The official client is the most reliable way to interact with the database.
- **Alternatives Considered**:
    - Direct REST API calls to Qdrant: More complex and requires manual handling of authentication and request formatting.
