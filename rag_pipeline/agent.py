from groq import Groq
import os
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv
import time

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from retrieval import RAGRetriever

def retrieve_information(query: str) -> Dict[str, Any]:
    """
    Retrieves relevant information based on the query using the RAGRetriever.
    """
    try:
        retriever = RAGRetriever()
        json_response = retriever.retrieve(query=query, top_k=10, threshold=0.3)
        results = json.loads(json_response)
        
        formatted_chunks = []
        for result in results.get('results', []):
            formatted_chunks.append({
                'content': result['content'],
                'url': result['url'],
                'position': result['position'],
                'similarity_score': result['similarity_score']
            })
        
        return {
            "query": query,
            "retrieved_chunks": formatted_chunks,
            "total_results": len(formatted_chunks)
        }
    except Exception as e:
        logging.error(f"Error in retrieve_information: {e}")
        return {
            "retrieved_chunks": [],
            "total_results": 0,
            "error": str(e)
        }

class RAGAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"  # FREE and powerful
        
        self.instructions = """
You are a helpful AI assistant specialized in answering questions about physical AI and robotics based on provided documents.

When asked a question:
1. Answer based on the retrieved documents
2. Always cite your sources by referencing the URLs
3. If no relevant information is found, state that you cannot answer based on the provided context
4. Be concise and accurate
"""
        logging.info(f"✅ RAG Agent initialized with Groq ({self.model_name})")

    def _calculate_confidence(self, matched_chunks: List[Dict]) -> str:
        if not matched_chunks:
            return "low"
        
        avg_score = sum(chunk.get("similarity_score", 0) for chunk in matched_chunks) / len(matched_chunks)
        
        if avg_score > 0.7:
            return "high"
        elif avg_score > 0.5:
            return "medium"
        else:
            return "low"

    def query_agent(self, query_text: str, max_retries: int = 3) -> Dict[str, Any]:
        start_time = time.time()
        
        # Step 1: Retrieve relevant chunks
        logging.info(f"Retrieving information for: '{query_text[:50]}...'")
        retrieval_result = retrieve_information(query_text)
        
        matched_chunks = retrieval_result.get("retrieved_chunks", [])
        logging.info(f"Retrieved {len(matched_chunks)} chunks")
        
        if not matched_chunks:
            return {
                "answer": "I couldn't find relevant information in the knowledge base to answer this question.",
                "sources": [],
                "matched_chunks": [],
                "error": None,
                "status": "success",
                "query_time_ms": (time.time() - start_time) * 1000,
                "confidence": "low"
            }
        
        # Step 2: Build context from retrieved chunks
        context = "\n\n".join([
            f"[Source {i+1} from {chunk['url']}]\n{chunk['content'][:500]}"
            for i, chunk in enumerate(matched_chunks[:5])
        ])
        
        # Step 3: Generate response with Groq
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": f"""Context from knowledge base:
{context}

User Question: {query_text}

Please provide a detailed answer based on the context above. Cite the sources by mentioning [Source 1], [Source 2], etc."""}
        ]

        for attempt in range(max_retries):
            try:
                logging.info(f"Generating response with Groq (attempt {attempt + 1}/{max_retries})...")
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                answer = response.choices[0].message.content
                sources = list(set([chunk['url'] for chunk in matched_chunks]))
                query_time_ms = (time.time() - start_time) * 1000
                confidence = self._calculate_confidence(matched_chunks)
                
                logging.info(f"✅ Successfully generated response")
                
                return {
                    "answer": answer,
                    "sources": sources,
                    "matched_chunks": matched_chunks,
                    "error": None,
                    "status": "success",
                    "query_time_ms": query_time_ms,
                    "confidence": confidence
                }
                
            except Exception as e:
                error_str = str(e).lower()
                if "rate" in error_str or "limit" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        logging.warning(f"Rate limit hit. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                logging.error(f"Error in query_agent: {e}")
                return {
                    "answer": "Sorry, I encountered an error processing your request.",
                    "sources": [],
                    "matched_chunks": [],
                    "error": str(e),
                    "status": "error",
                    "query_time_ms": (time.time() - start_time) * 1000,
                    "confidence": "low"
                }
        
        return {
            "answer": "Sorry, the service is temporarily unavailable. Please try again later.",
            "sources": [],
            "matched_chunks": [],
            "error": "Max retries exceeded",
            "status": "error",
            "query_time_ms": (time.time() - start_time) * 1000,
            "confidence": "low"
        }

if __name__ == "__main__":
    agent = RAGAgent()
    sample_query = "What is Physical AI?"
    print(f"\n{'='*60}")
    print(f"QUERYING: '{sample_query}'")
    print(f"{'='*60}\n")
    
    response = agent.query_agent(sample_query)
    
    print(f"\n{'='*60}")
    print("AGENT RESPONSE")
    print(f"{'='*60}\n")
    print(f"Answer:\n{response.get('answer')}\n")
    
    if response.get('sources'):
        print(f"Sources ({len(response.get('sources'))}):")
        for i, source in enumerate(response.get('sources'), 1):
            print(f"  [{i}] {source}")
    
    print(f"\nMetadata:")
    print(f"  • Confidence: {response.get('confidence')}")
    print(f"  • Query Time: {response.get('query_time_ms', 0):.2f}ms")
    print(f"  • Status: {response.get('status')}")
    
    if response.get("error"):
        print(f"  • Error: {response.get('error')}")