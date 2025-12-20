---

description: "Task list for RAG Data Ingestion Pipeline feature implementation"
---

# Tasks: RAG Data Ingestion Pipeline

**Input**: Design documents from `specs/002-rag-data-ingestion/`
**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `research.md`, `data-model.md`, `quickstart.md`

**Tests**: This plan does not explicitly include separate test tasks per user story, but rather a final verification task for the entire pipeline. If a TDD approach or more granular testing is desired, these tasks should be added.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All source code will be within the `rag_pipeline/` directory.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `rag_pipeline` directory at the repository root.
- [X] T002 Initialize Python project with UV and create `requirements.txt` in `rag_pipeline/`.
- [X] T003 [P] Create `main.py` in `rag_pipeline/`.
- [X] T004 [P] Create `.env.example` in `rag_pipeline/` to document required environment variables.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Add `python-dotenv`, `requests`, `beautifulsoup4`, `cohere`, `qdrant-client`, `langchain` to `rag_pipeline/requirements.txt`.
- [X] T006 Implement environment variable loading in `rag_pipeline/main.py`.
- [X] T007 Implement a utility function to initialize the Qdrant client in `rag_pipeline/main.py`.
- [X] T008 Implement a utility function to initialize the Cohere client in `rag_pipeline/main.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Content Extraction (Priority: P1) 🎯 MVP

**Goal**: Scrape all pages of a deployed Docusaurus website and extract clean, textual content.

**Independent Test**: The pipeline can be run against a sample Docusaurus site, and the output for each page is verified to be clean text content, stripped of HTML, CSS, and JavaScript.

### Implementation for User Story 1

- [X] T009 [US1] Implement `get_sitemap_urls(sitemap_url: str) -> List[str]` function to parse `sitemap.xml` and extract all URLs in `rag_pipeline/main.py`.
- [X] T010 [US1] Implement `fetch_html_content(url: str) -> str` function to fetch HTML content for a given URL in `rag_pipeline/main.py`.
- [X] T011 [US1] Implement `extract_clean_text(html_content: str) -> str` function to parse HTML and extract clean text using `BeautifulSoup` in `rag_pipeline/main.py`.
- [X] T012 [US1] Implement `chunk_text_by_paragraph(text: str) -> List[str]` function to divide extracted text into paragraphs in `rag_pipeline/main.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Embedding and Storage (Priority: P1)

**Goal**: Take extracted text, generate vector embeddings (Cohere), and store with metadata in Qdrant.

**Independent Test**: Given a set of text documents, the system can generate embeddings and successfully store them in the Qdrant database. A retrieval test from Qdrant should return the correct documents for a known query.

### Implementation for User Story 2

- [X] T013 [US2] Implement `get_cohere_embeddings(texts: List[str]) -> List[List[float]]` function to generate embeddings using the Cohere API in `rag_pipeline/main.py`.
- [X] T014 [US2] Implement `create_qdrant_collection(collection_name: str, vector_size: int, client: QdrantClient)` function to create the Qdrant collection (e.g., `rag_embedding`) in `rag_pipeline/main.py`.
- [X] T015 [US2] Implement `save_chunks_to_qdrant(collection_name: str, chunks: List[dict], embeddings: List[List[float]], client: QdrantClient)` function to store embeddings and metadata in Qdrant in `rag_pipeline/main.py`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Pipeline Re-run and Updates (Priority: P2)

**Goal**: Make pipeline re-runnable to update vector database with website content changes.

**Independent Test**: After making a change to a page on the Docusaurus site, re-running the pipeline should result in the corresponding vector in Qdrant being updated or replaced.

### Implementation for User Story 3

- [X] T016 [US3] Modify `save_chunks_to_qdrant` to use `upsert` functionality for idempotency in `rag_pipeline/main.py`.
- [X] T017 [US3] Implement a mechanism to uniquely identify content chunks (e.g., hash of URL + text content) for efficient updates in `rag_pipeline/main.py`.

**Checkpoint**: All user stories should now be independently functional

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall pipeline quality

- [X] T018 Integrate all functions into a `main()` execution block within `rag_pipeline/main.py` to orchestrate the pipeline flow.
- [X] T019 Add comprehensive error handling and logging throughout `rag_pipeline/main.py`.
- [X] T020 Implement a basic retrieval test at the end of `main()` execution to verify Qdrant functionality in `rag_pipeline/main.py`.
- [X] T021 Update `rag_pipeline/quickstart.md` with final instructions and configuration details.
- [X] T022 Refine and organize `rag_pipeline/requirements.txt` to include exact versions.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No direct dependencies on US1 for its core functionality, but consumes its output.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for its update mechanism.

### Within Each User Story

- Implementation of utility functions (e.g., client initialization) should precede their usage.
- URL discovery -> HTML fetching -> text extraction -> chunking.
- Embedding generation -> collection creation -> saving to Qdrant.
- Unique identification of chunks should be in place before `upsert` logic.

### Parallel Opportunities

- Tasks marked with [P] within a phase can run in parallel.
- Different user stories can be worked on in parallel by different team members once the Foundational phase is complete.

---

## Parallel Example: User Story 1

```bash
# Example of parallel execution for setup tasks:
- [ ] T003 [P] Create main.py in rag_pipeline/
- [ ] T004 [P] Create .env.example in rag_pipeline/
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

Given that both User Story 1 (Content Extraction) and User Story 2 (Embedding and Storage) are P1 priority and represent the core functionality of the pipeline, the MVP will encompass both:

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  Complete Phase 4: User Story 2
5.  **STOP and VALIDATE**: Test User Stories 1 and 2 independently and combined.
6.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Ready for integration
3.  Add User Story 2 → Test independently → Deploy/Demo (MVP with core functionality!)
4.  Add User Story 3 → Test independently → Deploy/Demo (Pipeline update capabilities)

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Content Extraction)
    -   Developer B: User Story 2 (Embedding and Storage)
    -   Developer C: User Story 3 (Pipeline Re-run and Updates)
3.  Stories complete and integrate as per dependencies.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests (if applicable) fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
