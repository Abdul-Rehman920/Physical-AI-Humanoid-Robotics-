# verify_qdrant.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=60
)

# Check collection
collection_name = "rag_embedding"

# Get collection info
info = client.get_collection(collection_name)
print(f"Collection Name: {collection_name}")
print(f"Points Count: {info.points_count}")
print(f"Indexed Vectors: {info.indexed_vectors_count}")  # ✅ Fixed
print(f"Status: {info.status}")
print(f"Segments: {info.segments_count}")

# Try to retrieve a sample point
points = client.scroll(
    collection_name=collection_name,
    limit=5
)

print(f"\nSample Points (showing {len(points[0])} of {info.points_count}):")
for point in points[0]:
    print(f"\n  ID: {point.id}")
    print(f"  Payload keys: {list(point.payload.keys())}")
    print(f"  Text preview: {point.payload.get('text_content', 'N/A')[:100]}...")