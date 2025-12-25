# Quickstart: RAG Agent API

This guide provides instructions on how to set up and run the RAG Agent API.

## Prerequisites

- Python 3.11
- `pip` for installing packages

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd textbook
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    Navigate to the `rag_pipeline` directory and install the required packages.
    ```bash
    cd rag_pipeline
    pip install -r requirements.txt
    ```
    You will need to add the new dependencies to `requirements.txt`:
    ```
    agents
    fastapi
    uvicorn[standard]
    pydantic
    python-dotenv
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the `rag_pipeline` directory and add any necessary environment variables (e.g., for connecting to Qdrant or other services).

## Running the API

1.  **Start the API server**:
    From the `rag_pipeline` directory, run the following command:
    ```bash
    uvicorn api:app --reload
    ```

2.  **Access the API documentation**:
    Once the server is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Health Check

- **Endpoint**: `GET /health`
- **Description**: Checks the health of the API.
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: `{"status": "ok", "message": "Service is healthy"}`

### Ask a Question

- **Endpoint**: `POST /ask`
- **Description**: Submits a query to the RAG agent.
- **Request Body**:
  ```json
  {
    "query": "Your question here"
  }
  ```
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**: A `QueryResponse` object with the answer, sources, and other metadata.

**Example using `curl`**:
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"query": "What is embodied intelligence?"}'
```
