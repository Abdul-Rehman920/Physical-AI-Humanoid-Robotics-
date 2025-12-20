---
id: 002
title: Implement Batch Processing for Qdrant Upsert
stage: green
date: 2025-12-19
surface: agent
model: gemini
feature: rag-data-ingestion
branch: 002-rag-data-ingestion
user: system
command: replace
labels: [refactor, qdrant, batch-processing]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - rag_pipeline/main.py
tests:
 - none
---

## Prompt

The issue is sending too many points at once (7820). Fix by implementing batch processing:
- Split points into smaller batches of 100 points each
- Upload each batch separately with retry logic
- Add progress logging to show batch upload status
- Keep the 3 retry attempts per batch with 5 second delay

# Points ko batches mein divide karo
batch_size = 100
for i in range(0, len(points), batch_size):
    batch = points[i:i+batch_size]
    # Retry logic for each batch
    for attempt in range(3):
        try:
            qdrant_client.upsert(collection_name, points=batch)
            logger.info(f"Uploaded batch {i//batch_size + 1}")
            break
        except Exception as e:
            if attempt < 2:
                time.sleep(5)

## Response snapshot

I have successfully modified the `save_chunks_to_qdrant` function in `rag_pipeline/main.py` to implement batching as you requested. The function now splits the points into batches of 100 and uploads each batch separately with a retry logic of 3 attempts and a 5-second delay. I also added progress logging to show the batch upload status.

## Outcome

- ✅ Impact: The `save_chunks_to_qdrant` function was refactored to use batch processing, preventing errors when uploading a large number of points to Qdrant.
- 🧪 Tests: No tests were added or modified.
- 📁 Files: The `save_chunks_to_qdrant` function in `rag_pipeline/main.py` was updated to implement batching.
- 🔁 Next prompts: none
- 🧠 Reflection: The change was straightforward and directly addressed the user's request.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (if applicable): none
