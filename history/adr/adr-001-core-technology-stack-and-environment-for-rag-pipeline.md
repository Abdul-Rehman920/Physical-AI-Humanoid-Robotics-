# ADR-001: Core Technology Stack and Environment for RAG Pipeline

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2025-12-18
- **Feature:** 002-rag-data-ingestion
- **Context:** Establishing a robust and efficient development environment and selecting foundational technologies for a data ingestion pipeline that scrapes Docusaurus content, generates embeddings, and stores them in Qdrant. The goal is to leverage well-supported tools that streamline development and ensure maintainability.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

The core technology stack and environment for the RAG data ingestion pipeline will consist of:
-   **Language:** Python 3.11+
-   **Package Manager:** UV
-   **Core Libraries:**
    -   `requests`: For making HTTP requests to scrape web content.
    -   `beautifulsoup4`: For parsing HTML and extracting clean text.
    -   `cohere`: Official Python client for Cohere API integration.
    -   `qdrant-client`: Official Python client for Qdrant vector database interaction.
    -   `python-dotenv`: For loading environment variables from `.env` files.
    -   `langchain`: Utilized specifically for advanced text splitting capabilities (though paragraph splitting was chosen).
-   **Environment Setup:** Sensitive information (API keys, URLs) will be managed via environment variables and loaded using `python-dotenv`.

## Consequences

### Positive

-   Leverages Python's extensive ecosystem, providing a rich set of libraries for data processing, web scraping, and AI/ML tasks.
-   UV package manager offers significantly faster and more reliable dependency resolution and installation, enhancing developer experience and CI/CD pipelines.
-   Utilizing dedicated client libraries for Cohere and Qdrant simplifies API interactions, handling authentication, request formatting, and error management internally.
-   Secure handling of API keys and sensitive URLs through environment variables prevents accidental exposure and facilitates easy credential rotation across different environments.
-   `langchain` provides battle-tested text splitting algorithms, which can be adapted if the paragraph-only strategy proves insufficient.

### Negative

-   The project introduces a dependency on multiple external libraries, necessitating careful version management and vigilance for breaking changes in future updates.
-   New team members might face a learning curve if unfamiliar with specific libraries like `qdrant-client` or the `uv` package manager.
-   Reliance on `python-dotenv` for local development requires developers to correctly configure their `.env` files.

## Alternatives Considered

-   **Alternative Core Libraries:**
    -   **Manual HTTP requests and custom parsing:** Instead of `requests`/`beautifulsoup4`, `cohere` client, `qdrant-client`.
        -   **Why rejected:** Significantly increases development effort, code complexity, and introduces higher risk of bugs due to manual implementation of features like retries, backoff, authentication, and API-specific formatting.
-   **Alternative Package Manager:**
    -   `pip` with `pip-tools` or `Poetry`.
        -   **Why rejected:** While viable, `uv` was chosen for its superior speed and efficiency in dependency resolution and installation, which is a key factor for local development and CI/CD.
-   **Alternative Secret Management:**
    -   **Hardcoding secrets directly in code:**
        -   **Why rejected:** Unacceptable security risk, makes credential rotation difficult, and prevents easy deployment to different environments (e.g., development, staging, production) without code changes.
    -   **Cloud-specific secret managers (e.g., AWS Secrets Manager, Azure Key Vault):**
        -   **Why rejected:** Over-engineered for the current project scope and local development needs; `python-dotenv` provides sufficient security and flexibility for this stage.

## References

- Feature Spec: `specs/002-rag-data-ingestion/spec.md`
- Implementation Plan: `specs/002-rag-data-ingestion/plan.md`
- Related ADRs: N/A
- Evaluator Evidence: `specs/002-rag-data-ingestion/research.md`
