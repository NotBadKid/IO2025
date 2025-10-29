from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "kids_assistant"

client = QdrantClient(url=QDRANT_URL)

def init_collection():
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

init_collection()

def save_entry(question: str, answer: str, vector: list[float]):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=None,
                vector=vector,
                payload={"question": question, "answer": answer},
            )
        ]
    )

def search_similar(vector: list[float], threshold: float = 0.7):
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=1,
    )
    if hits and hits[0].score >= threshold:
        return hits[0].payload["answer"]
    return None
