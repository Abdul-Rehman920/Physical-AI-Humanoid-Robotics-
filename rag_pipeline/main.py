import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient, models
import requests
from bs4 import BeautifulSoup
from typing import List
import xml.etree.ElementTree as ET
import hashlib
import logging
import time
import httpx
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    logging.info("Environment variables loaded.")

def initialize_cohere_client():
    """Initialize and return the Cohere client."""
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logging.error("COHERE_API_KEY environment variable not set.")
        raise ValueError("COHERE_API_KEY environment variable not set.")
    logging.info("Cohere client initialized.")
    return cohere.Client(cohere_api_key)

def initialize_qdrant_client():
    """Initialize and return the Qdrant client."""
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    if not qdrant_url or not qdrant_api_key:
        logging.error("QDRANT_URL or QDRANT_API_KEY environment variables not set.")
        raise ValueError("QDRANT_URL or QDRANT_API_KEY environment variables not set.")
    logging.info("Qdrant client initialized.")
    return QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

def get_sitemap_urls(sitemap_url: str) -> List[str]:
    """Parse sitemap.xml and extract all URLs."""
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        logging.info(f"Found {len(urls)} URLs in sitemap.")
        return urls
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching sitemap: {e}")
        return []

def fetch_html_content(url: str) -> str:
    """Fetch HTML content for a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching HTML from {url}: {e}")
        return ""

def extract_clean_text(html_content: str) -> str:
    """Parse HTML and extract clean text using BeautifulSoup."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('article')
    if main_content:
        return main_content.get_text(separator='\n', strip=True)
    return ""

def smart_chunk_text(text: str, chunk_size: int = 400, overlap: int = 50, min_words: int = 50) -> List[str]:
    """
    Intelligently chunk text into meaningful segments.
    
    Args:
        text: Input text to chunk
        chunk_size: Target number of words per chunk
        overlap: Number of words to overlap between chunks
        min_words: Minimum words required for a chunk to be valid
    
    Returns:
        List of text chunks (only chunks with >= min_words)
    """
    # Clean text: normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Check if text meets minimum word requirement
    words = text.split()
    if len(words) < min_words:
        return []  # Skip pages with too little content
    
    # If text is shorter than chunk_size but meets minimum, return as single chunk
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    i = 0
    while i < len(words):
        # Get chunk_size words
        chunk_words = words[i:i + chunk_size]
        chunk_text = ' '.join(chunk_words)
        
        # Only add chunks that meet minimum word count
        if len(chunk_words) >= min_words:
            chunks.append(chunk_text)
        
        # Move forward with overlap
        i += (chunk_size - overlap)
    
    return chunks

