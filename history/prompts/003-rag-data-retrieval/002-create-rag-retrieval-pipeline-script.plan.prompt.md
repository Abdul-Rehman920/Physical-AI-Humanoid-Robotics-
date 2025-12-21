---
id: 002
title: Create RAG Retrieval Pipeline Script
stage: plan
date: 2025-12-20
surface: agent
model: gemini-pro
feature: 003-rag-data-retrieval
branch: 003-rag-data-retrieval
user: unknown
command: /sp.plan
labels: ["plan", "rag", "python"]
links:
  spec: specs/003-rag-data-retrieval/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - rag_pipeline/retrieval.py
tests:
  - none
---

## Prompt

/sp.plan Create file at 'rag_pipeline/retrieval.py' with the following structure:

**Core Components:**

1. **RAGRetriever Class**
   - Initialize Cohere client for query embeddings
   - Initialize Qdrant client connection
   - Set collection_name = "rag_embedding"

2. **get_query_embedding() method**
   - Input: user query string
   - Generate embedding using Cohere embed-multilingual-v3.0
   - input_type="search_query" for optimized retrieval
   - Return: List[float] embedding vector
   - Handle errors gracefully with logging

3. **search_similar_chunks() method**
   - Input: query_embedding, top_k (default=5), threshold (default=0.0)
   - Query Qdrant collection with similarity search
   - Retrieve with_payload=True to get metadata
   - Return: List of formatted results with:
     * content (text chunk)
     * url (source URL)
     * position (chunk index)
     * similarity_score
     * chunk_id
     * created_at timestamp

4. **validate_retrieval() method**
   - Check retrieved chunks have required fields (content, url)
   - Verify similarity scores are within expected range
   - Log warnings for missing or malformed data
   - Return: boolean validation status

5. **format_response() method**
   - Structure results into clean JSON
   - Include query metadata (time, result count, timestamp)
   - Return: formatted JSON string

6. **retrieve() main method**
   - Orchestrate complete retrieval workflow:
     a. Generate query embedding
     b. Search Qdrant for similar vectors
     c. Validate results
     d. Format and return JSON response
   - Log query time and result count

**Testing Functions:**

7. **test_retrieval_pipeline()**
   - Test with 5+ diverse queries about book content
   - Print formatted results with similarity scores
   - Display query performance metrics
   - Test edge cases (empty results, low similarity scores)

8. **retrieve_all_stored_data()** (utility)
   - Use Qdrant scroll API to fetch all stored chunks
   - Display collection statistics
   - Show sample chunks with metadata
   - Useful for debugging and verification

**Main Execution:**
- Command-line interface:
  * `python retrieval.py` - Run test queries
  * `python retrieval.py --all` - Display all stored data
  * `python retrieval.py --query "your question"` - Single query test
- Comprehensive logging of all operations
- Error handling for missing API keys or connection failures

**Environment Setup:**
- Load from .env: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY
- Default Qdrant URL: http://localhost:6333 (or cloud URL)

**Key Differences from Reference File:**
- Optimize function names for clarity (search_similar_chunks vs query_qdrant)
- Add command-line argument support for flexible testing
- Enhanced validation logic specific to your data structure
- More detailed logging and error messages
- Structured testing workflow that matches your book content

Deliverable: Single retrieval.py file that can be run standalone to test the complete retrieval pipeline.

## Response snapshot

I have created the `retrieval.py` file in the `rag_pipeline` directory with the requested structure and content.

## Outcome

- ✅ Impact: Created a Python script for the RAG retrieval pipeline.
- 🧪 Tests: No tests were run.
- 📁 Files: Created `rag_pipeline/retrieval.py`.
- 🔁 Next prompts: /sp.implement or /sp.tasks
- 🧠 Reflection: The user provided a very detailed implementation plan, which made the task straightforward.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
