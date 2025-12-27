import os
import cohere
import qdrant_client
from dotenv import load_dotenv
import logging
import json
import argparse
from time import time

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get API keys from environment
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

class RAGRetriever:
    """
    A class to retrieve relevant text chunks from a Qdrant database using Cohere embeddings.
    """
    def __init__(self):
        """
        Initializes the Cohere and Qdrant clients.
        """
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY not found in environment variables.")
        self.cohere_client = cohere.Client(COHERE_API_KEY)
        
        self.qdrant_client = qdrant_client.QdrantClient(
            url=QDRANT_URL, 
            api_key=QDRANT_API_KEY,
        )
        self.collection_name = "rag_embedding"
    def get_query_embedding(self, query: str) -> list[float]:
        """
        Generates an embedding for the given query using Cohere.
        """
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",  # ✅ CHANGE: Same as main.py
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logging.error(f"Error generating query embedding: {e}")
            raise
    def search_similar_chunks(self, query_embedding: list[float], top_k: int = 5, threshold: float = 0.0) -> list:
        """
        Searches for similar chunks in the Qdrant collection.
        """
        try:
            response = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                score_threshold=threshold,
                with_payload=True
            )

            print(f"DEBUG: Response points count: {len(response.points)}")  # ← ADD THIS LINE

            # ADD THESE 3 LINES HERE:
            if response.points:
                print(f"DEBUG: Payload keys: {list(response.points[0].payload.keys())}")
                print(f"DEBUG: Sample payload: {response.points[0].payload}")

            results = []
            for point in response.points:
                payload = point.payload
                if payload:
                    results.append({
                        "content": payload.get("text_content"),
                        "url": payload.get("source_url"),
                        "position": payload.get("chunk_index"),
                        "similarity_score": point.score,
                        "chunk_id": point.id,
                        "created_at": payload.get("created_at")
                    })
                    
            print(f"DEBUG: Results count: {len(results)}")  # ← ADD THIS LINE                    
            return results
        except Exception as e:
            logging.error(f"Error searching for similar chunks: {e}")
            raise    
    def retrieve(self, query: str, top_k: int = 5, threshold: float = 0.0) -> str:
        """
        Orchestrates the retrieval workflow.
        """
        start_time = time()
        
        logging.info(f"Generating embedding for query: '{query}'")
        query_embedding = self.get_query_embedding(query)
        
        logging.info("Searching for similar chunks...")
        similar_chunks = self.search_similar_chunks(query_embedding, top_k, threshold)

        # ADD THESE LINES BELOW:
        logging.info("Validating retrieved chunks...")
        is_valid = self.validate_retrieval(similar_chunks)
        if not is_valid:
            logging.warning("Retrieval validation failed.")

        end_time = time()
        query_time = end_time - start_time
        
        logging.info(f"Found {len(similar_chunks)} results in {query_time:.4f} seconds.")
        
        return self.format_response(query, similar_chunks, query_time)
    def format_response(self, query: str, results: list, query_time: float) -> str:
        """
        Formats the results into a JSON string.
        """
        response = {
            "query": query,
            "query_time": query_time,
            "result_count": len(results),
            "timestamp": time(),
            "results": results
        }
        return json.dumps(response, indent=4)
    def validate_retrieval(self, chunks: list) -> bool:
        """
        Validates the retrieved chunks.
        """
        for chunk in chunks:
            if not chunk.get("content") or not chunk.get("url"):
                logging.warning(f"Missing 'content' or 'url' in chunk: {chunk}")
                return False
            if not (0.0 <= chunk.get("similarity_score", 0.0) <= 1.0):
                logging.warning(f"Invalid similarity score in chunk: {chunk}")
                return False
        return True
           
        logging.info("Validating retrieved chunks...")
        is_valid = self.validate_retrieval(similar_chunks)
        if not is_valid:
            logging.warning("Retrieval validation failed.")
            # Decide if you want to return empty or partial results
            # For now, we'll return what we have but log the warning.

        end_time = time()
        query_time = end_time - start_time
        
        logging.info(f"Found {len(similar_chunks)} results in {query_time:.4f} seconds.")
        
        return self.format_response(query, similar_chunks, query_time)
def test_retrieval_pipeline(retriever: RAGRetriever):
    """
    Tests the retrieval pipeline with a set of diverse queries.
    """
    test_queries = [
        "What is Physical AI?",
        "Explain the difference between digital and physical intelligence.",
        "What are some real-world applications of Physical AI?",
        "How does a humanoid robot work?",
        "What is the role of simulation in robotics?",
    ]
    
    for query in test_queries:
        print("-" * 50)
        print(f"Testing query: '{query}'")
        response_json = retriever.retrieve(query)  # ✅ Yeh line hai
        print(response_json)  # ✅ Par print None kyun aa raha?
def retrieve_all_stored_data(retriever: RAGRetriever):
    """
    Retrieves all stored data from the Qdrant collection.
    """
    try:
        collection_info = retriever.qdrant_client.get_collection(collection_name=retriever.collection_name)
        logging.info(f"Collection Info: {collection_info}")

        scroll_result = retriever.qdrant_client.scroll(
            collection_name=retriever.collection_name,
            with_payload=True,
            limit=10  # Show first 10, add pagination if needed
        )
        print(json.dumps(scroll_result, indent=4))

    except Exception as e:
        logging.error(f"Error retrieving all data: {e}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Retrieval Pipeline Test CLI")
    parser.add_argument("--all", action="store_true", help="Display all stored data from the collection.")
    parser.add_argument("--query", type=str, help="Run a single query test.")
    
    args = parser.parse_args()
    
    try:
        retriever = RAGRetriever()
        
        if args.all:
            logging.info("Retrieving all stored data...")
            retrieve_all_stored_data(retriever)
        elif args.query:
            logging.info(f"Running single query test for: '{args.query}'")
            response = retriever.retrieve(args.query)
            print(response)
        else:
            logging.info("Running standard test queries...")
            test_retrieval_pipeline(retriever)
            
    except ValueError as e:
        logging.error(f"Initialization failed: {e}")
    except Exception as e:
        logging.error(f"An error occurred during the retrieval process: {e}")
    