def get_cohere_embeddings(texts: List[str], client: cohere.Client) -> List[List[float]]:
    """Generate embeddings using the Cohere API with retry logic and batching."""
    all_embeddings = []
    batch_size = 96 # Cohere API often works well with batch sizes around 96

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.embed(texts=batch_texts, model='embed-english-v3.0', input_type='search_document')
                all_embeddings.extend(response.embeddings)
                logging.info(f"Generated embeddings for batch {i // batch_size + 1}/{len(texts) // batch_size + 1}.")
                break  # Break out of the retry loop if successful
            except httpx.ReadError as e:
                logging.error(f"HTTP Read Error (Cohere API) for batch {i // batch_size + 1} on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    logging.critical(f"Failed to generate embeddings for batch {i // batch_size + 1} after {max_retries} attempts due to HTTP Read Error.")
                    raise
            except Exception as e: # Catch other potential Cohere or network errors
                logging.error(f"Error generating embeddings for batch {i // batch_size + 1} on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    logging.critical(f"Failed to generate embeddings for batch {i // batch_size + 1} after {max_retries} attempts.")
                    raise
    
    logging.info(f"Generated total {len(all_embeddings)} embeddings.")
    return all_embeddings
def create_qdrant_collection(collection_name: str, vector_size: int, client: QdrantClient):
    """Create the Qdrant collection."""
    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        logging.info(f"Qdrant collection '{collection_name}' created or recreated.")
    except Exception as e:
        logging.error(f"Error creating Qdrant collection: {e}")
        raise

def check_and_print_collection_info(collection_name: str, client: QdrantClient):
    """Check if a collection exists and print its information."""
    try:
        collection_info = client.get_collection(collection_name=collection_name)
        logging.info(f"Collection '{collection_name}' exists.")
        logging.info(f"Collection info: {collection_info.json()}")
    except Exception as e:
        logging.info(f"Collection '{collection_name}' does not exist or an error occurred: {e}")

def save_chunks_to_qdrant(collection_name: str, chunks: List[dict], embeddings: List[List[float]], client: QdrantClient):
    """Store embeddings and metadata in Qdrant with batching and retry logic."""
    if not embeddings:
        logging.warning("No embeddings to save.")
        return

    points = []
    # Loop through chunks and embeddings together, using an incrementing integer ID
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
        points.append(models.PointStruct(
            id=idx,  # Use integer ID
            vector=embedding,
            payload=chunk
        ))

    batch_size = 50
    total_batches = (len(points) + batch_size - 1) // batch_size  # ✅ Calculate total

    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        batch_num = i//batch_size + 1  # ✅ Define batch_num HERE
        max_retries = 3

        for attempt in range(max_retries):
            try:
                client.upsert(collection_name=collection_name, points=batch, wait=True)
                logging.info(f"✓ Uploaded batch {batch_num}/{total_batches} to Qdrant collection '{collection_name}'.")
                break  # Break out of the retry loop if successful
            except ConnectionResetError as e:  # Catch WinError 10054
                logging.error(f"Connection error (WinError 10054) on batch {batch_num}, attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3  # 3s, 6s, 9s
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.critical(f"Failed to save batch {batch_num} after {max_retries} attempts due to connection error.")
                    raise                   
            except Exception as e:
                logging.error(f"Error on batch {batch_num}, attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    # ✅ CHANGE 4: Exponential backoff for generic errors too
                    wait_time = (attempt + 1) * 3  # 3s, 6s, 9s
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.critical(f"Failed to save batch {batch_num} after {max_retries} attempts.")
                    raise

def run_retrieval_test(query_text: str, collection_name: str, cohere_client: cohere.Client, qdrant_client: QdrantClient):
    """Run a basic retrieval test."""
    logging.info(f"Running retrieval test with query: '{query_text}'")
    query_embedding = get_cohere_embeddings([query_text], cohere_client)[0]
    
    search_result = qdrant_client.query_points( 
        collection_name=collection_name,
        query=query_embedding,
        limit=3
    ).points
    
    logging.info("Top 3 search results:")
    for result in search_result:
        logging.info(f"  - ID: {result.id}, Score: {result.score}")
        logging.info(f"    Payload: {result.payload}")

def main():
    """Main function to orchestrate the pipeline."""
    load_environment()
    
    try:
        cohere_client = initialize_cohere_client()
        qdrant_client = initialize_qdrant_client()
    except ValueError as e:
        logging.critical(f"Client initialization failed: {e}")
        return

    collection_name = "rag_embedding"
    vector_size = 1024  # From Cohere documentation
    
    try:
        create_qdrant_collection(collection_name, vector_size, qdrant_client)
    except Exception:
        logging.critical("Failed to create Qdrant collection. Aborting.")
        return

    start_url = os.getenv("START_URL")
    if not start_url:
        logging.critical("START_URL environment variable not set. Aborting.")
        return
        
    sitemap_url = start_url.rstrip('/') + '/sitemap.xml'
    
    urls = get_sitemap_urls(sitemap_url)
    if not urls:
        logging.warning("No URLs found in sitemap. Exiting.")
        return

    all_chunks = []
    for url in urls:
        logging.info(f"Processing {url}...")
        html_content = fetch_html_content(url)
        clean_text = extract_clean_text(html_content)
        if clean_text:
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.find('h1').text if soup.find('h1') else 'No Title'
            
            # ✅ USE SMART CHUNKING WITH QUALITY FILTER
            chunks = smart_chunk_text(clean_text, chunk_size=400, overlap=50, min_words=50)
            
            if not chunks:
                logging.info(f"  - Skipped (insufficient content: {len(clean_text.split())} words)")
                continue
            
            for chunk in chunks:
                all_chunks.append({
                    "page_title": title, 
                    "source_url": url, 
                    "text_content": chunk
                })
            
            logging.info(f"  - Created {len(chunks)} smart chunks (avg {sum(len(c.split()) for c in chunks)//len(chunks)} words/chunk).")
    
    if all_chunks:
        chunk_texts = [chunk['text_content'] for chunk in all_chunks]
        embeddings = get_cohere_embeddings(chunk_texts, cohere_client)
        save_chunks_to_qdrant(collection_name, all_chunks, embeddings, qdrant_client)
        
        # Retrieval Test
        run_retrieval_test("What is Physical AI?", collection_name, cohere_client, qdrant_client)

    check_and_print_collection_info(collection_name, qdrant_client)

if __name__ == '__main__':
    main()
