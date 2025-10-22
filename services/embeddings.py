import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-004"


def create_embedding(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Tekst do embeddingu nie może być pusty.")

    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document"
    )

    embedding_vector = result["embedding"]

    embedding_data = {
        "text": text,
        "embedding": embedding_vector
    }

    return embedding_data

