from agents import Agent, Runner, function_tool, set_tracing_disabled, set_default_openai_client
#from agents.models import OpenAIChatCompletionsModel
#from openai import AsyncOpenAI
from openai import OpenAI

from typing import Dict, List, Any
import os
from dotenv import load_dotenv
import time
import logging
import json

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
set_tracing_disabled(disabled=True)

# Configure Gemini through OpenAI-compatible endpoint
gemini_api_key = os.getenv("GEMINI_API_KEY")
#provider = AsyncOpenAI(
gemini_client = OpenAI(  # Changed to sync OpenAI
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
#model = OpenAIChatCompletionsModel(
#    model="gemini-2.0-flash-exp",
#    openai_client=provider
#)

# Set Gemini client as default for agents
set_default_openai_client(gemini_client)

from retrieval import RAGRetriever

@function_tool
def retrieve_information(query: str) -> Dict[str, Any]:
    """
    Retrieves relevant information based on the query using the RAGRetriever.
    """
    try:
        retriever = RAGRetriever()
        json_response = retriever.retrieve(query=query, top_k=5, threshold=0.3)
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
        instructions = """
You are a helpful AI assistant specialized in answering questions about physical AI and robotics based on provided documents.

When a user asks a question:
1. First, call the 'retrieve_information' tool with the user's query
2. Use ONLY the retrieved content to answer the question
3. Always cite your sources by referencing the URLs from the retrieved chunks
4. If no relevant information is found, say "I don't have enough information in the knowledge base to answer this question."
"""
        self.agent = Agent(
            name="RAG Assistant",
            tools=[retrieve_information],
            instructions=instructions,
            model="gemini-2.0-flash-exp"  # Gemini model name
        )
        logging.info("RAG Agent initialized with Gemini through OpenAI SDK")

    def _calculate_confidence(self, matched_chunks: List[Dict]) -> str:
        if not matched_chunks:
            return "low"
        
        avg_score = sum(chunk.get("similarity_score", 0) for chunk in matched_chunks) / len(matched_chunks)
        
        if avg_score > 0.8:
            return "high"
        elif avg_score > 0.6:
            return "medium"
        else:
            return "low"

    def query_agent(self, query_text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            logging.info(f"Processing query: '{query_text[:50]}...'")
            
            # Run agent synchronously using Runner.run_sync
            result = Runner.run_sync(self.agent, input=query_text)
            
            # Extract response
            answer = result.final_output if hasattr(result, 'final_output') else "No answer generated."
            
            # Try to extract matched chunks and sources from tool calls
            matched_chunks = []
            sources = set()
            
            # Check if we can access tool results
            if hasattr(result, 'result') and result.result:
                if hasattr(result.result, 'tool_code_results'):
                    for tool_result in result.result.tool_code_results:
                        if tool_result.tool_name == "retrieve_information" and tool_result.result:
                            retrieval_data = tool_result.result
                            if retrieval_data.get("retrieved_chunks"):
                                matched_chunks = retrieval_data["retrieved_chunks"]
                                sources = set([chunk["url"] for chunk in matched_chunks])
            
            query_time_ms = (time.time() - start_time) * 1000
            confidence = self._calculate_confidence(matched_chunks)
            
            response = {
                "answer": str(answer),
                "sources": list(sources),
                "matched_chunks": matched_chunks,
                "error": None,
                "status": "success",
                "query_time_ms": query_time_ms,
                "confidence": confidence
            }
            
            logging.info(f"Query processed in {query_time_ms:.2f}ms")
            return response
            
        except Exception as e:
            logging.error(f"Error processing query: {e}")
            return {
                "answer": "Sorry, I encountered an error processing your request.",
                "sources": [],
                "matched_chunks": [],
                "error": str(e),
                "status": "error",
                "query_time_ms": (time.time() - start_time) * 1000,
                "confidence": "low"
            }

if __name__ == "__main__":
    agent = RAGAgent()
    sample_query = "What is Physical AI?"
    print(f"Querying agent with: '{sample_query}'")
    response = agent.query_agent(sample_query)
    print("\n--- Agent Response ---")
    print(f"Answer: {response.get('answer')}")
    print(f"\nSources ({len(response.get('sources', []))}):")
    for source in response.get('sources', []):
        print(f"  - {source}")
    print(f"\nConfidence: {response.get('confidence')}")
    print(f"Query time: {response.get('query_time_ms', 0):.2f}ms")
    if response.get("error"):
        print(f"Error: {response.get('error')}")