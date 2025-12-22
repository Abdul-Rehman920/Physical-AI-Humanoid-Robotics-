# Quickstart Guide: RAG Data Retrieval

**Branch**: `003-rag-data-retrieval` | **Date**: 2025-12-22 | **Plan**: [plan.md](plan.md)
**Spec**: [spec.md](spec.md)

This guide provides instructions to set up and run the RAG Data Retrieval service locally.

---

## Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.11+**: [Download and install Python](https://www.python.org/downloads/)
-   **UV Package Manager**: Install UV by following instructions on its official site (e.g., `curl -sSL https://uv.sh/install.sh | sh` or `pip install uv`).
-   **A running Qdrant instance**: This service assumes you have already populated a Qdrant collection named `rag_embedding` using the data ingestion pipeline.

## 1. Project Setup

1.  **Navigate to the `rag_pipeline` directory**:
    ```bash
    cd rag_pipeline
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    uv venv
    ```

3.  **Activate the Virtual Environment**:
    -   **Windows**: `.\.venv\Scripts\activate`
    -   **macOS/Linux**: `source ./.venv/bin/activate`

4.  **Install Dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

## 2. Configuration

The service requires API keys for Cohere and connection details for Qdrant. These should be provided via environment variables.

1.  **Create `.env` file**:
    In the root of your `rag_pipeline` directory, create a file named `.env` and add the following:

    ```ini
    COHERE_API_KEY="your_cohere_api_key_here"
    QDRANT_API_KEY="your_qdrant_api_key_here"
    QDRANT_URL="your_qdrant_cloud_url_here"
    ```
    *(Note: Replace the placeholder values with your actual API keys and Qdrant Cloud URL.)*

2.  **Get API Keys**:
    -   **Cohere**: Sign up at [Cohere](https://cohere.com/) and obtain your API key.
    -   **Qdrant Cloud**: Sign up at [Qdrant Cloud](https://cloud.qdrant.io/) to get your cluster URL and API key.

## 3. Execution

Once configured, you can run the retrieval script:

```bash
python retrieval.py --query "Your query here"
```
This command will:
1. Initialize Cohere and Qdrant clients.
2. Generate an embedding for your query using the Cohere API.
3. Search the `rag_embedding` collection in Qdrant for similar text chunks.
4. Return a JSON object containing the most relevant results.

### Example

```bash
python retrieval.py --query "What is Physical AI?"
```

You can also run a series of test queries defined in the script:

```bash
python retrieval.py
```

Or retrieve all stored data:
```bash
python retrieval.py --all
```

## 4. Verification

The `retrieval.py` script will print a JSON object to the console containing the search results. The output will include the retrieved text chunks, their source URLs, and similarity scores, allowing you to verify that the service is working correctly.
