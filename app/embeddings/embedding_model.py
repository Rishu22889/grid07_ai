# Embedding model setup
# app/embeddings/embedding_model.py

from __future__ import annotations
from functools import lru_cache
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config.settings import EMBEDDING_MODEL, GOOGLE_API_KEY

@lru_cache(maxsize=1)
def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    if not GOOGLE_API_KEY:
        raise EnvironmentError("GOOGLE_API_KEY is not set in environment variables.")
    
    print(f"[Embeddings] Loading model: {EMBEDDING_MODEL}")

    embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, api_key=GOOGLE_API_KEY)

    return embedding_model


def embed_doc(text: list[str]) -> list[float]:
    model = get_embedding_model()
    embedding = model.embed_documents(text)
    return embedding

def embed_query(text: list[str]) -> list[float]:
    model = get_embedding_model()
    embedding = model.embed_query(text)
    return embedding
