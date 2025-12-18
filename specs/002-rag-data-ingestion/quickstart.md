# Quickstart Guide: RAG Data Ingestion Pipeline

**Branch**: `002-rag-data-ingestion` | **Date**: 2025-12-18 | **Plan**: [plan.md](plan.md)
**Spec**: [spec.md](spec.md)

This guide provides instructions to set up and run the RAG Data Ingestion Pipeline locally.

---

## Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.11+**: [Download and install Python](https://www.python.org/downloads/)
-   **UV Package Manager**: Install UV by following instructions on its official site (e.g., `curl -sSL https://uv.sh/install.sh | sh` or `pip install uv`).

## 1. Project Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd rag-pipeline
    ```
    *(Note: Replace `<repository_url>` with the actual URL of your repository and `rag-pipeline` with the directory containing `main.py` once it's created.)*

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
    *(Note: `requirements.txt` will be generated during the implementation phase.)*

## 2. Configuration

The pipeline requires API keys for Cohere and connection details for Qdrant. These should be provided via environment variables.

1.  **Create `.env` file**:
    In the root of your `rag_pipeline` directory, create a file named `.env` and add the following:

    ```ini
    COHERE_API_KEY="your_cohere_api_key_here"
    QDRANT_API_KEY="your_qdrant_api_key_here"
    QDRANT_URL="your_qdrant_cloud_url_here"
    START_URL="https://abdul-rehman920.github.io/Physical-AI-Humanoid-Robotics-/"
    ```
    *(Note: Replace the placeholder values with your actual API keys and Qdrant Cloud URL. The `START_URL` is the root of the Docusaurus website to be scraped.)*

2.  **Get API Keys**:
    -   **Cohere**: Sign up at [Cohere](https://cohere.com/) and obtain your API key.
    -   **Qdrant Cloud**: Sign up at [Qdrant Cloud](https://cloud.qdrant.io/) to get your cluster URL and API key.

## 3. Execution

Once configured, you can run the pipeline:

```bash
python main.py
```
This command will:
1. Discover URLs from the Docusaurus website using `sitemap.xml`.
2. Scrape and extract text content from each page.
3. Chunk the text content by paragraph.
4. Generate embeddings using the Cohere API.
5. Store embeddings and metadata in Qdrant Cloud.

## 4. Verification

The `main.py` script will include a basic retrieval test at the end of its execution. After the pipeline completes, you should see output indicating the results of this test, confirming that relevant information can be retrieved from the Qdrant database.
